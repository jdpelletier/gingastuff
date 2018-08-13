#in process
"""
Draft of NIRES plugin. Still in development
"""
from ginga import GingaPlugin, RGBImage, colors
from ginga.gw import Widgets, Viewers, Plot
from ginga.gw.GwHelp import FileSelection
from ginga.util import iqcalc, plots, dp
import numpy as np


__all__ = ['Nires']


class NiresTest(GingaPlugin.LocalPlugin):

    def __init__(self, fv, fitsimage):
        # superclass defines some variables for us, like logger
        super(NiresTest, self).__init__(fv, fitsimage)

        self.niimage = None
        self.nisky = None
        self.sqcolor = 'green'
        self.layertag = 'nires-canvas'
        self.fwhm_plot = None
        self.iqcalc = iqcalc.IQCalc(self.logger)
        self.xclick = 0
        self.yclick = 0
        self.bside = 50
        self.dc = fv.get_draw_classes()
        canvas = self.dc.DrawingCanvas()
        canvas.name = 'nires-canvas'
        canvas.add_callback('cursor-down', self.btndown)
        canvas.set_surface(self.fitsimage)
        self.canvas = canvas

        self.sqbx = self.dc.Rectangle(0, 0, self.bside, self.bside,
                                      color=self.sqcolor)

        self.canvas.add(self.sqbx, redraw=False)


    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)

        box, sw, orientation = Widgets.get_oriented_box(container)
        box.set_border_width(4)
        box.set_spacing(2)


        paned = Widgets.Splitter(orientation=orientation)

        self.fwhm_plot = plots.FWHMPlot(logger=self.logger,
                                        width=400, height=400)

        if plots.MPL_GE_2_0:
            kwargs = {'facecolor': 'white'}
        else:
            kwargs = {'axisbg': 'white'}
        ax = self.fwhm_plot.add_axis(**kwargs)
        ax.grid(True)
        w = Plot.PlotWidget(self.fwhm_plot)
        w.resize(400, 400)
        paned.add_widget(Widgets.hadjust(w, orientation))


        captions = (("Load a Nires Image", 'label', "Load", 'button'),
                   ("Load an image and sky", 'label', "Load with sky", 'button'),
                   ('Object_X', 'label', 'Object_X', 'llabel'),
                   ('Object_Y', 'label', 'Object_Y', 'llabel'),
                   ('Box Size (50): ', 'label', 'Box Size', 'entry',
                    "Resize", 'button')
                   )


        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        self.wdetail = b

        b.load.add_callback('activated', lambda w: self.load_cb())

        b.load_with_sky.add_callback('activated', lambda w: self.load_with_sky_cb())

        b.box_size.add_callback('activated', lambda w: self.boxsize_cb())

        b.resize.add_callback('activated', lambda w: self.resize_cb())

        fr = Widgets.Frame("Pick Target Star")
        fr.set_widget(w)
        box.add_widget(fr, stretch=0)
        paned.add_widget(sw)

        paned.set_sizes([400, 500])

        top.add_widget(paned, stretch=5)

        btns = Widgets.HBox()
        btns.set_spacing(3)

        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        container.add_widget(top, stretch=1)
        self.mfilesel = FileSelection(self.fv.w.root.get_widget())

    def close(self):
        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        # start crosshair operation
        p_canvas = self.fitsimage.get_canvas()
        if not p_canvas.has_object(self.canvas):
            p_canvas.add(self.canvas, tag=self.layertag)

        self.resume()

    def pause(self):
        self.canvas.ui_set_active(False)

    def resume(self):
        self.canvas.ui_set_active(True)
        self.fv.show_status("Click to print")

    def stop(self):
        #remove the canvas from the image
        p_canvas = self.fitsimage.get_canvas()
        try:
            p_canvas.delete_object_by_tag(self.layertag)
        except Exception:
            pass
        self.canvas.ui_set_active(False)
        self.fv.show_status("")

    def redo(self):
        pass


    def cutdetail(self, image, shape_obj):
        view, mask = image.get_shape_view(shape_obj)

        data = image._slice(view)

        y1, y2 = view[0].start, view[0].stop
        x1, x2 = view[1].start, view[1].stop

        # mask non-containing members
        mdata = np.ma.array(data, mask=np.logical_not(mask))
        return (x1, y1, x2, y2, mdata)

    def findstar(self):
        image = self.fitsimage.get_image()
        obj = self.sqbx
        shape = obj
        x1, y1, x2, y2, data = self.cutdetail(image, shape) 
        ht, wd = data.shape[:2]
        xc, yc = wd // 2, ht // 2
        radius = min(xc, yc)
        peaks = [(xc, yc)]
        peaks = self.iqcalc.find_bright_peaks(data,
                                              threshold=None,
                                              radius=radius)

        xc, yc = peaks[0]
        xc += 1
        yc += 1
        return(xc, yc, radius, data)


    def movebox(self, viewer):
        self.sqbx.move_to(self.xclick, self.yclick)
        self.canvas.update_canvas(whence=3) 
        image = self.fitsimage.get_image()
        x1, y1, x2, y2 = self.sqbx.get_llur()
        xc, yc, radius, boxdata = self.findstar()
        xc += x1
        yc += y1

        self.wdetail.object_x.set_text('%.3f' % (xc))
        self.wdetail.object_y.set_text('%.3f' % (yc))

        self.fwhm_plot.plot_fwhm(xc, yc, radius, image,
                                 cutout_data=boxdata,
                                 iqcalc=self.iqcalc,
                                 fwhm_method='gaussian')


    def btndown(self, canvas, event, data_x, data_y):
        self.xclick = data_x
        self.yclick = data_y        
        self.movebox(self.fitsimage)
        
    def skysub(self):
        firstdat = self.niimage.get_data()
        seconddat = self.nisky.get_data()
        finaldat = firstdat - seconddat
        final_image = dp.make_image(finaldat, self.niimage, {}, pfx='subtracted')
        name = dp.get_image_name(final_image)
        self.fv.add_image(name, final_image, chname='Image')


    def load_cb(self):
        self.mfilesel.popup('Image', self.loadimage,
                            initialdir='.', filename='fits files (*.fits)')


    def load_with_sky_cb(self):
        self.mfilesel.popup('Image', self.loadimage,
                            initialdir='.', filename='fits files (*.fits)')        

        self.mfilesel.popup('Sky', self.loadsky,
                            initialdir='.', filename='fits files (*.fits)')

    def boxsize_cb(self):
        self.canvas.deleteAllObjects()
        self.bside = float(self.w.box_size.get_text())
        x1 = self.xclick - (self.bside / 2)
        x2 = self.xclick + (self.bside / 2)
        y1 = self.yclick - (self.bside / 2)
        y2 = self.yclick + (self.bside / 2)

        self.sqbx = self.dc.Rectangle(x1, y1, x2, y2,
                                      color=self.sqcolor)
        self.canvas.add(self.sqbx, redraw=True)
        self.canvas.update_canvas(whence=3)
       
    def resize_cb(self):
        self.boxsize_cb()


    def loadimage(self, filename):
        self.niimage = self.fv.load_file(filename, chname='image')
        print("loading...")
        return True


    def loadsky(self, filename):
        self.nisky = self.fv.load_file(filename, chname='Sky')
        self.skysub()
        return True

    def __str__(self):
        return 'nirestest'

# END

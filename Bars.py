#
# Bars.py -- Currently testing overlaying bars
#
#
import numpy
from ginga import GingaPlugin, RGBImage, colors
from ginga.gw import Widgets
from ginga.misc import ParamSet, Bunch
from ginga.util import dp

class Bars(GingaPlugin.LocalPlugin):
    """
    Currently testing overlaying bars.  Type in the pixel values for each bar.
    """

    def __init__(self, fv, fitsimage):
        super(Bars, self).__init__(fv, fitsimage)

        self.layertag = 'bars-canvas'

        self.dc = fv.get_draw_classes()
        canvas = self.dc.DrawingCanvas()
        canvas.enable_draw(False)
        canvas.set_surface(self.fitsimage)
        self.canvas = canvas

        self.colornames = colors.get_colors()
        self.fll = 0.0
	self.frl = 0.0
        self.canvas_img = None

    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)

        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)

        fr = Widgets.Frame("Bar Input")

        captions = (('From Left Length:', 'label', 'Fll', 'entry'),
		    ('From Right Length:', 'label', 'Frl', 'entry'),
		    ('Overlay', 'button'),
		    ('Clear', 'button'))
	
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        b.fll.set_text(str(self.fll))
	b.frl.set_text(str(self.frl))
	b.fll.add_callback('activated',
	    		       lambda w: self.overlaybars())
        b.frl.add_callback('activated',
                               lambda w: self.overlaybars())
	b.overlay.add_callback('activated',
			       lambda w: self.overlaybars())

        b.clear.add_callback('activated', lambda w: self.clear_canvas())
	fr.set_widget(w)
        vbox.add_widget(fr, stretch=0)

        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        top.add_widget(sw, stretch=1)

        btns = Widgets.HBox()
        btns.set_spacing(3)

        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btn = Widgets.Button("Help")
        btn.add_callback('activated', lambda w: self.help())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        container.add_widget(top, stretch=1)

    def help(self):
        name = str(self).capitalize()
        self.fv.help_text(name, self.__doc__, text_kind='rst', trim_pfx=4)

    def close(self):
        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        # start ruler drawing operation
        p_canvas = self.fitsimage.get_canvas()
        try:
            obj = p_canvas.get_object_by_tag(self.layertag)

        except KeyError:
            # Add ruler layer
            p_canvas.add(self.canvas, tag=self.layertag)

        self.resume()

    def pause(self):
        self.canvas.ui_setActive(False)

    def resume(self):
        self.canvas.ui_setActive(True)
        self.fv.show_status("Enter a value for bar length")

    def stop(self):
        self.arrsize = None
        self.rgbobj.set_data(self.rgbarr)

        # remove the canvas from the image
        p_canvas = self.fitsimage.get_canvas()
        try:
            p_canvas.delete_object_by_tag(self.layertag)
        except:
            pass
        #self.canvas.ui_setActive(False)
        self.fv.show_status("")

    def redo(self):
	pass

    def overlaybars(self):
	fromleft = float(self.w.fll.get_text())
	fromright = float(self.w.frl.get_text())
	self.canvas.add(self.dc.Rectangle(3076, 1000, fromleft, 1100))
	self.canvas.add(self.dc.Rectangle(0, 1000, fromright, 1100))	
    def clear_canvas(self):
        self.canvas.delete_all_objects()

    def __str__(self):
        return 'bars'

#END

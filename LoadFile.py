"""
Test plugin that load image from computer
"""


# Local application imports
from ginga import GingaPlugin
from ginga.gw import Widgets

# import any other modules you want here--it's a python world!

class LoadFile(GingaPlugin.LocalPlugin):

    def __init__(self, fv, fitsimage):
        super(LoadFile, self).__init__(fv, fitsimage)
	self.image = ''

    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)
	self.msg_font = self.fv.get_font("Courier", 12)
        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)
        

	fr = Widgets.Frame("Load an image")
        vbox2 = Widgets.VBox()
        

	captions = (("Path to file:", 'label', 'Image', 'entry'),
                    ("Load", 'button'),
                    )   
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w = b 

#setup for entry callback 
	b.image.set_text(str(self.image))
        b.image.add_callback('activated', lambda w: self.loadimg())
        b.image.set_tooltip("Path to image")
#load button callback
        b.load.add_callback('activated',
                                   lambda w: self.loadimg())



        vbox2.add_widget(w, stretch=0)

        fr.set_widget(vbox2)
        vbox.add_widget(fr, stretch=0)

	
        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        top.add_widget(sw, stretch=1)

        btns = Widgets.HBox()
        btns.set_spacing(3)

        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        container.add_widget(top, stretch=1)

#load image function

    def loadimg(self):
	image = self.w.image.get_text()
	self.fv.load_file(image)


    def close(self):

        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        
	self.resume()

    def pause(self):
        
	pass

    def resume(self):
        
	pass

    def stop(self):
        
	pass

    def redo(self):
        
	pass
 
    def __str__(self):
        
	return 'loadfile'

"""
Test plugin that loads 2 images and allows you to add or subtract them.
"""

import numpy as np
from ginga.BaseImage import BaseImage
from ginga import GingaPlugin
from ginga.gw import Widgets
from ginga import AstroImage, colors
from ginga.RGBImage import RGBImage
from ginga.util import dp


class ImageMath(GingaPlugin.LocalPlugin):

    def __init__(self, fv, fitsimage):
        super(ImageMath, self).__init__(fv, fitsimage)
	self.first = ''
	self.second = ''

    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)
	self.msg_font = self.fv.get_font("Courier", 12)
        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)
#Gui        

	fr = Widgets.Frame("Add or Subtract Two Images")
        vbox2 = Widgets.VBox()
        

	captions = (("Path to file 1:", 'label', 'First', 'entry'),
		    ("Path to file 2:", 'label', 'Second', 'entry'),
		    ("Add", 'button', "Subtract", 'button'),
                    )
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w = b 
#Function callbacks
	b.first.set_text(str(self.first))
        b.first.add_callback('activated',
                                   lambda w: self.addimg())
        b.second.set_text(str(self.second))
	b.second.add_callback('activated',
                                   lambda w: self.addimg())	
        
	b.add.add_callback('activated',
                                   lambda w: self.addimg())
        b.first.add_callback('activated',
                                   lambda w: self.subimg())
        b.second.add_callback('activated',
                                   lambda w: self.subimg())     
        b.subtract.add_callback('activated',
                                   lambda w: self.subimg())

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
#Add and Subtract functions


    def addimg(self):
	
	first = self.fv.load_file(self.w.first.get_text(), chname = '1')
	second = self.fv.load_file(self.w.second.get_text(), chname = '2')
	firstdat = first.get_data()
	seconddat = second.get_data()
	finaldat = firstdat + seconddat
	final_image = dp.make_image(finaldat, first, {}, pfx='added')
	name = dp.get_image_name(final_image)
	self.fv.add_image(name, final_image, chname='3')
	

    def subimg(self):
        first = self.fv.load_file(self.w.first.get_text(), chname = '1')
        second = self.fv.load_file(self.w.second.get_text(), chname = '2')
        firstdat = first.get_data()
        seconddat = second.get_data()
        finaldat = firstdat - seconddat
        final_image = dp.make_image(finaldat, first, {}, pfx='subtracted')
        name = dp.get_image_name(final_image)
        self.fv.add_image(name, final_image, chname='4')


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
        
	return 'imagemath'

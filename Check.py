"""
Plugin to check how many images are loaded.
Test run for plugins.

"""
import numpy
import time
from ginga import GingaPlugin
from ginga.gw import Widgets


class Check(GingaPlugin.LocalPlugin):

    def __init__(self, *args):
        """
        """
        super(Check, self).__init__(*args)
	
	self.hist_w = None
	self.histlimit = 5000
	


    def build_gui(self, container):
        


	#main gui setup
	top = Widgets.VBox()
        top.set_border_width(4)
	self.msg_font = self.fv.get_font("Courier", 12)
        
	vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)
        
	fr = Widgets.Frame("See how many images are open")
        vbox2 = Widgets.VBox()
        #out put area
	vbox.add_widget(Widgets.Label("Output:"))
        tw = Widgets.TextArea(wrap=True, editable=False)
        tw.set_font(self.msg_font)
        tw.set_limit(self.histlimit)
	self.hist_w = tw

	vbox.add_widget(tw, stretch=1)
	
	#button
	captions = (("Check", 'button'),
                    )   
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w = b 

	#callback to make button do something
        b.check.add_callback('activated',
                                   lambda w: self.checkimg())


	#other gui stuff
        vbox2.add_widget(w, stretch=0)

        fr.set_widget(vbox2)
        vbox.add_widget(fr, stretch=0)

	

        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        top.add_widget(sw, stretch=1)

        # A button box that is always visible at the bottom
        btns = Widgets.HBox()
        btns.set_spacing(3)

        # Add a close button for the convenience of the user
        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        # Add our GUI to the container
        container.add_widget(top, stretch=1)

#Funcion that check images
    def checkimg(self):
	if len(self.channel) == 0:
		self.log("No images open")
	elif len(self.channel) == 1:
		self.log("There is 1 image open.")
	else:
		self.log("There are %d images open!" % len(self.channel))


#Function for outputting result of checkimg()
    def log(self, text, w_time=False):
        if self.hist_w is not None:
            pfx = ''
            if w_time:
                pfx = time.strftime("%H:%M:%S", time.localtime()) + ": "
            self.fv.gui_do(self.hist_w.append_text, pfx + text + '\n',
                           autoscroll=True)


#All the other stuff that goes in every plugin
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
        
	return 'mytestplugin'

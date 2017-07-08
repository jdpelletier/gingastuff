#
# KeckMosaic.py -- Pending
#
#
import re
import os
import numpy as np
import math
from ginga import GingaPlugin, RGBImage, colors
from ginga.gw import Widgets
from ginga.gw.GwHelp import FileSelection
from ginga.util import wcs, io_fits, dp
from astropy.io import fits

class KeckMosaic(GingaPlugin.LocalPlugin):
    """
    MultiBars
    =========
    Plugin Type: Local
    ------------------
    TVMask is a local plugin, which means it is associated with a
    channel.  An instance can be opened for each channel.

    Usage
    -----
    This plugin adds cartoon bars with expected positions over
    and image of the MOSFIRE CSU.  Click overlay to load your
    position file and have it overlay your image.
    """

    def __init__(self, fv, fitsimage):
        super(KeckMosaic, self).__init__(fv, fitsimage)


    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)

        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)

        fr = Widgets.Frame("Keck Mosaic")

        captions = (('Load a multi-extension FITS file, create a mosaic', 'label'),
		    ('Load', 'button'))

        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        b.load.add_callback('activated',
                               lambda w: self.load_cb())

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

        self.mfilesel = FileSelection(self.fv.w.root.get_widget())

    def help(self):
        name = str(self).capitalize()
        self.fv.help_text(name, self.__doc__, text_kind='rst', trim_pfx=4)

    def close(self):
        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def stop(self):
        pass

    def redo(self):
        pass


###BEGIN MAIN FUNCTION###

    def multimos(self, filename):
	hdulist = fits.open(filename)
	files = np.sum([1 for hdu in hdulist if type(hdu) in
                  	[fits.hdu.image.PrimaryHDU, fits.hdu.image.ImageHDU]
                  	and hdu.data is not None])
	k = 0
	j = 0
	
	ra_deg = 0.5
	dec_deg = 0.5
	fov_deg = 0.2
	header = hdulist[1].header
	(rot_deg, cdelt1, cdelt2) = wcs.get_rotation_and_scale(header, skew_threshold=1)
	px_scale = math.fabs(cdelt1)
	cdbase = [np.sign(cdelt1), np.sign(cdelt2)]

	###Sorting Images###
	imagesort = [[0 for x in range(4)] for y in range(files)]
	for i in range(1, files+1):
		imagesort[i-1][0] = hdulist[i]
  		df = hdulist[i].header['DETSEC']
        	cpos = df.index(':')
        	epos = df.index(',')
        	dflow = ''.join(df[1:cpos])
        	dflow = int(dflow)
        	dfhigh = ''.join (df[cpos+1:epos])
        	dfhigh = int(dfhigh)
        	imagesort[i-1][1] = dflow + dfhigh
		ncpos = df.index(':', cpos+1)
		nepos = df.index(']')
		yflow = ''.join(df[epos+1:ncpos])
		yflow = int(yflow)
		yhigh = ''.join(df[ncpos+1:nepos])
		yhigh = int(yhigh)
		imagesort[i-1][2] = yflow + yhigh
		ccd = hdulist[i].header['CCDNAME']
		imagesort[i-1][3] = ccd

	sortedim = sorted(imagesort, key=lambda x: x[1])

	###Putting images together###

	#2D#

	if sortedim[0][1] == sortedim[1][1]:
		for i in range(1, files+1):
			dr = sortedim[i-1][0].header['DATASEC']
        		colpos = dr.index(':')
        		endpos = dr.index(',')
       			drlow = ''.join(dr[1:colpos])
        		drlow = int(drlow)
        		drhigh = ''.join (dr[colpos+1:endpos])
        		drhigh = int(drhigh)
        		imdata = sortedim[i-1][0].data[:, drlow:drhigh]
        		gapxdim = np.size(imdata, 0)
        		gapx = np.zeros((gapxdim, 30))
			gapx[:,:] = np.nan
			gapydim = np.size(imdata, 1) + 30
			gapy = np.zeros((20, gapydim))
			gapy[:,:] = np.nan
			fgapy = np.zeros((20, gapydim - 30))
			fgapy[:,:] = np.nan
        		#image flips#
        		df = sortedim[i-1][0].header['DETSEC']
        		cpos = df.index(':')
        		epos = df.index(',')
        		dflow = ''.join(df[1:cpos])
        		dflow = int(dflow)
        		dfhigh = ''.join (df[cpos+1:epos])
        		dfhigh = int(dfhigh)
        		ncpos = df.index(':', cpos+1)
        		nepos = df.index(']')
        		yflow = ''.join(df[epos+1:ncpos])
        		yflow = int(yflow)
        		yhigh = ''.join(df[ncpos+1:nepos])
        		yhigh = int(yhigh)
	        	if dflow > dfhigh:
                		findatx = np.fliplr(imdata)
        		else:
                		findatx = imdata

        		if yflow > yhigh:
                		findat = np.flipud(findatx)
        		else:
                		findat = findatx
			fm = files - 1
			if i != files:
				if i != fm:
					if sortedim[i-1][3] != sortedim[i][3]:
						findat = np.column_stack((findat, gapx))
	
			if i == 1:
				vert = findat
		
			elif sortedim[i-1][1] == sortedim[i-2][1]:
				if sortedim[i-1][2] > sortedim[i-2][2]:
					if i == files:
						vert = np.vstack((vert, fgapy))
                                        	vert = np.vstack((vert, findat))
                                        	if i == files:
                                                	final = np.column_stack((final, vert))	
					else:
						vert = np.vstack((vert, gapy))
						vert = np.vstack((vert, findat))
						if i == files:
							final = np.column_stack((final, vert))
				else:
					findat = np.vstack((findat, gapy))
					vert = np.vstack((findat, vert))
					if i == files:
						final = np.column_stack((final, vert))
			
			else:
				k = k+1
				if k == 1:
					final = vert
					vert = findat
				else:
					final = np.column_stack((final, vert))
					vert = findat
				


	else:
	#1d#
		for i in range(1, files+1):
			#data ranges#
			dr = sortedim[i-1][0].header['DATASEC']
			colpos = dr.index(':')
			endpos = dr.index(',')
			drlow = ''.join(dr[1:colpos])
			drlow = int(drlow)
			drhigh = ''.join (dr[colpos+1:endpos])
			drhigh = int(drhigh)
			imdata = sortedim[i-1][0].data[:, drlow:drhigh]
			gapxdim = np.size(imdata, 0)
			gapx = np.zeros((gapxdim, 30))
			gapx[:,:] = np.nan
			#image flips#
			df = sortedim[i-1][0].header['DETSEC']
			cpos = df.index(':')
			epos = df.index(',')
			dflow = ''.join(df[1:cpos])
			dflow = int(dflow)
			dfhigh = ''.join (df[cpos+1:epos])
			dfhigh = int(dfhigh)
			ncpos = df.index(':', cpos+1)
        		nepos = df.index(']')
       			yflow = ''.join(df[epos+1:ncpos])
        		yflow = int(yflow)
        		yhigh = ''.join(df[ncpos+1:nepos])
        		yhigh = int(yhigh)
	
			if dflow > dfhigh:
				findatx = np.fliplr(imdata)
			else:
				findatx = imdata

			if yflow > yhigh:
				findat = np.flipud(findatx)
			else:
				findat = findatx
			#final image
			if i == 1:
				final = findat
			else:
				final = np.append(final, findat, axis=1)
		
			if i != files and sortedim[i-1][3] != sortedim[i][3]:
				final = np.append(final, gapx, axis=1)



	#finalimage#
	#plt.imshow(final)
	#plt.show()
	#finalimage = fits.ImageHDU()
	#finalimage.data = final
	oldim = dp.create_blank_image(ra_deg, dec_deg,
                                      fov_deg, px_scale, rot_deg,
                                      cdbase=cdbase,
                                      logger=None)
	finalimage = dp.make_image(final, oldim, {}, pfx='mosaic')
	name = dp.get_image_name(finalimage)
        self.fv.add_image(name, finalimage, chname='Mosaic')
	#finalimage.writeto('mosaic.fits', clobber=True)

###END MAIN FUNCTION###



#####LOADING FILE#######

    def load_cb(self):
        self.mfilesel.popup('Load fits file', self.multimos,
                            initialdir='.', filename='FITS files (*.fits)')



    def __str__(self):
        return 'keckmosaic'

#END

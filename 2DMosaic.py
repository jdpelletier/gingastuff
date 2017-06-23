from astropy.io import fits
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

hdulist = fits.open(argv[1])
files = np.sum([1 for hdu in hdulist if type(hdu) in
                  [fits.hdu.image.PrimaryHDU, fits.hdu.image.ImageHDU]
                  and hdu.data is not None])
k = 0
j = 0


###Sorting Images###
imagesort = [[0 for x in range(3)] for y in range(files)]
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
        	gapx = np.zeros((gapxdim, 20))
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
	
		if i == 1:
			vert = findat
		
		elif sortedim[i-1][1] == sortedim[i-2][1]:
			if sortedim[i-1][2] > sortedim[i-2][2]:
				vert = np.vstack((vert, findat))
				if i == files:
					final = np.column_stack((final, vert))
			else:
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
		gapx = np.zeros((gapxdim, 20))
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
			#final = np.append(final, gapx, axis=1)
		else:
			final = np.append(final, findat, axis=1)
			#final = np.append(final, gapx, axis=1)
		

#TODO GAPS#
#gapydim = np.size(final, 1)
#gapy = np.zeros((30, gapydim))
#final = np.vstack((final, gapy))


#finalimage#
plt.imshow(final)
plt.show()
finalimage = fits.ImageHDU()
finalimage.data = final
finalimage.writeto('mosaic.fits', clobber=True)

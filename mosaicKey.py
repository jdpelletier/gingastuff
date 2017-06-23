from astropy.io import fits
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

hdulist = fits.open(argv[1])
files = np.sum([1 for hdu in hdulist if type(hdu) in
                  [fits.hdu.image.PrimaryHDU, fits.hdu.image.ImageHDU]
                  and hdu.data is not None])

###Sorting Images###
imagesort = [[0 for x in range(2)] for y in range(files)]
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

sortedim = sorted(imagesort, key=lambda x: x[1])
	
###Putting images together###

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
	if dflow > dfhigh:
		findat = np.fliplr(imdata)
	else:
		findat = imdata
	#final image
	if i == 1:
		final = findat
		final = np.append(final, gapx, axis=1)
	else:
		final = np.append(final, findat, axis=1)
		final = np.append(final, gapx, axis=1)

gapydim = np.size(final, 1)
gapy = np.zeros((30, gapydim))
final = np.vstack((final, gapy))


#finalimage#
plt.imshow(final)
plt.show()
finalimage = fits.ImageHDU()
finalimage.data = final
finalimage.writeto('mosaic.fits', clobber=True)

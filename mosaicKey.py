from astropy.io import fits
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

hdulist = fits.open(argv[1])
files = int(argv[2])
for i in range(1, files+1):
	#data ranges#
	dr = hdulist[i].header['DATASEC']
	colpos = dr.index(':')
	endpos = dr.index(',')
	drlow = ''.join(dr[1:colpos])
	drlow = int(drlow)
	drhigh = ''.join (dr[colpos+1:endpos])
	drhigh = int(drhigh)
	imdata = hdulist[i].data[:, drlow:drhigh]
	#image flips#
	df = hdulist[i].header['DETSEC']
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
	else:
		final = np.append(final, findat, axis=1)

#finalimage#
plt.imshow(final)
plt.show()
#finalimage = fits.ImageHDU()
#finalimage.data = final
#finalimage.writeto('mosaic.fits', clobber=True)

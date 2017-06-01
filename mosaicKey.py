from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

hdulist = fits.open('hires0201.fits')

#sort images#
ds = hdulist[1].header['DETSEC']
ds = ''.join(ds[1:5])
ds = int(ds)

 
ds2 = hdulist[2].header['DETSEC']
ds2 = ''.join(ds2[1:5])
ds2 = int(ds2)

ds3 = hdulist[3].header['DETSEC']
ds3 = ''.join(ds3[1:5])
ds3 = int(ds3)

if ds > ds2 and ds > ds3:
	image3 = hdulist[1]
elif ds > ds2 and ds < ds3:
	image2 = hdulist[1]
else:
	image1 = hdulist[1]

if ds2 > ds and ds2 > ds3:
	image3 = hdulist[2]
elif ds2 > ds and ds2 < ds3:
        image2 = hdulist[2]
else:
        image1 = hdulist[2]

if ds3 > ds and ds3 > ds2:
        image3 = hdulist[3]
elif ds3 > ds and ds3 < d2:
        image2 = hdulist[3]
else:
        image1 = hdulist[3]

#firstimage#
olddat = image1.data
olddat = olddat[0:4096, 6:1030]
placehold = np.zeros((4096, 2048))
bigold = np.append(olddat, placehold, axis=1)

#secondimage#
olddat2 = image2.data
olddat2 = olddat2[0:4096, 6:1030]
placehold2 = np.zeros((4096, 1024))
bigold2temp = np.append(placehold2, olddat2, axis=1)
bigold2 = np.append(bigold2temp, placehold2, axis=1)

#thirdimage#
olddat3 = image3.data
olddat3 = olddat3[0:4096, 6:1030]
bigold3 = np.append(placehold, olddat3, axis=1)

#finalimage#
final = bigold + bigold2 + bigold3
finalimage = fits.ImageHDU()
finalimage.data = final
finalimage.writeto('hires_mosaic.fits', clobber=True)

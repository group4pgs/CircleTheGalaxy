"""
File where we work
"""

import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from circles_found import *	#User-defined Library


filename = 'NGA_NGC3351-fd-int.fits'
image = fits.open(filename)[0].data
print("Image Read.\nShape of FITS = ",image.shape)

circles = listCircles1(image)

if circles is not None:
	circles = np.round(circles[0, :]).astype("int")
	for (x, y, r) in circles:
		if r<60:
			print("Radius = ",r,'x,y = ',x,',',y)
			cv2.circle(image, (x, y), r, (0, 255, 255), 1)
else:
	print("No circles found")

plt.imshow(image,cmap='gray',norm=LogNorm())
plt.show()

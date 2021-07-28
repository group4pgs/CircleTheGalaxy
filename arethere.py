import numpy as np
from astropy.io import fits
import cv2

NGC3351_fd = fits.open('NGA_NGC3351-fd-int.fits')
image = NGC3351_fd[0].data

for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		if image[i][j]>0.1:
			image[i][j] = image[i][j]*10000

cv2.imwrite('enhanced5.jpg',image)

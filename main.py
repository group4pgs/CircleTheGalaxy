import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm
from circle_detect import *
from chord_finder import *
from enhance_image import *
import cv2


filename = 'NGA_NGC3351-fd-int.fits'
NGC3351_fd = fits.open(filename)
image = NGC3351_fd[0].data
print("Full-frame: ",image.shape)

en_image = basic_enhance(image)
data = slicer(en_image)
print("Sliced-frame: ",data.shape)

circles = listCircles(data.copy())
print("\nTentative Circle")
if circles is not None:
	circles = np.round(circles[0, :]).astype("int")
	for (x, y, r) in circles:
		if r<60:
			print("Radius = ",r,'x,y = ',x,',',y)
			cv2.circle(data, (x, y), 2, (255, 0, 0), -1)


diameter = find_chords(data)
print("\n\nDiameter of the Circle found: ",diameter)
plt.imshow(data,cmap='gray',norm=LogNorm())
plt.show()

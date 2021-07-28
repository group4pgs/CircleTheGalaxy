import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm
from distance_calc import *

def basic_enhance(image):
	image = image*150
	return image.astype(np.uint8)

def slicer(data):
	M,N = data.shape[0]//9,data.shape[1]//9
	tiles = [data[x:x+M,y:y+N] for x in range(0,data.shape[0],M) for y in range(0,data.shape[1],N)]
	data,high =[[]],0
	for cropped in tiles:
		if cropped.mean()>high:
			data = cropped.copy()
			high = cropped.mean()

	return data


filename = 'NGA_NGC3351-fd-int.fits'
NGC3351_fd = fits.open(filename)
image = NGC3351_fd[0].data
print("Full-frame: ",image.shape)

en_image = basic_enhance(image)
data = slicer(en_image)
print("Sliced-frame: ",data.shape)



chords = chord_finder(data)
print(chords)
plt.imshow(data,cmap='gray',norm=LogNorm())
plt.show()




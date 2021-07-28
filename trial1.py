import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm

NGC3351_fd = fits.open('NGA_NGC3351-fd-int.fits')
image = NGC3351_fd[0].data
print("Full-frame: ",image.shape)

data = image.copy()
data = 100*data
data = data.astype(np.uint8)
M,N = data.shape[0]//9,data.shape[1]//9
tiles = [data[x:x+M,y:y+N] for x in range(0,data.shape[0],M) for y in range(0,data.shape[1],N)]


data,high =[[]],0
for cropped in tiles:
	if cropped.mean()>high:
		data = cropped.copy()
		high = cropped.mean()

print(data.shape)

def main_method(data):
	structure = data.copy()
	max_array=structure[0]
	for array in structure:
		if sum(max_array)<sum(array):
			max_array = array

	start,stop,buffer_point=0,len(max_array),False
	for pixel in range(1,len(max_array)):
		if max_array[pixel-1]>0 and buffer_point==True and max_array[pixel]>0:
			start=pixel
		elif max_array[pixel-1]==0 and buffer_point!=True and max_array[pixel]>0:
			buffer_point=True
		if buffer_point==True and max_array[pixel+1]==0:
			buffer_point=False
			break
	#print(start)
	max_array = max_array[::-1]
	pixel=0
	for pixel in range(1,len(max_array)):
		if max_array[pixel-1]>0 and buffer_point==True and max_array[pixel]>0:
			stop=pixel
		elif max_array[pixel-1]==0 and buffer_point!=True and max_array[pixel]>0:
			buffer_point=True
		if buffer_point==True and max_array[pixel+1]==0:
			buffer_point=False
			break
	
	#print(stop)
	
	print("\n\nDiameter = ",np.abs(stop-start))
	
	print("Chosen strip = \n",max_array)

main_method(data)


plt.imshow(data,cmap='gray',norm=LogNorm())
plt.show()

import numpy as np

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


#From trial2 of alpha2

import numpy as np

def find_chords(structure):
	n=0
	max_array=structure[0]
	for array in structure:
		if sum(max_array)<sum(array):
			max_array = array
			#print(n)
		n = n+1
	#print(max_array)
	start,stop,buffer_point=0,len(max_array),False
	for pixel in range(1,len(max_array)-1):
		"""
		if max_array[pixel-1]>0 and buffer_point==True and max_array[pixel]>0:
			start=pixel
		elif max_array[pixel-1]==0 and buffer_point!=True and max_array[pixel]>0:
			buffer_point=True
		if buffer_point==True and max_array[pixel+1]==0:
			buffer_point=False
			break
		"""	
		if max_array[pixel-1]>0 and max_array[pixel]>0 and max_array[pixel+1]==0:
			start = pixel
			break
		
		
		
		
		
	#print(start)
	max_array = max_array[::-1]
	pixel=0
	
	for pixel in range(1,len(max_array)-1):
		"""
		if max_array[pixel-1]>0 and buffer_point==True and max_array[pixel]>0:
			stop=pixel
		elif max_array[pixel-1]==0 and buffer_point!=True and max_array[pixel]>0:
			buffer_point=True
		if buffer_point==True and max_array[pixel+1]==0:
			buffer_point=False
			break
		"""
		
		if max_array[pixel-1]>0 and max_array[pixel]>0 and max_array[pixel+1]==0:
			stop = len(max_array)-pixel
			break
	#print(stop)
	return np.abs(stop-start)
	

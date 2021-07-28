import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def chord_finder_peaks(data):
	chord_lengths = []
	for row in data:
		peaks,_ = find_peaks(row,height=4)
		if len(peaks)>1:
			#plt.plot(np.arange(len(peaks)),row[peaks])
			print(peaks)
		
			
		
	
	#plt.show()
	return chord_lengths
	
def chord_finder(data):
	stops,chord_lengths = [],[]
	has_points={}
	flag,flagp,start,stop=False,False,0,0
	flag = True if data[0][0]>2 else False
	flagp = flag
	for i in range(data.shape[0]):
		for position in range(len(data[i])):
			if flag!=True and flagp!=True and data[i][position]>2:
				flag = True
			elif flag==True and flagp!=True and data[i][position]>2:
				flagp,flag = True,True
			elif flag==True and flagp==True and data[i][position]<2:
				start = position
				has_points[i]=start
				flagp,flag=False,False
				continue
			else:
				flag=flag
	#print(has_points) 	
	flagp,flag,position=False,False,0
	for row in has_points.keys():
		for position in range(len(data[row])-1,0,-1):
			if flag!=True and flagp!=True and data[row][position]>2:
				flag = True
			elif flag==True and flagp!=True and data[row][position]>2:
				flagp,flag = True,True
			elif flag==True and flagp==True and data[row][position]<2:
				print(row)
				chord_lengths.append(has_points[row]-position)
				flagp,flag=False,False
				continue
			else:
				flag=flag

	return chord_lengths

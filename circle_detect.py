import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def listCircles(image):
	
	
	#Edge-Detect
	image = cv2.Canny(image,2,1)
	
	#HOUGH CIRCLES
	circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 6, 1500, param1=10, param2=1, maxRadius=100)
	#print(circles)
	#plt.imshow(image,cmap='gray',norm=LogNorm())
	#plt.show()
	print("Done with processing")
	return circles

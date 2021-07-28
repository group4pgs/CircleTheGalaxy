import numpy as np
import cv2
from astropy.io import fits

path = "NGA_NGC3351-fd-int.fits"
image = fits.open(path)[0].data
output = image.copy()
output = cv2.convertScaleAbs(output, alpha=(255.0))
#output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
output = cv2.blur(output,(1,1))

print(output.shape)
circles = cv2.HoughCircles(output, cv2.HOUGH_GRADIENT, 0.1, 2)
#circles = np.uint16(np.around(circles))
#if circles is not None:
#	circles = np.round(circles[0, :]).astype("int")
#	for (x, y, r) in circles:
#		cv2.circle(image, (x, y), r, (0, 255, 255), 4)
#else:
#	print("Nothing available")
print(output)
#cv2.imshow("sample",image)
#cv2.waitKey(0)
cv2.imwrite("fitsTrial.jpg")

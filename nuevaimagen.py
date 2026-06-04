import cv2 as cv 
import numpy as np 

img = np.ones((400, 400 ) ,  np.uint8 ) * 150
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()
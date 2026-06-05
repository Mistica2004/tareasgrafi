import cv2
import numpy as np

img = cv2.imread("qr_rotado.jpg")

h, w = img.shape[:2]

center = (w // 2, h // 2)

M = cv2.getRotationMatrix2D(center, -45, 1.0)

result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("Rotacion OpenCV", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

img = cv2.imread("vehiculo.jpg")

h, w = img.shape[:2]

# Matriz de traslación
M = np.float32([
    [1, 0, 300],
    [0, 1, 200]
])

result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("OpenCV Translation", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
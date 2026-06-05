import cv2
import numpy as np

img = cv2.imread("vehiculo.jpg")

h, w = img.shape[:2]

# Lienzo negro
canvas = np.zeros((h, w, 3), dtype=np.uint8)

dx = 300
dy = 200

# Traslación manual
for y in range(h):
    for x in range(w):
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < w and 0 <= new_y < h:
            canvas[new_y, new_x] = img[y, x]

cv2.imshow("Raw Translation", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

img = cv2.imread("microfilm.jpg")

# Recorte central (ajusta si es necesario)
recorte = img[900:1100, 900:1100]

h, w = recorte.shape[:2]

scale = 5
new_h, new_w = h * scale, w * scale

canvas = np.zeros((new_h, new_w, 3), dtype=np.uint8)

for y in range(new_h):
    for x in range(new_w):

        src_x = x // scale
        src_y = y // scale

        canvas[y, x] = recorte[src_y, src_x]

cv2.imshow("Escalado RAW", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np
import math
img = np.zeros((500, 500, 3), dtype=np.uint8)
t = 0.0
step = 0.01
a = 3
b = 2
while t <= 2 * math.pi:
    # ecuaciones paramétricas
    x = int(250 + 150 * math.sin(a * t))
    y = int(250 + 150 * math.cos(b * t))
    # dibujar punto
    cv2.circle(img, (x, y), 1, (255, 255, 255), -1)
    t += step
cv2.imshow("Antena Parabolica (Lissajous)", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
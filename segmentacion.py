import cv2
import numpy as np

img = cv2.imread("frutas.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Rojo bajo
lower1 = np.array([0, 100, 100])
upper1 = np.array([10, 255, 255])

# Rojo alto
lower2 = np.array([160, 100, 100])
upper2 = np.array([180, 255, 255])

mask1 = cv2.inRange(hsv, lower1, upper1)
mask2 = cv2.inRange(hsv, lower2, upper2)

mask = cv2.bitwise_or(mask1, mask2)

kernel = np.ones((5,5), np.uint8)
mask_limpia = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_limpia)

area_minima = 500
contador = 0

for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    if area > area_minima:
        contador += 1
        print("Fruta roja", contador, area)

print("Total rojas:", contador)

cv2.imshow("Mascara Roja", mask_limpia)
cv2.waitKey(0)
cv2.destroyAllWindows()

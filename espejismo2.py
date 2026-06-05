import cv2
import numpy as np
h, w = 300, 700
img = np.random.randint(0, 80, (h, w, 3), dtype=np.uint8)
text = "SECRETO-9"
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, text, (50, 150), font, 2, (30, 220, 30), 4, cv2.LINE_AA)
cv2.imwrite("m5_tricolor.png", img)
b, g, r = cv2.split(img)
b_img = b
g_img = g
r_img = r
diff = cv2.absdiff(g, b)
diff_norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
_, mask = cv2.threshold(diff_norm, 80, 255, cv2.THRESH_BINARY)
cv2.imwrite("m5_mensaje.png", mask)
cv2.imshow("Canal B", b_img)
cv2.imshow("Canal G", g_img)
cv2.imshow("Canal R", r_img)
cv2.imshow("Diferencia G-B", diff_norm)
cv2.imshow("Mensaje recuperado", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

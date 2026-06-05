import cv2

img = cv2.imread("microfilm.jpg")

recorte = img[900:1100, 900:1100]

# Escalado con interpolación avanzada
resultado = cv2.resize(
    recorte,
    None,
    fx=5,
    fy=5,
    interpolation=cv2.INTER_CUBIC
)

cv2.imshow("Escalado OpenCV", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np


img = cv2.imread("m1_oscura.png", cv2.IMREAD_GRAYSCALE)


# MODO RAW (con ciclos)


# Convertir a int32 para evitar overflow
img_int = img.astype(np.int32)

alto, ancho = img_int.shape

# Crear matrices de salida
recuperado_x50 = np.zeros((alto, ancho), dtype=np.int32)
recuperado_x50_mas20 = np.zeros((alto, ancho), dtype=np.int32)

# Paso A: multiplicar por 50
for y in range(alto):
    for x in range(ancho):
        valor = img_int[y, x] * 50
        # Saturar a 0..255
        valor = np.clip(valor, 0, 255)
        recuperado_x50[y, x] = valor

cv2.imwrite("m1_recuperado_x50.png", recuperado_x50.astype(np.uint8))

# Paso B: sumar +20
for y in range(alto):
    for x in range(ancho):
        valor = recuperado_x50[y, x] + 20
        # Saturar a 0..255
        valor = np.clip(valor, 0, 255)
        recuperado_x50_mas20[y, x] = valor

cv2.imwrite("m1_recuperado_x50_mas20.png", recuperado_x50_mas20.astype(np.uint8))



# MODO VECTORIZADO

vec_x50 = np.clip(img.astype(np.int32) * 50, 0, 255).astype(np.uint8)
cv2.imwrite("m1_recuperado_x50_vec.png", vec_x50)


vec_x50_mas20 = np.clip(vec_x50.astype(np.int32) + 20, 0, 255).astype(np.uint8)
cv2.imwrite("m1_recuperado_x50_mas20_vec.png", vec_x50_mas20)

print("Proceso completado. Imágenes guardadas.")
MISION1 
Tu Tarea
Modo Raw (Manual): Crea un lienzo negro nuevo de 600x800. Traslada los píxeles de la imagen original al lienzo nuevo utilizando la matemática pura de coordenadas (ya sea con ciclos for o "slicing" de NumPy). ¡Prohibido usar cv2.warpAffine!
Modo OpenCV: Construye la matriz de traslación  y utiliza la función optimizada cv2.warpAffine para lograr el mismo resultado.

MODO Raw
Codigo
import cv2
import numpy as np

img = cv2.imread("vehiculo.jpg")

h, w = img.shape[:2]

canvas = np.zeros((h, w, 3), dtype=np.uint8)

dx = 300
dy = 200

for y in range(h):
    for x in range(w):
        new_x = x + dx
        new_y = y + dy

        if 0 <= new_x < w and 0 <= new_y < h:
            canvas[new_y, new_x] = img[y, x]

cv2.imshow("Raw Translation", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

Resultado:
![modo raw](<modo raw.png>)

MODO OPENCV:
Codigo:
import cv2
import numpy as np

img = cv2.imread("vehiculo.jpg")

h, w = img.shape[:2]

M = np.float32([
    [1, 0, 300],
    [0, 1, 200]
])

result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("OpenCV Translation", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

Resultado:
![modo opencv](<modo opencv.png>)

¿Notaste alguna diferencia de tiempo al procesar la imagen píxel por píxel con ciclos for (Modo Raw) en comparación con la función cv2.warpAffine de OpenCV? ¿Por qué crees que tu código manual tarda mucho más en ejecutarse?

¿Por qué el código manual es más lento?

El método manual tarda más porque:

* Procesa la imagen pixel por pixel
* Usa bucles for en Python (muy lentos comparados con C++)
* No está optimizado para operaciones matriciales
* Realiza validaciones en cada iteración

En cambio, cv2.warpAffine:

* Está implementado en C/C++ optimizado
* Usa operaciones vectorizadas
* Aprovecha procesamiento a bajo nivel (SIMD)
* Evita bucles en Python


Conclusión técnica

El método manual es útil para entender cómo funciona la transformación geométrica a nivel matemático, pero no es eficiente para imágenes reales. OpenCV es significativamente más rápido porque está optimizado para procesamiento de imágenes en tiempo real.


Conclusión general

La traslación de imágenes puede implementarse de forma manual usando coordenadas o de forma optimizada con OpenCV. Aunque ambos métodos producen el mismo resultado visual, el rendimiento del método vectorizado es muy superior, lo que lo hace indispensable en aplicaciones de visión por computadora en tiempo real como robótica, satélites o realidad aumentada.

Misión 3: El Microfilm Oculto (Escalamiento)

La Historia
Encontramos un archivo de imagen gigantesco de 2000x2000 píxeles. Al inspeccionarlo de cerca, notamos que en el centro hay un texto diminuto. Los criminales encogieron la evidencia.

Las Pistas
El texto es ilegible a simple vista.
Debes extraer un recorte (crop) de la zona central y aplicar un factor de escala de 5 tanto en el eje X () como en el eje Y ().
La matemática para escalar coordenadas es simple: 

Tu Tarea
Modo Raw (Manual): Recorta una región central de la imagen (por ejemplo, de 200x200 píxeles donde está el texto). Crea un nuevo lienzo de 1000x1000 y usa la matemática para "estirar" los píxeles del recorte. (Pista: te quedará un efecto pixelado tipo "Vecino Más Cercano").
Modo OpenCV: Utiliza cv2.resize sobre ese mismo recorte usando los parámetros fx=5 y fy=5. Prueba el parámetro de interpolación cv2.INTER_CUBIC para ver cómo OpenCV suaviza los bordes mágicamente.

MODO RAW
Codigo:
import cv2
import numpy as np

img = cv2.imread("microfilm.jpg")

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

Resultado:
![modo raw](<mision3 raw.png>)


MODO OPENCV
Codigo:
import cv2

img = cv2.imread("microfilm.jpg")

recorte = img[900:1100, 900:1100]

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

Resultado:
![modo opencv](<mision3 opencv.png>)

Al comparar visualmente el texto ampliado, ¿qué diferencia notas en los bordes de las letras entre tu resultado del Modo Raw y el de OpenCV usando la interpolación cv2.INTERCUBIC? ¿De dónde crees que OpenCV saca los colores para rellenar y suavizar esos píxeles nuevos que en la imagen original no existían

¿Qué diferencia hay entre RAW y OpenCV?

Modo RAW:
* Bordes de las letras pixelados
* Apariencia “cuadriculada”
* No hay suavizado
* Cada pixel se copia directamente (vecino más cercano)

OpenCV (INTER_CUBIC):
* Bordes suaves
* Letras más legibles
* Transiciones de color graduales
* Imagen más natural


¿De dónde saca OpenCV los nuevos colores?

Usa interpolación matemática, principalmente:
* INTER_NEAREST → copia el pixel más cercano
* INTER_LINEAR → mezcla 4 píxeles vecinos
* INTER_CUBIC → usa 16 píxeles vecinos (más suave)

En el caso de INTER_CUBIC, OpenCV:
* Analiza los píxeles alrededor del punto nuevo
* Calcula una media ponderada con función cúbica
* Genera un color intermedio más realista

Conclusión
El escalamiento manual permite entender el principio básico de la ampliación de imágenes mediante el vecino más cercano, pero produce pérdida de calidad visual. En contraste, OpenCV utiliza interpolación avanzada como INTER_CUBIC para estimar valores de píxeles inexistentes mediante el análisis de vecinos, logrando imágenes más suaves y legibles. Esto es esencial en aplicaciones como visión por computadora, OCR y restauración de imágenes.


Misión 2: El Código Mareado (Rotación)

La Historia
Hemos interceptado un código QR que nos dará acceso al servidor de los sospechosos. Para evitar que lo escaneemos, lo han girado de forma extraña. Si intentamos leerlo así, nuestros escáneres fallan. ¡Necesitamos enderezarlo!

Las Pistas
El código QR está exactamente en el centro de una imagen cuadrada de 500x500 píxeles.
El análisis indica que fue rotado 45 grados en sentido antihorario. Debes girarlo en sentido horario (-45 grados o 315 grados).
Para el modo raw, la trigonometría para rotar un punto  alrededor del centro  es:   (Nota: recuerda convertir los grados a radianes con math.radians)

Tu Tarea
Modo Raw (Manual): Usa ciclos anidados para recorrer la imagen vacía de destino. Para cada píxel, calcula de qué coordenada de la imagen original proviene aplicando las fórmulas trigonométricas inversas.
Modo OpenCV: Usa cv2.getRotationMatrix2D para generar tu matriz de rotación tomando como eje el centro de la imagen (250, 250), y aplícala con cv2.warpAffine.

MODO RAW
Codigo:
import cv2
import numpy as np

img = cv2.imread("qr_rotado.jpg")

h, w = img.shape[:2]

center = (w // 2, h // 2)

M = cv2.getRotationMatrix2D(center, -45, 1.0)

result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("Rotacion OpenCV", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

Resultado:
![modo raw](mision2raw.png)

MODO OPENCV
Codigo:
import cv2
import numpy as np

img = cv2.imread("qr_rotado.jpg")

h, w = img.shape[:2]

center = (w // 2, h // 2)

M = cv2.getRotationMatrix2D(center, -45, 1.0)

result = cv2.warpAffine(img, M, (w, h))

cv2.imshow("Rotacion OpenCV", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

Resultados:
![modo opencv](<mision2 opencv.png>)

Al calcular la rotación píxel por píxel con tus fórmulas matemáticas (Modo Raw), ¿te quedaron 'puntos negros' o píxeles sin color esparcidos en la imagen resultante? ¿Cómo te imaginas que algoritmos profesionales como los de OpenCV logran rotar la imagen sin dejar esos huecos vacíos?

¿Aparecieron puntos negros en el método RAW?

Sí, al usar el método manual aparecen píxeles negros o huecos vacíos en la imagen resultante.

Esto ocurre porque:
* El mapeo es discreto (enteros)
* Algunos píxeles destino nunca reciben información
* Se pierden datos por redondeo
* No hay interpolación entre píxeles


¿Cómo lo evita OpenCV?

OpenCV evita estos huecos usando técnicas avanzadas como:
* Interpolación bilineal o bicúbica
* Re-muestreo continuo de la imagen
* Transformaciones optimizadas en C++
* Cálculo inverso de coordenadas para cada pixel destino

Esto permite que cada píxel tenga un valor asignado, incluso si no cae exactamente en una posición original.

Conclusión
La rotación manual mediante trigonometría permite comprender el fundamento matemático de las transformaciones geométricas, pero presenta limitaciones como pérdida de información y aparición de huecos. En contraste, OpenCV implementa algoritmos optimizados con interpolación que garantizan una imagen continua y de alta calidad, siendo indispensable para aplicaciones reales como visión por computadora y procesamiento en tiempo real.


Generación de un Marcador ArUco con OpenCV

Introducción

Los marcadores ArUco son patrones visuales utilizados en aplicaciones de visión por computadora y realidad aumentada para identificar posiciones y orientaciones dentro de una escena. Gracias a su diseño único, estos marcadores pueden ser detectados de forma rápida y precisa por una cámara, permitiendo el desarrollo de sistemas interactivos y aplicaciones de seguimiento en tiempo real.

Descripción

Este programa utiliza la biblioteca OpenCV para generar automáticamente un marcador ArUco y almacenarlo como una imagen en formato PNG. El código selecciona un diccionario de marcadores predefinido y crea el marcador con identificador 0, generando una imagen de alta resolución.

Posteriormente, se añade un borde blanco alrededor del marcador para mejorar su detección por parte de los algoritmos de visión artificial. Finalmente, la imagen resultante se guarda en una ubicación específica del sistema y se muestra un mensaje de confirmación indicando que el archivo fue creado correctamente.

Este tipo de marcadores es ampliamente utilizado en proyectos de realidad aumentada, robótica, seguimiento de objetos y sistemas de navegación visual.

Codigo
import cv2
import numpy as np
from pathlib import Path

OUT = Path("/Users/mistica/Desktop/marcador_aruco_id0.png")
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
if hasattr(cv2.aruco, "generateImageMarker"):
    img = cv2.aruco.generateImageMarker(dictionary, 0, 400)
else:
    img = cv2.aruco.drawMarker(dictionary, 0, 400)
border = 40
canvas = np.full((480, 480), 255, np.uint8)
canvas[40:440, 40:440] = img
cv2.imwrite(str(OUT), canvas)
print("OK ->", OUT)

Conclusión

La práctica permitió comprender el proceso de generación de marcadores ArUco mediante OpenCV y su importancia dentro de las aplicaciones de visión por computadora. Además, se observó cómo es posible crear marcadores personalizados de forma automática y prepararlos para ser utilizados en sistemas de detección, seguimiento y realidad aumentada. Este procedimiento constituye una etapa fundamental en proyectos que requieren interacción entre el mundo físico y elementos virtuales.
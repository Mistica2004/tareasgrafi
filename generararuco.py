import cv2

print("OpenCV:", cv2.__version__)
print("Tiene ArUco:", hasattr(cv2, "aruco"))

diccionario = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

marker = cv2.aruco.generateImageMarker(
    diccionario,
    0,
    400
)

ok = cv2.imwrite("aruco0.png", marker)

print("Guardado:", ok)
print("Terminado")
import cv2
import numpy as np
import mediapipe as mp

if not hasattr(cv2, "aruco"):
    raise Exception("ERROR: instala opencv-contrib-python, no opencv-python")

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)

try:
    aruco_params = cv2.aruco.DetectorParameters()
except:
    aruco_params = cv2.aruco.DetectorParameters_create()

detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

SCENE_W = 4000
SCENE_H = 2500

VIEW_W = 1280
VIEW_H = 720

scene = np.zeros((SCENE_H, SCENE_W, 3), dtype=np.uint8)

focal = VIEW_W

cameraMatrix = np.array([
    [focal, 0, VIEW_W / 2],
    [0, focal, VIEW_H / 2],
    [0, 0, 1]
], dtype=np.float32)

distCoeffs = np.zeros((5, 1), dtype=np.float32)

marker_length = 0.05

# ==========================
# FUNCIONES DE DIBUJO
# ==========================

def cielo_atardecer(img):

    altura_cielo = 1000

    for y in range(altura_cielo):

        t = y / altura_cielo

        # Parte alta (azul oscuro)
        if t < 0.25:

            k = t / 0.25

            b = int(120 + k * 80)
            g = int(60 + k * 50)
            r = int(180 + k * 40)

        # Zona morada
        elif t < 0.50:

            k = (t - 0.25) / 0.25

            b = int(200 + k * 20)
            g = int(110 + k * 40)
            r = int(220 + k * 20)

        # Zona rojiza
        elif t < 0.75:

            k = (t - 0.50) / 0.25

            b = int(220 - k * 120)
            g = int(150 + k * 40)
            r = 255

        # Horizonte naranja
        else:

            k = (t - 0.75) / 0.25

            b = int(100 - k * 70)
            g = int(190 + k * 40)
            r = 255

        cv2.line(
            img,
            (0, y),
            (SCENE_W, y),
            (b, g, r),
            1
        )
 
def montañas(img):

    # Montañas lejanas
    for i in range(-300, SCENE_W + 300, 450):

        altura = np.random.randint(400, 700)

        montana = np.array([
            [i, 1000],
            [i + 225, altura],
            [i + 450, 1000]
        ])

        cv2.fillPoly(
            img,
            [montana],
            (170, 150, 140)
        )

    # Montañas cercanas
    for i in range(-300, SCENE_W + 300, 350):

        altura = np.random.randint(250, 550)

        montana = np.array([
            [i, 1000],
            [i + 175, altura],
            [i + 350, 1000]
        ])

        cv2.fillPoly(
            img,
            [montana],
            (90, 90, 110)
        )

        # Iluminación
        luz = np.array([
            [i + 175, altura],
            [i + 60, 1000],
            [i + 175, 1000]
        ])

        cv2.fillPoly(
            img,
            [luz],
            (130, 130, 150)
        )

        # Nieve
        nieve = np.array([
            [i + 140, altura + 60],
            [i + 175, altura],
            [i + 210, altura + 60]
        ])

        cv2.fillPoly(
            img,
            [nieve],
            (255, 255, 255)
        )

def casa(img, x, y):

    # sombra (da profundidad)
    cv2.rectangle(img, (x+6, y+6), (x+186, y+146), (90, 90, 90), -1)

    # cuerpo principal
    cv2.rectangle(img, (x, y), (x+180, y+140), (200, 220, 240), -1)

    # ligero sombreado lateral (fake 3D)
    cv2.rectangle(img, (x+140, y), (x+180, y+140), (170, 190, 210), -1)

    # techo (triángulo con volumen)
    roof = np.array([
        [x-15, y],
        [x+90, y-100],
        [x+195, y]
    ])
    cv2.fillPoly(img, [roof], (120, 40, 40))

    # sombra del techo (profundidad)
    roof_shadow = np.array([
        [x+90, y-100],
        [x+195, y],
        [x+180, y+10],
        [x+90, y-85]
    ])
    cv2.fillPoly(img, [roof_shadow], (90, 30, 30))

    # puerta con profundidad
    cv2.rectangle(img, (x+70, y+70), (x+110, y+140), (90, 60, 40), -1)
    cv2.rectangle(img, (x+73, y+73), (x+107, y+137), (130, 90, 60), -1)

    # ventanas (con brillo)
    for wx in [x+20, x+125]:

        # marco
        cv2.rectangle(img, (wx, y+25), (wx+40, y+60), (230, 230, 230), -1)

        # vidrio
        cv2.rectangle(img, (wx+3, y+28), (wx+37, y+57), (180, 220, 255), -1)

        # cruz de ventana
        cv2.line(img, (wx+20, y+25), (wx+20, y+60), (80, 80, 80), 1)
        cv2.line(img, (wx, y+42), (wx+40, y+42), (80, 80, 80), 1)


def arbol(img, x, y):

    cv2.rectangle(img,
                  (x,y),
                  (x+25,y+100),
                  (40,80,140), -1)

    cv2.circle(img,(x+12,y-10),50,(0,120,0),-1)
    cv2.circle(img,(x-15,y+20),40,(0,150,0),-1)
    cv2.circle(img,(x+40,y+20),40,(0,170,0),-1)


def flor(img, x, y):

    # tallo con leve grosor
    cv2.line(img, (x, y), (x, y-45), (0, 160, 0), 4)
    cv2.line(img, (x+2, y), (x+2, y-45), (0, 120, 0), 2)

    # pétalos (más naturales, en círculo)
    cv2.circle(img, (x, y-55), 10, (255, 80, 200), -1)   # arriba
    cv2.circle(img, (x-10, y-45), 10, (255, 0, 180), -1) # izquierda
    cv2.circle(img, (x+10, y-45), 10, (255, 0, 180), -1) # derecha
    cv2.circle(img, (x, y-35), 10, (255, 100, 210), -1)  # abajo

    # pétalos extra (diagonales para volumen)
    cv2.circle(img, (x-8, y-55), 8, (255, 120, 220), -1)
    cv2.circle(img, (x+8, y-55), 8, (255, 120, 220), -1)

    # centro de la flor
    cv2.circle(img, (x, y-45), 6, (0, 220, 255), -1)

    # brillo central (efecto luz)
    cv2.circle(img, (x-2, y-47), 2, (255, 255, 255), -1)


def auto(img, x, y, color):

    # sombra
    cv2.ellipse(img,
                (x + 60, y + 55),
                (70, 15),
                0,
                0,
                360,
                (50, 50, 50),
                -1)

    # carrocería
    cv2.rectangle(img,
                  (x, y),
                  (x + 120, y + 40),
                  color,
                  -1)

    # techo
    techo = np.array([
        [x + 20, y],
        [x + 40, y - 35],
        [x + 80, y - 35],
        [x + 100, y]
    ])

    cv2.fillPoly(img, [techo], color)

    # ventanas
    ventana = np.array([
        [x + 30, y - 5],
        [x + 45, y - 28],
        [x + 75, y - 28],
        [x + 90, y - 5]
    ])

    cv2.fillPoly(img,
                 [ventana],
                 (255, 220, 180))

    # división ventanas
    cv2.line(img,
             (x + 60, y - 30),
             (x + 60, y),
             (80, 80, 80),
             2)

    # ruedas
    cv2.circle(img,
               (x + 25, y + 40),
               16,
               (30, 30, 30),
               -1)

    cv2.circle(img,
               (x + 95, y + 40),
               16,
               (30, 30, 30),
               -1)

    # rines
    cv2.circle(img,
               (x + 25, y + 40),
               7,
               (180, 180, 180),
               -1)

    cv2.circle(img,
               (x + 95, y + 40),
               7,
               (180, 180, 180),
               -1)

    # luces delanteras
    cv2.circle(img,
               (x + 118, y + 10),
               4,
               (200, 255, 255),
               -1)

    # luces traseras
    cv2.circle(img,
               (x + 2, y + 10),
               4,
               (0, 0, 255),
               -1)

    # defensa delantera
    cv2.line(img,
             (x + 118, y + 25),
             (x + 120, y + 25),
             (180, 180, 180),
             3)

    # manija
    cv2.line(img,
             (x + 70, y + 15),
             (x + 80, y + 15),
             (200, 200, 200),
             2)


def nube(img, x, y):

    # sombra suave (da profundidad)
    cv2.circle(img, (x+10, y+10), 55, (200, 200, 200), -1)
    cv2.circle(img, (x+50, y), 65, (210, 210, 210), -1)
    cv2.circle(img, (x+100, y+10), 55, (200, 200, 200), -1)

    # capa principal (blanco puro)
    cv2.circle(img, (x, y), 45, (255, 255, 255), -1)
    cv2.circle(img, (x+45, y-20), 60, (255, 255, 255), -1)
    cv2.circle(img, (x+95, y), 45, (255, 255, 255), -1)

    # capa superior (volumen extra)
    cv2.circle(img, (x+25, y-35), 50, (250, 250, 250), -1)
    cv2.circle(img, (x+70, y-30), 40, (245, 245, 245), -1)

    # brillo (efecto luz del sol)
    cv2.circle(img, (x+35, y-20), 15, (255, 255, 255), -1)

def sol(img, x, y, radio=80):

    # halo grande 
    cv2.circle(img, (x, y), radio + 60, (0, 180, 255), -1)
    cv2.circle(img, (x, y), radio + 40, (0, 210, 255), -1)

    # disco del sol
    cv2.circle(img, (x, y), radio, (0, 255, 255), -1)

    # centro brillante
    cv2.circle(img, (x, y), radio - 20, (255, 255, 255), -1)

    # rayos 
    for i in range(0, 360, 15):
        angle = np.radians(i)

        x1 = int(x + np.cos(angle) * radio)
        y1 = int(y + np.sin(angle) * radio)

        x2 = int(x + np.cos(angle) * (radio + 80))
        y2 = int(y + np.sin(angle) * (radio + 80))

        cv2.line(img, (x1, y1), (x2, y2), (0, 200, 255), 3)


def puente(img, x=1500, y=1750, ancho=700, alto=400):

    # seguridad de límites
    h, w = img.shape[:2]

    x2 = min(x + ancho, w - 1)
    y2 = min(y + alto, h - 1)

    # base del puente
    cv2.rectangle(img,
                  (x, y),
                  (x2, y2),
                  (90, 90, 90),
                  -1)

    # tablas (textura del puente)
    for i in range(x, x2, 40):
        cv2.line(img,
                 (i, y),
                 (i, y2),
                 (60, 60, 60),
                 1)

    # bordes superior e inferior
    cv2.rectangle(img, (x, y), (x2, y + 20), (50, 50, 50), -1)
    cv2.rectangle(img, (x, y2 - 20), (x2, y2), (50, 50, 50), -1)

    # postes
    for i in range(x, x2, 80):
        cv2.rectangle(img,
                      (i, y - 30),
                      (i + 8, y2 + 30),
                      (40, 40, 40),
                      -1)

    # sombra (efecto flotante eliminado)
    cv2.rectangle(img,
                  (x, y2),
                  (x2, y2 + 20),
                  (0, 0, 0),
                  -1)
    
def camion(img):

    x = 1900
    y = 1240

    # cuerpo del camión
    cv2.rectangle(img,
                  (x, y),
                  (x + 200, y + 80),
                  (255, 120, 0),
                  -1)

    # cabina
    cv2.rectangle(img,
                  (x + 140, y - 40),
                  (x + 200, y + 80),
                  (200, 60, 0),
                  -1)

    # ventana
    cv2.rectangle(img,
                  (x + 150, y - 25),
                  (x + 190, y + 10),
                  (220, 220, 220),
                  -1)

    # ruedas
    cv2.circle(img, (x + 50, y + 85), 18, (0, 0, 0), -1)
    cv2.circle(img, (x + 160, y + 85), 18, (0, 0, 0), -1)

    # centro ruedas
    cv2.circle(img, (x + 50, y + 85), 7, (200, 200, 200), -1)
    cv2.circle(img, (x + 160, y + 85), 7, (200, 200, 200), -1)

    # línea de separación
    cv2.line(img, (x + 140, y), (x + 140, y + 80), (0, 0, 0), 2)

def vaca(img):

    x = 3200
    y = 1150

    # sombra suave en el suelo
    cv2.ellipse(img,
                (x + 90, y + 135),
                (90, 25),
                0,
                0,
                360,
                (0, 0, 0),
                -1)

    # cuerpo 
    cv2.ellipse(img,
                (x + 70, y + 50),
                (80, 50),
                0,
                0,
                360,
                (255, 255, 255),
                -1)

    # cabeza 
    cv2.circle(img,
               (x + 165, y + 45),
               30,
               (255, 255, 255),
               -1)

    # ojos
    cv2.circle(img, (x + 175, y + 40), 4, (0, 0, 0), -1)
    cv2.circle(img, (x + 155, y + 40), 4, (0, 0, 0), -1)

    # nariz
    cv2.circle(img, (x + 165, y + 60), 7, (200, 200, 200), -1)

    # orejas
    cv2.ellipse(img,
                (x + 185, y + 20),
                (10, 15),
                30,
                0,
                360,
                (255, 255, 255),
                -1)

    cv2.ellipse(img,
                (x + 145, y + 20),
                (10, 15),
                -30,
                0,
                360,
                (255, 255, 255),
                -1)

    # 🐄 patas 
    leg_color = (240, 240, 240)

    cv2.rectangle(img, (x + 40, y + 80), (x + 55, y + 135), leg_color, -1)
    cv2.rectangle(img, (x + 80, y + 80), (x + 95, y + 135), leg_color, -1)
    cv2.rectangle(img, (x + 110, y + 80), (x + 125, y + 135), leg_color, -1)
    cv2.rectangle(img, (x + 145, y + 80), (x + 160, y + 135), leg_color, -1)

    # 🐄 manchas 
    cv2.ellipse(img, (x + 60, y + 50), (12, 8), 0, 0, 360, (0, 0, 0), -1)
    cv2.ellipse(img, (x + 90, y + 40), (10, 6), 0, 0, 360, (0, 0, 0), -1)
    cv2.ellipse(img, (x + 120, y + 60), (14, 9), 0, 0, 360, (0, 0, 0), -1)

    # 🐄 cola
    cv2.line(img,
             (x + 10, y + 40),
             (x - 20, y + 80),
             (0, 0, 0),
             2)

    cv2.circle(img,
               (x - 20, y + 80),
               4,
               (0, 0, 0),
               -1)

def lago(img):

    cx = 1000
    cy = 1500   

    # borde de pasto 
    cv2.ellipse(img,
                (cx, cy + 25),
                (240, 150),
                0,
                0,
                360,
                (60, 170, 60),
                -1)

    # agua 
    cv2.ellipse(img,
                (cx, cy),
                (200, 120),
                0,
                0,
                360,
                (200, 140, 90),
                -1)

    # profundidad
    cv2.ellipse(img,
                (cx, cy + 15),
                (170, 100),
                0,
                0,
                360,
                (170, 110, 70),
                -1)

    # reflejo de luz
    cv2.ellipse(img,
                (cx - 60, cy - 40),
                (90, 35),
                0,
                0,
                360,
                (255, 255, 255),
                -1)

    # borde visible
    cv2.ellipse(img,
                (cx, cy),
                (210, 130),
                0,
                0,
                360,
                (50, 160, 50),
                2)
def escuela(img):

    x = 1600
    y = 850

    # sombra
    cv2.rectangle(img,
                  (x + 15, y + 15),
                  (x + 265, y + 265),
                  (80, 80, 80),
                  -1)

    # edificio principal
    cv2.rectangle(img,
                  (x, y),
                  (x + 250, y + 250),
                  (180, 220, 255),
                  -1)

    # techo
    techo = np.array([
        [x - 20, y],
        [x + 125, y - 80],
        [x + 270, y]
    ])

    cv2.fillPoly(img,
                 [techo],
                 (40, 40, 180))

    # puerta principal
    cv2.rectangle(img,
                  (x + 105, y + 140),
                  (x + 145, y + 250),
                  (80, 120, 160),
                  -1)

    # manija
    cv2.circle(img,
               (x + 135, y + 195),
               3,
               (0, 255, 255),
               -1)

    # ventanas fila superior
    for i in range(4):
        wx = x + 20 + i * 55

        cv2.rectangle(img,
                      (wx, y + 35),
                      (wx + 35, y + 70),
                      (255, 255, 255),
                      -1)

        cv2.line(img,
                 (wx + 17, y + 35),
                 (wx + 17, y + 70),
                 (0, 0, 0),
                 1)

        cv2.line(img,
                 (wx, y + 52),
                 (wx + 35, y + 52),
                 (0, 0, 0),
                 1)

    # ventanas fila inferior
    for i in range(2):
        wx = x + 30 + i * 140

        cv2.rectangle(img,
                      (wx, y + 100),
                      (wx + 50, y + 140),
                      (255, 255, 255),
                      -1)

        cv2.line(img,
                 (wx + 25, y + 100),
                 (wx + 25, y + 140),
                 (0, 0, 0),
                 1)

        cv2.line(img,
                 (wx, y + 120),
                 (wx + 50, y + 120),
                 (0, 0, 0),
                 1)

    # escaleras
    cv2.rectangle(img,
                  (x + 90, y + 250),
                  (x + 160, y + 265),
                  (140, 140, 140),
                  -1)

    cv2.rectangle(img,
                  (x + 80, y + 265),
                  (x + 170, y + 280),
                  (120, 120, 120),
                  -1)

    # letrero
    cv2.rectangle(img,
                  (x + 55, y - 45),
                  (x + 195, y - 10),
                  (255, 255, 255),
                  -1)

    cv2.putText(img,
                "ESCUELA",
                (x + 65, y - 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2)

    # brillo lateral 
    cv2.rectangle(img,
                  (x, y),
                  (x + 12, y + 250),
                  (220, 240, 255),
                  -1)
def hospital(img):

    x = 2000
    y = 850

    # sombra
    cv2.rectangle(img,
                  (x + 15, y + 15),
                  (x + 265, y + 265),
                  (90, 90, 90),
                  -1)

    # edificio principal
    cv2.rectangle(img,
                  (x, y),
                  (x + 250, y + 250),
                  (245, 245, 245),
                  -1)

    # techo
    cv2.rectangle(img,
                  (x - 10, y - 15),
                  (x + 260, y),
                  (180, 180, 180),
                  -1)

    # cruz roja central
    cv2.line(img,
             (x + 125, y + 40),
             (x + 125, y + 160),
             (0, 0, 255),
             14)

    cv2.line(img,
             (x + 70, y + 100),
             (x + 180, y + 100),
             (0, 0, 255),
             14)

    # ventanas
    for fila in range(2):
        for col in range(4):

            wx = x + 20 + col * 55
            wy = y + 170 + fila * 35

            cv2.rectangle(img,
                          (wx, wy),
                          (wx + 35, wy + 25),
                          (255, 220, 180),
                          -1)

            cv2.rectangle(img,
                          (wx, wy),
                          (wx + 35, wy + 25),
                          (120, 120, 120),
                          1)

    # entrada principal
    cv2.rectangle(img,
                  (x + 95, y + 170),
                  (x + 155, y + 250),
                  (120, 160, 200),
                  -1)

    # manijas
    cv2.circle(img,
               (x + 118, y + 210),
               3,
               (0, 255, 255),
               -1)

    cv2.circle(img,
               (x + 132, y + 210),
               3,
               (0, 255, 255),
               -1)

    # escalones
    cv2.rectangle(img,
                  (x + 85, y + 250),
                  (x + 165, y + 265),
                  (140, 140, 140),
                  -1)

    cv2.rectangle(img,
                  (x + 75, y + 265),
                  (x + 175, y + 280),
                  (120, 120, 120),
                  -1)

    # letrero
    cv2.rectangle(img,
                  (x + 55, y - 55),
                  (x + 195, y - 15),
                  (255, 255, 255),
                  -1)

    cv2.putText(img,
                "HOSPITAL",
                (x + 60, y - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2)

    # brillo lateral 
    cv2.rectangle(img,
                  (x, y),
                  (x + 10, y + 250),
                  (255, 255, 255),
                  -1)
    
def iglesia(img):

    x = 2400
    y = 850

    # sombra
    cv2.rectangle(img,
                  (x + 12, y + 12),
                  (x + 192, y + 262),
                  (80, 80, 80),
                  -1)

    # edificio principal
    cv2.rectangle(img,
                  (x, y),
                  (x + 180, y + 250),
                  (220, 220, 220),
                  -1)

    # techo principal
    techo = np.array([
        [x - 10, y],
        [x + 90, y - 80],
        [x + 190, y]
    ])

    cv2.fillPoly(img,
                 [techo],
                 (60, 60, 160))

    # campanario
    cv2.rectangle(img,
                  (x + 75, y - 150),
                  (x + 105, y),
                  (170, 170, 170),
                  -1)

    # techo campanario
    techo_torre = np.array([
        [x + 65, y - 150],
        [x + 90, y - 190],
        [x + 115, y - 150]
    ])

    cv2.fillPoly(img,
                 [techo_torre],
                 (60, 60, 160))

    # cruz
    cv2.line(img,
             (x + 90, y - 220),
             (x + 90, y - 180),
             (0, 255, 255),
             4)

    cv2.line(img,
             (x + 75, y - 200),
             (x + 105, y - 200),
             (0, 255, 255),
             4)

    # puerta principal
    cv2.rectangle(img,
                  (x + 70, y + 150),
                  (x + 110, y + 250),
                  (70, 90, 140),
                  -1)

    # arco de entrada
    cv2.ellipse(img,
                (x + 90, y + 150),
                (20, 20),
                0,
                180,
                360,
                (70, 90, 140),
                -1)

    # vitrales
    cv2.rectangle(img,
                  (x + 25, y + 70),
                  (x + 55, y + 130),
                  (255, 120, 120),
                  -1)

    cv2.rectangle(img,
                  (x + 125, y + 70),
                  (x + 155, y + 130),
                  (120, 180, 255),
                  -1)

    # detalles vitrales
    cv2.line(img,
             (x + 40, y + 70),
             (x + 40, y + 130),
             (255, 255, 255),
             1)

    cv2.line(img,
             (x + 140, y + 70),
             (x + 140, y + 130),
             (255, 255, 255),
             1)

    # escaleras
    cv2.rectangle(img,
                  (x + 60, y + 250),
                  (x + 120, y + 265),
                  (140, 140, 140),
                  -1)

    cv2.rectangle(img,
                  (x + 50, y + 265),
                  (x + 130, y + 280),
                  (120, 120, 120),
                  -1)

    # iluminación lateral
    cv2.rectangle(img,
                  (x, y),
                  (x + 8, y + 250),
                  (245, 245, 245),
                  -1)
    
def granja(img):

    x = 2800
    y = 900

    # sombra
    cv2.rectangle(img,
                  (x + 15, y + 15),
                  (x + 265, y + 215),
                  (70, 70, 70),
                  -1)

    # granero principal
    cv2.rectangle(img,
                  (x, y),
                  (x + 250, y + 200),
                  (40, 40, 180),
                  -1)

    # techo
    techo = np.array([
        [x - 20, y],
        [x + 125, y - 100],
        [x + 270, y]
    ])

    cv2.fillPoly(img,
                 [techo],
                 (20, 20, 120))

    # puerta principal
    cv2.rectangle(img,
                  (x + 90, y + 80),
                  (x + 160, y + 200),
                  (80, 120, 180),
                  -1)

    # líneas de la puerta
    cv2.line(img,
             (x + 125, y + 80),
             (x + 125, y + 200),
             (255, 255, 255),
             2)

    cv2.line(img,
             (x + 90, y + 140),
             (x + 160, y + 140),
             (255, 255, 255),
             2)

    # ventanas
    cv2.rectangle(img,
                  (x + 30, y + 50),
                  (x + 70, y + 90),
                  (255, 255, 255),
                  -1)
    
    cv2.rectangle(img,
                  (x + 180, y + 50),
                  (x + 220, y + 90),
                  (255, 255, 255),
                  -1)

   
# silo
    cv2.rectangle(img,
                  (x + 280, y + 20),
                  (x + 340, y + 200),
                  (180, 180, 180),
                  -1)

    cv2.ellipse(img,
                (x + 310, y + 20),
                (30, 20),
                0,
                180,
                360,
                (200, 200, 200),
                -1)


    # cerca
    for i in range(x - 80, x + 420, 25):

        cv2.line(img,
                 (i, y + 180),
                 (i, y + 240),
                 (80, 120, 180),
                 3)

    cv2.line(img,
             (x - 80, y + 195),
             (x + 420, y + 195),
             (80, 120, 180),
             3)

    cv2.line(img,
             (x - 80, y + 225),
             (x + 420, y + 225),
             (80, 120, 180),
             3)
    
def molino(img):

    x = 3300
    y = 850

    # sombra
    cv2.ellipse(img,
                (x + 10, y + 260),
                (90, 25),
                0,
                0,
                360,
                (60, 60, 60),
                -1)

    # torre principal
    cuerpo = np.array([
        [x - 50, y + 250],
        [x + 50, y + 250],
        [x + 30, y],
        [x - 30, y]
    ])

    cv2.fillPoly(img,
                 [cuerpo],
                 (170, 190, 220))

    # techo cónico
    techo = np.array([
        [x - 45, y],
        [x, y - 70],
        [x + 45, y]
    ])

    cv2.fillPoly(img,
                 [techo],
                 (50, 50, 150))

    # puerta
    cv2.rectangle(img,
                  (x - 15, y + 180),
                  (x + 15, y + 250),
                  (80, 120, 160),
                  -1)

    # ventanas
    cv2.rectangle(img,
                  (x - 12, y + 60),
                  (x + 12, y + 90),
                  (255, 255, 255),
                  -1)

    cv2.rectangle(img,
                  (x - 12, y + 120),
                  (x + 12, y + 150),
                  (255, 255, 255),
                  -1)

    # centro de aspas
    cx = x
    cy = y + 20

    cv2.circle(img,
               (cx, cy),
               12,
               (120, 120, 120),
               -1)

    # aspas
    cv2.line(img, (cx, cy), (cx, cy - 120),
             (255, 255, 255), 8)

    cv2.line(img, (cx, cy), (cx, cy + 120),
             (255, 255, 255), 8)

    cv2.line(img, (cx, cy), (cx - 120, cy),
             (255, 255, 255), 8)

    cv2.line(img, (cx, cy), (cx + 120, cy),
             (255, 255, 255), 8)

    # aspas diagonales
    cv2.line(img, (cx, cy), (cx - 85, cy - 85),
             (240, 240, 240), 6)

    cv2.line(img, (cx, cy), (cx + 85, cy + 85),
             (240, 240, 240), 6)

    cv2.line(img, (cx, cy), (cx - 85, cy + 85),
             (240, 240, 240), 6)

    cv2.line(img, (cx, cy), (cx + 85, cy - 85),
             (240, 240, 240), 6)
    
def estadio(img):

    x = 3500
    y = 1500

    # sombra
    cv2.ellipse(img,
                (x + 20, y + 20),
                (240, 170),
                0,
                0,
                360,
                (80, 80, 80),
                -1)

    # gradas exteriores
    cv2.ellipse(img,
                (x, y),
                (230, 160),
                0,
                0,
                360,
                (180, 180, 180),
                -1)

    # gradas internas
    cv2.ellipse(img,
                (x, y),
                (190, 125),
                0,
                0,
                360,
                (140, 140, 140),
                -1)

    # cancha
    cv2.ellipse(img,
                (x, y),
                (140, 85),
                0,
                0,
                360,
                (50, 180, 50),
                -1)

    # línea central
    cv2.line(img,
             (x, y - 85),
             (x, y + 85),
             (255, 255, 255),
             2)

    # círculo central
    cv2.circle(img,
               (x, y),
               25,
               (255, 255, 255),
               2)

    # porterías
    cv2.rectangle(img,
                  (x - 125, y - 20),
                  (x - 110, y + 20),
                  (255, 255, 255),
                  2)

    cv2.rectangle(img,
                  (x + 110, y - 20),
                  (x + 125, y + 20),
                  (255, 255, 255),
                  2)

    # torres de iluminación
    for px in [x - 260, x + 260]:

        cv2.line(img,
                 (px, y - 180),
                 (px, y - 40),
                 (120, 120, 120),
                 4)

        cv2.rectangle(img,
                      (px - 20, y - 210),
                      (px + 20, y - 180),
                      (220, 220, 220),
                      -1)

    # entrada principal
    cv2.rectangle(img,
                  (x - 40, y + 120),
                  (x + 40, y + 160),
                  (100, 100, 100),
                  -1)

    # letrero
    cv2.putText(img,
                "ESTADIO",
                (x - 70, y + 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2)
def torre_agua(img):

    x = 3500
    y = 800

    # sombra
    cv2.ellipse(img,
                (x + 20, y + 300),
                (90, 20),
                0,
                0,
                360,
                (60, 60, 60),
                -1)

    # patas principales
    cv2.line(img, (x - 50, y + 300),
                  (x - 20, y + 80),
                  (120, 120, 120), 5)

    cv2.line(img, (x + 50, y + 300),
                  (x + 20, y + 80),
                  (120, 120, 120), 5)

    cv2.line(img, (x - 25, y + 300),
                  (x - 10, y + 80),
                  (120, 120, 120), 5)

    cv2.line(img, (x + 25, y + 300),
                  (x + 10, y + 80),
                  (120, 120, 120), 5)

    # refuerzos cruzados
    cv2.line(img, (x - 50, y + 250),
                  (x + 50, y + 180),
                  (140, 140, 140), 2)

    cv2.line(img, (x + 50, y + 250),
                  (x - 50, y + 180),
                  (140, 140, 140), 2)

    # tanque principal
    cv2.rectangle(img,
                  (x - 80, y),
                  (x + 80, y + 100),
                  (200, 200, 200),
                  -1)

    # tapa superior
    cv2.ellipse(img,
                (x, y),
                (80, 25),
                0,
                180,
                360,
                (220, 220, 220),
                -1)

    # base inferior del tanque
    cv2.ellipse(img,
                (x, y + 100),
                (80, 20),
                0,
                0,
                360,
                (170, 170, 170),
                -1)

    # reflejo de luz
    cv2.rectangle(img,
                  (x - 60, y + 10),
                  (x - 40, y + 90),
                  (240, 240, 240),
                  -1)

    # escalera
    cv2.line(img,
             (x + 95, y + 20),
             (x + 95, y + 280),
             (100, 100, 100),
             2)

    cv2.line(img,
             (x + 110, y + 20),
             (x + 110, y + 280),
             (100, 100, 100),
             2)

    for i in range(y + 30, y + 280, 20):
        cv2.line(img,
                 (x + 95, i),
                 (x + 110, i),
                 (100, 100, 100),
                 1)

    # texto
    cv2.putText(img,
                "AGUA",
                (x - 35, y + 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (80, 80, 80),
                2)
         
    # ==========================
# CREAR PAISAJE
# ==========================

# Cielo
cielo_atardecer(scene)

# Montañas
montañas(scene)

# Sol
sol(scene, 3200, 200)

# Nubes
nube(scene,300,150)
nube(scene,800,220)
nube(scene,1500,170)
nube(scene,2300,250)
nube(scene,3200,180)


# Pasto
cv2.rectangle(scene,
              (0,1000),
              (SCENE_W,SCENE_H),
              (50,180,50),
              -1)

# Lago
lago(scene)

# Rio
cv2.rectangle(scene,
(0,1800), (SCENE_W,2100),
(255,100,0),
-1)

# Puente
puente(scene)

# Carretera
cv2.rectangle(scene,
              (0,1200),
              (SCENE_W,1350),
              (70,70,70),
              -1)

for x in range(0,SCENE_W,120):
    cv2.rectangle(scene,
                  (x,1265),
                  (x+60,1280),
                  (255,255,255),
                  -1)

# Casas
casa(scene,200,900)
casa(scene,500,930)
casa(scene,850,910)
casa(scene,1200,900)

# Escuela
escuela(scene)

# Iglesia
iglesia(scene)

# Granja
granja(scene)

# Molino
molino(scene)

# Estadio
estadio(scene)

# Torre de agua
torre_agua(scene)

# Hospital
hospital(scene)

# Arboles
for x in range(100,3900,250):
    arbol(scene,x,1000)

# Flores
for x in range(150,3900,180):
    flor(scene,x,1700)

# Autos
auto(scene, 1200, 1200, (0, 0, 255))      # rojo
auto(scene, 1500, 1200, (255, 0, 0))      # azul
auto(scene, 1800, 1200, (0, 255, 255))    # amarillo

# Camion
camion(scene)

# Vaca
vaca(scene)

# ==========================
# MEDIAPIPE
# ==========================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

offset_x = SCENE_W // 2
offset_y = SCENE_H // 2
zoom = 1.0

smooth_x = offset_x
smooth_y = offset_y
alpha = 0.2

cameraMatrix = np.array([
    [1000, 0, VIEW_W / 2],
    [0, 1000, VIEW_H / 2],
    [0, 0, 1]
], dtype=np.float32)

distCoeffs = np.zeros((5, 1), dtype=np.float32)

marker_length = 0.05

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(gray)

    rvec = None
    tvec = None

    # ==========================
    # ARUCO DETECCIÓN
    # ==========================
    if ids is not None and len(corners) > 0:

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # ====================
        # USAR SOLO HOMOGRAFÍA 
        # ====================

        marker_corners = corners[0][0].astype(np.float32)

    
        dst = np.array([
            marker_corners[0],
            marker_corners[1],
            marker_corners[2],
            marker_corners[3]
        ], dtype=np.float32)

        src = np.array([
            [0, 0],
            [SCENE_W, 0],
            [SCENE_W, SCENE_H],
            [0, SCENE_H]
        ], dtype=np.float32)

        H = cv2.getPerspectiveTransform(src, dst)

        warped = cv2.warpPerspective(scene, H, (w, h))

        mask = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        fg = cv2.bitwise_and(warped, warped, mask=mask)

        frame = cv2.add(bg, fg)

        cv2.putText(frame,
                    "AR ACTIVADO",
                    (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

    else:

        cv2.putText(frame,
                    "SIN ARUCO",
                    (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)

    cv2.imshow("PAISAJE", cv2.resize(scene, (800, 500)))
    cv2.imshow("AR CAMARA", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
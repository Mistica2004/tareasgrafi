Proyecto: Paisaje 3D con realidad aumentada

Descripción general

Este proyecto implementa una escena de Realidad Aumentada (AR) utilizando Python, OpenCV, OpenGL, GLFW, ArUco y MediaPipe. El sistema detecta un marcador ArUco mediante la cámara web y coloca sobre él una ciudad tridimensional interactiva. Además, permite controlar el zoom y el desplazamiento de la escena mediante gestos de la mano detectados con MediaPipe.


Librerías utilizadas

OpenGL

Se utiliza para renderizar todos los objetos tridimensionales de la escena, como edificios, árboles, animales, carreteras y elementos decorativos.

GLFW

Permite crear la ventana de visualización y administrar el contexto gráfico de OpenGL.

OpenCV

Se utiliza para capturar video desde la cámara, detectar marcadores ArUco y calcular la posición y orientación del marcador.

ArUco

Permite identificar marcadores visuales cuadrados que sirven como referencia para colocar objetos virtuales en el mundo real.

MediaPipe

Se encarga del reconocimiento de la mano y de los gestos utilizados para controlar la escena.

NumPy

Facilita los cálculos matemáticos y el manejo de matrices necesarias para las transformaciones 3D.


Configuración inicial

Se definen parámetros globales como:

* Resolución de la ventana.
* Tamaño del marcador ArUco.
* Escala general del paisaje.
* Parámetros de la cámara virtual.
* Variables de interacción y animación.

Estas configuraciones permiten controlar el tamaño y comportamiento de toda la escena.


Detección de manos

MediaPipe detecta los puntos clave de la mano en tiempo real.

El sistema utiliza dos gestos principales:

Zoom

Cuando el pulgar y el índice se acercan entre sí, se calcula la distancia entre ambos dedos y se modifica el nivel de acercamiento de la cámara.

Desplazamiento

Cuando la mano está abierta, se utiliza la posición de la muñeca para mover la escena en diferentes direcciones.


Detección del marcador ArUco

OpenCV analiza cada cuadro de video buscando marcadores ArUco.

Cuando encuentra uno:

1. Detecta las esquinas del marcador.
2. Calcula su posición en el espacio.
3. Obtiene los vectores de rotación y traslación.
4. Convierte esos datos a matrices compatibles con OpenGL.

Esto permite que la escena virtual permanezca alineada con el marcador físico.


Estabilización de la pose

Para evitar movimientos bruscos causados por pequeñas variaciones en la detección del marcador, se aplica un filtro de suavizado.

Este filtro calcula un promedio progresivo de la posición y orientación detectadas, generando una experiencia visual más estable.


Primitivas 3D

El código incluye funciones básicas para construir objetos tridimensionales:

* Cubos.
* Pirámides.
* Cilindros.
* Esferas.

Estas primitivas sirven como bloques de construcción para todos los elementos del paisaje.


Construcción de la escena

La ciudad está formada por múltiples elementos modelados manualmente mediante primitivas 3D.

Entre ellos se encuentran:

Terreno

Representa el suelo principal donde se coloca toda la ciudad.

Carreteras

Conectan las distintas zonas urbanas.

Río y lagos

Añaden elementos naturales y movimiento visual.

Montañas

Crean profundidad y un horizonte más realista.

Sol y nubes

Forman el fondo ambiental del escenario.

Casas

Representan la zona residencial.

Escuela

Edificio educativo dentro de la ciudad.

Hospital

Centro médico modelado en 3D.

Iglesia

Construcción religiosa con torre principal.

Granja

Zona rural con silo y estructuras agrícolas.

Estadio

Área deportiva con graderías.

Torre de agua

Infraestructura urbana de almacenamiento.

Edificios modernos

Rascacielos que representan la zona urbana avanzada.

Molino

Elemento animado con aspas giratorias.


Vegetación

La escena incorpora distintos tipos de plantas:

* Árboles.
* Pinos.
* Palmeras.
* Flores.
* Girasoles.

Estos elementos mejoran el realismo visual del entorno.


Mobiliario urbano

Se incluyen objetos decorativos y funcionales:

* Semáforos.
* Farolas.
* Bancas.

Algunos de estos elementos poseen animaciones dinámicas.


Personajes y animales

Para dar vida al paisaje se incorporan:

* Personas caminando.
* Pájaros volando.
* Caballos.
* Ovejas.
* Perros.

Los movimientos son generados mediante funciones matemáticas y actualizaciones continuas de posición.


Animaciones

El sistema actualiza constantemente diversos elementos:

* Movimiento de nubes.
* Vuelo de pájaros.
* Circulación de vehículos.
* Caminata de personas.
* Movimiento de animales.
* Giro del molino.
* Ondas del río.
* Desplazamiento del globo aerostático.

Estas animaciones hacen que el escenario sea dinámico.


Fondo de cámara

La imagen capturada por la cámara se utiliza como fondo de la escena.

Sobre esta imagen se renderizan todos los objetos virtuales, creando el efecto de Realidad Aumentada.


Renderizado final

Durante cada ciclo de ejecución:

1. Se captura una imagen de la cámara.
2. Se detecta la mano.
3. Se detecta el marcador ArUco.
4. Se actualizan las animaciones.
5. Se calcula la posición de la escena.
6. OpenGL dibuja todos los objetos 3D.
7. Se muestra el resultado en pantalla.


Resultado

El resultado es una aplicación de Realidad Aumentada interactiva que combina visión por computadora, gráficos 3D y reconocimiento de gestos para visualizar una ciudad animada sobre un marcador ArUco físico.

Codigo
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import cv2.aruco as aruco
import numpy as np
import math
import random
import mediapipe as mp


VIEW_W      = 1280
VIEW_H      = 720
MARKER_SIZE = 0.10
SCENE_SCALE = 0.05

random.seed(42)
np.random.seed(42)

FOCAL = VIEW_W * 0.9
camera_matrix = np.array([
    [FOCAL,     0, VIEW_W/2],
    [0,     FOCAL, VIEW_H/2],
    [0,         0,         1]
], dtype=np.float64)
dist_coeffs = np.zeros((4,1))

# ==========================
# MEDIAPIPE
# ==========================
mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

# ==========================
# INTERACCIÓN
# ==========================
zoom_factor      = 4.0
pan_offset       = [0.0, 0.0, 0.0]
_pinch_dist_prev = None
_pinch_active    = False
_pan_prev_pos    = None
_pan_active      = False
PINCH_THRESHOLD  = 0.08
PAN_OPEN_THR     = 0.15

# ==========================
# ESTABILIZACIÓN DE POSE
# ==========================
SMOOTH_ALPHA   = 0.35   # 0=máximo suavizado, 1=sin suavizado
_rvec_smooth   = None
_tvec_smooth   = None

# ==========================
# ANIMACIÓN
# ==========================
t             = 0.0
molino_angulo = 0.0
rio_onda      = 0.0
globo_fase    = 0.0

nubes_off  = [0.0]*5
nubes_vel  = [0.02, 0.015, 0.025, 0.018, 0.022]
nubes_base = [(-30,18,-30),(-10,20,-28),(15,19,-32),(30,17,-29),(5,21,-35)]

pajaros = [[-20.0,12.0,-15.0,0.0],[-5.0,14.0,-18.0,1.2],
           [10.0,11.5,-12.0,2.4],[25.0,13.0,-20.0,0.8]]

autos_anim = [
    [-10.0, 6.5, (0,0,220),   0.12, 6.5],
    [ -4.0, 7.5, (220,0,0),   0.09, 7.5],
    [  3.0, 6.5, (0,220,220), 0.11, 6.5],
    [ 20.0, 7.5, (255,200,0), 0.08, 7.5],
    [-30.0, 6.5, (180,0,180), 0.13, 6.5],
]

personas = [[-12.0,4.0,0.0,1],[5.0,4.0,1.5,-1],[18.0,4.0,0.8,1]]
caballo  = [-5.0, -8.0, 0.0]
ovejas   = [[10.0,-8.0,0.0,1],[13.0,-9.0,1.0,-1],[16.0,-8.5,2.0,1]]
perro_st = [-8.0,-7.0,0.0,1]

semaforos_x = [-20,-5,15,35]
farolas_x   = list(range(-55,60,10))
casas_pos   = [(-25,-5),(-20,-5),(-14,-5),(-8,-5),(-35,-5),(-40,-5)]
arboles_pos = [(x*4-55,-3) for x in range(28)]
pinos_pos   = [(x*5-50,-18) for x in range(20)]
flores_pos  = [(x*3-55,11) for x in range(36)]
bancos_pos  = [(-15,3),(-5,3),(8,3),(22,3)]

# ==========================
# ARUCO
# ==========================
aruco_dict     = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
aruco_params   = aruco.DetectorParameters()
aruco_detector = aruco.ArucoDetector(aruco_dict, aruco_params)

obj_pts = np.array([
    [-MARKER_SIZE/2,  MARKER_SIZE/2, 0],
    [ MARKER_SIZE/2,  MARKER_SIZE/2, 0],
    [ MARKER_SIZE/2, -MARKER_SIZE/2, 0],
    [-MARKER_SIZE/2, -MARKER_SIZE/2, 0],
], dtype=np.float32)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  VIEW_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIEW_H)

bg_tex = None

# ==========================
# PRIMITIVAS 3D
# ==========================
def set_color(r,g,b):
    glColor3f(r/255.0, g/255.0, b/255.0)

sc = set_color   

def draw_box(x,y,z,w,h,d,color):
    r,g,b = color
    x0,x1 = x-w/2, x+w/2
    y0,y1 = y, y+h
    z0,z1 = z-d/2, z+d/2
    glBegin(GL_QUADS)
    sc(r,g,b);                                  glVertex3f(x0,y0,z1);glVertex3f(x1,y0,z1);glVertex3f(x1,y1,z1);glVertex3f(x0,y1,z1)
    sc(int(r*.8),int(g*.8),int(b*.8));          glVertex3f(x1,y0,z0);glVertex3f(x0,y0,z0);glVertex3f(x0,y1,z0);glVertex3f(x1,y1,z0)
    sc(int(r*.7),int(g*.7),int(b*.7));          glVertex3f(x0,y0,z0);glVertex3f(x0,y0,z1);glVertex3f(x0,y1,z1);glVertex3f(x0,y1,z0)
    sc(int(r*.9),int(g*.9),int(b*.9));          glVertex3f(x1,y0,z1);glVertex3f(x1,y0,z0);glVertex3f(x1,y1,z0);glVertex3f(x1,y1,z1)
    sc(min(255,int(r*1.1)),min(255,int(g*1.1)),min(255,int(b*1.1)));
    glVertex3f(x0,y1,z1);glVertex3f(x1,y1,z1);glVertex3f(x1,y1,z0);glVertex3f(x0,y1,z0)
    sc(int(r*.5),int(g*.5),int(b*.5));          glVertex3f(x0,y0,z0);glVertex3f(x1,y0,z0);glVertex3f(x1,y0,z1);glVertex3f(x0,y0,z1)
    glEnd()

def draw_pyramid(x,y,z,bw,bd,h,color):
    r,g,b = color
    x0,x1 = x-bw/2, x+bw/2
    z0,z1 = z-bd/2, z+bd/2
    tx,ty,tz = x, y+h, z
    glBegin(GL_TRIANGLES)
    sc(r,g,b);                               glVertex3f(x0,y,z1);glVertex3f(x1,y,z1);glVertex3f(tx,ty,tz)
    sc(int(r*.7),int(g*.7),int(b*.7));       glVertex3f(x1,y,z0);glVertex3f(x0,y,z0);glVertex3f(tx,ty,tz)
    sc(int(r*.85),int(g*.85),int(b*.85));    glVertex3f(x0,y,z0);glVertex3f(x0,y,z1);glVertex3f(tx,ty,tz)
    sc(int(r*.9),int(g*.9),int(b*.9));       glVertex3f(x1,y,z1);glVertex3f(x1,y,z0);glVertex3f(tx,ty,tz)
    glEnd()

def draw_cylinder(x,y,z,radius,height,color,segments=12):
    r,g,b = color
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        a = 2*math.pi*i/segments
        cx = x+radius*math.cos(a)
        cz = z+radius*math.sin(a)
        shade = 0.7+0.3*math.cos(a)
        glColor3f(r/255*shade,g/255*shade,b/255*shade)
        glVertex3f(cx,y,cz); glVertex3f(cx,y+height,cz)
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    sc(min(255,int(r*1.2)),min(255,int(g*1.2)),min(255,int(b*1.2)))
    glVertex3f(x,y+height,z)
    for i in range(segments+1):
        a=2*math.pi*i/segments
        glVertex3f(x+radius*math.cos(a),y+height,z+radius*math.sin(a))
    glEnd()

def draw_sphere(x,y,z,radius,color,stacks=7,slices=7):
    r,g,b = color
    for i in range(stacks):
        lat0 = math.pi*(-0.5+i/stacks)
        lat1 = math.pi*(-0.5+(i+1)/stacks)
        lz0,lzr0 = math.sin(lat0),math.cos(lat0)
        lz1,lzr1 = math.sin(lat1),math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices+1):
            lng = 2*math.pi*j/slices
            cx2,cy2 = math.cos(lng),math.sin(lng)
            shade = 0.7+0.3*lz1
            glColor3f(r/255*shade,g/255*shade,b/255*shade)
            glVertex3f(x+cx2*lzr1*radius,y+lz1*radius,z+cy2*lzr1*radius)
            glVertex3f(x+cx2*lzr0*radius,y+lz0*radius,z+cy2*lzr0*radius)
        glEnd()

# ==========================
# CIELO DEGRADADO
# ==========================
def draw_sky():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    glOrtho(0,1,0,1,-1,1)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(0.47,0.24,0.71); glVertex2f(0,1); glVertex2f(1,1)
    glColor3f(1.0,0.55,0.1);   glVertex2f(1,0); glVertex2f(0,0)
    glEnd()
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW); glEnable(GL_DEPTH_TEST)

# ==========================
# TERRENO Y AGUA
# ==========================
def draw_terrain():
    glBegin(GL_QUADS); sc(50,180,50)
    glVertex3f(-60,0,-60);glVertex3f(60,0,-60);glVertex3f(60,0,60);glVertex3f(-60,0,60)
    glEnd()
    glBegin(GL_QUADS); sc(70,70,70)
    glVertex3f(-60,0.02,5);glVertex3f(60,0.02,5);glVertex3f(60,0.02,9);glVertex3f(-60,0.02,9)
    glEnd()
    for xi in range(-58,60,8):
        glBegin(GL_QUADS); sc(255,255,255)
        glVertex3f(xi,0.03,6.8);glVertex3f(xi+4,0.03,6.8);glVertex3f(xi+4,0.03,7.2);glVertex3f(xi,0.03,7.2)
        glEnd()
    glBegin(GL_QUADS); sc(180,170,160)
    glVertex3f(-60,0.02,4);glVertex3f(60,0.02,4);glVertex3f(60,0.02,5);glVertex3f(-60,0.02,5)
    glEnd()
    glBegin(GL_QUADS); sc(180,170,160)
    glVertex3f(-60,0.02,9);glVertex3f(60,0.02,9);glVertex3f(60,0.02,10);glVertex3f(-60,0.02,10)
    glEnd()

def draw_rio():
    for i in range(20):
        fz = 15+(i/20)*7
        offset = math.sin(fz*1.5+rio_onda)*0.5
        r=int(80+offset*20); g=int(120+offset*15); b=int(220+offset*10)
        glBegin(GL_QUADS); glColor3f(r/255,g/255,b/255)
        glVertex3f(-60,0.01,fz);glVertex3f(60,0.01,fz)
        glVertex3f(60,0.01,fz+7/20);glVertex3f(-60,0.01,fz+7/20)
        glEnd()

def draw_lago(x,z):
    glBegin(GL_QUADS); sc(60,170,60)
    glVertex3f(x-5,0.01,z-4);glVertex3f(x+5,0.01,z-4);glVertex3f(x+5,0.01,z+4);glVertex3f(x-5,0.01,z+4)
    glEnd()
    glBegin(GL_QUADS); sc(100,140,200)
    glVertex3f(x-4,0.02,z-3);glVertex3f(x+4,0.02,z-3);glVertex3f(x+4,0.02,z+3);glVertex3f(x-4,0.02,z+3)
    glEnd()
    rf = abs(math.sin(rio_onda*0.5))*0.4+0.6
    glBegin(GL_QUADS); glColor3f(rf,rf*0.9,0.3)
    glVertex3f(x-1.5,0.03,z-0.8);glVertex3f(x+1.5,0.03,z-0.8);glVertex3f(x+1.5,0.03,z+0.8);glVertex3f(x-1.5,0.03,z+0.8)
    glEnd()

# ==========================
# CIELO (sol, nubes, montañas)
# ==========================
def draw_sol():
    sx,sy,sz = 25,18,-42
    draw_sphere(sx,sy,sz,6.0,(255,160,50),6,6)
    draw_sphere(sx,sy,sz,4.5,(255,190,80),6,6)
    draw_sphere(sx,sy,sz,3.0,(255,220,120),8,8)
    draw_sphere(sx,sy,sz,2.0,(255,255,180),8,8)
    draw_sphere(sx,sy,sz,1.0,(255,255,255),8,8)

def draw_nubes():
    for i,(cx,cy,cz) in enumerate(nubes_base):
        ox = nubes_off[i]
        draw_sphere(cx+ox,cy,cz,2.5,(255,255,255))
        draw_sphere(cx+ox+2,cy+1,cz,2.0,(240,240,240))
        draw_sphere(cx+ox-2,cy+.5,cz,2.0,(240,240,240))
        draw_sphere(cx+ox+1,cy,cz+1,1.5,(250,250,250))
        draw_sphere(cx+ox,cy+1.5,cz,1.8,(245,245,245))

def draw_montanas():
    data=[(-40,-22,9,(160,140,130)),(-20,-26,11,(150,130,120)),
          (0,-23,10,(170,155,140)),(20,-25,12,(145,125,115)),
          (40,-21,9,(165,145,135)),(-50,-19,8,(155,135,125)),
          (-30,-24,10,(158,138,128)),(10,-22,9,(162,142,132)),
          (30,-24,11,(148,128,118)),(50,-20,8,(168,148,138))]
    for mx,mz,mh,mc in data:
        draw_pyramid(mx,0,mz,14,14,mh,mc)
        draw_pyramid(mx,mh*0.68,mz,3.5,3.5,mh*0.32,(255,255,255))

# ==========================
# EDIFICIOS
# ==========================
def draw_casa(x,z):
    draw_box(x,0,z,3.5,2.5,3.0,(200,220,240))
    draw_pyramid(x,2.5,z,4.0,3.5,1.5,(120,40,40))
    draw_box(x,0,z+1.51,0.6,1.2,0.05,(90,60,40))
    for wx in [-0.9,0.9]:
        draw_box(x+wx,1.0,z+1.51,0.7,0.6,0.05,(230,230,230))
        draw_box(x+wx,1.05,z+1.52,0.6,0.5,0.04,(180,220,255))

def draw_escuela(x,z):
    draw_box(x,0,z,5.0,3.5,4.0,(180,220,255))
    draw_pyramid(x,3.5,z,5.5,4.5,1.8,(40,40,180))
    draw_box(x,0,z+2.01,0.8,1.8,0.05,(80,120,160))
    for wx in [-1.5,-0.5,0.5,1.5]:
        draw_box(x+wx,2.0,z+2.01,0.6,0.6,0.05,(255,255,255))
        draw_box(x+wx,2.05,z+2.02,0.5,0.5,0.04,(255,255,200))
    draw_box(x,3.55,z+2.0,2.5,0.5,0.08,(255,255,255))

def draw_hospital(x,z):
    draw_box(x,0,z,5.0,4.0,4.0,(245,245,245))
    draw_box(x,4.0,z,5.2,0.3,4.2,(180,180,180))
    draw_box(x,2.0,z+2.01,0.4,2.0,0.1,(0,0,220))
    draw_box(x,2.7,z+2.01,2.0,0.4,0.1,(0,0,220))
    for fila in range(2):
        for col in range(4):
            wx=x-1.7+col*1.1; wy=0.5+fila*1.2
            draw_box(wx,wy,z+2.01,0.7,0.5,0.05,(255,220,180))
    draw_box(x,0,z+2.01,1.0,2.0,0.05,(120,160,200))
    draw_box(x,4.1,z+2.0,2.5,0.5,0.08,(255,255,255))

def draw_iglesia(x,z):
    draw_box(x,0,z,4.0,3.5,4.0,(220,220,220))
    draw_pyramid(x,3.5,z,4.5,4.5,2.0,(60,60,160))
    draw_box(x,3.5,z,1.0,3.0,1.0,(170,170,170))
    draw_pyramid(x,6.5,z,1.2,1.2,1.5,(60,60,160))
    draw_box(x,7.8,z,0.1,1.0,0.1,(0,220,220))
    draw_box(x,8.3,z,0.5,0.1,0.1,(0,220,220))
    draw_box(x,0,z+2.01,0.7,1.5,0.05,(70,90,140))

def draw_granja(x,z):
    draw_box(x,0,z,5.0,3.5,4.0,(40,40,180))
    draw_pyramid(x,3.5,z,5.5,4.5,2.0,(20,20,120))
    draw_box(x,0,z+2.01,1.2,2.0,0.05,(80,120,180))
    draw_cylinder(x+3.2,0,z,0.7,4.5,(180,180,180))
    draw_pyramid(x+3.2,4.5,z,1.6,1.6,0.8,(200,200,200))

def draw_estadio(x,z):
    for i in range(16):
        a=2*math.pi*i/16
        draw_box(x+4.5*math.cos(a),0,z+3.0*math.sin(a),1.2,2.0,1.2,(160,160,160))
    for i in range(16):
        a=2*math.pi*i/16
        draw_box(x+3.5*math.cos(a),0,z+2.2*math.sin(a),0.9,1.5,0.9,(130,130,130))
    glBegin(GL_QUADS); sc(50,200,50)
    glVertex3f(x-3,0.01,z-2);glVertex3f(x+3,0.01,z-2);glVertex3f(x+3,0.01,z+2);glVertex3f(x-3,0.01,z+2)
    glEnd()
    for px in [-5.5,5.5]:
        draw_box(x+px,0,z,0.2,4.5,0.2,(120,120,120))
        draw_box(x+px,4.3,z,1.2,0.3,0.6,(220,220,220))

def draw_torre_agua(x,z):
    for ox,oz in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        draw_box(x+ox*0.9,0,z+oz*0.9,0.18,5.0,0.18,(120,120,120))
    draw_cylinder(x,4.8,z,1.5,1.8,(200,200,200))
    draw_pyramid(x,6.6,z,3.2,3.2,0.8,(180,180,200))

def draw_edificio_moderno(x,z):
    draw_box(x,0,z,4.0,12.0,4.0,(160,180,210))
    for piso in range(0,12):
        for col in range(3):
            draw_box(x-1.2+col*1.2,0.5+piso*1.0,z+2.01,0.6,0.5,0.04,(200,230,255))
    draw_box(x,12.0,z,0.2,1.5,0.2,(180,180,200))

def draw_molino(x,z):
    draw_box(x,0,z,2.0,5.0,2.0,(170,190,220))
    draw_pyramid(x,5.0,z,2.2,2.2,1.5,(50,50,150))
    draw_sphere(x,5.5,z+1.1,0.25,(120,120,120))
    glPushMatrix()
    glTranslatef(x,5.5,z+1.1)
    glRotatef(molino_angulo,0,0,1)
    glTranslatef(-x,-5.5,-(z+1.1))
    draw_box(x,5.5,z+1.1,0.12,3.5,0.08,(255,255,255))
    draw_box(x,5.5,z+1.1,3.5,0.12,0.08,(255,255,255))
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x,5.5,z+1.1)
    glRotatef(molino_angulo+45,0,0,1)
    glTranslatef(-x,-5.5,-(z+1.1))
    draw_box(x,5.5,z+1.1,0.1,3.0,0.07,(220,220,220))
    draw_box(x,5.5,z+1.1,3.0,0.1,0.07,(220,220,220))
    glPopMatrix()

def draw_puente(x,z):
    draw_box(x,0.5,z,14,0.3,2.0,(90,90,90))
    for px in range(-6,7,2):
        draw_box(x+px,0.5,z-1.0,0.15,2.0,0.15,(50,50,50))
        draw_box(x+px,0.5,z+1.0,0.15,2.0,0.15,(50,50,50))
    draw_box(x,2.3,z-1.0,14,0.1,0.1,(60,60,60))
    draw_box(x,2.3,z+1.0,14,0.1,0.1,(60,60,60))

# ==========================
# VEGETACIÓN
# ==========================
def draw_arbol(x,z):
    draw_cylinder(x,0,z,0.2,1.5,(40,80,140))
    draw_sphere(x,1.8,z,1.2,(0,130,0))
    draw_sphere(x-.5,1.4,z,1.0,(0,160,0))
    draw_sphere(x+.5,1.4,z,1.0,(0,150,0))

def draw_pino(x,z):
    draw_cylinder(x,0,z,0.15,1.0,(80,50,20))
    draw_pyramid(x,0.8,z,2.0,2.0,2.5,(0,120,30))
    draw_pyramid(x,2.0,z,1.5,1.5,2.0,(0,140,40))
    draw_pyramid(x,3.2,z,1.0,1.0,1.5,(0,160,50))

def draw_palmera(x,z):
    for i in range(5):
        draw_cylinder(x+i*0.05,i*0.8,z,0.15,0.85,(160,120,60))
    for ang in range(0,360,60):
        rad=math.radians(ang)
        draw_box(x+0.25+math.cos(rad)*0.8,3.8+math.sin(rad)*0.2,z+math.sin(rad)*0.8,
                 1.2,0.06,0.08,(0,160,60))

def draw_flor(x,z,c1=(255,80,200),c2=(255,0,180)):
    draw_box(x,0,z,0.07,1.0,0.07,(0,160,0))
    draw_sphere(x,1.1,z,0.15,c1)
    draw_sphere(x+.2,1.0,z,0.13,c2)
    draw_sphere(x-.2,1.0,z,0.13,c2)
    draw_sphere(x,1.0,z+.2,0.13,c2)
    draw_sphere(x,1.0,z-.2,0.13,c2)
    draw_sphere(x,1.05,z,0.08,(0,220,255))

def draw_girasol(x,z):
    draw_box(x,0,z,0.08,1.5,0.08,(0,140,0))
    for ang in range(0,360,40):
        rad=math.radians(ang)
        draw_sphere(x+math.cos(rad)*0.2,1.7,z+math.sin(rad)*0.2,0.15,(255,200,0))
    draw_sphere(x,1.7,z,0.18,(80,40,0))

# ==========================
# MOBILIARIO URBANO
# ==========================
def draw_semaforo(x,z):
    draw_box(x,0,z,0.12,3.5,0.12,(60,60,60))
    draw_box(x,3.3,z,0.3,0.9,0.3,(40,40,40))
    fase=int(t*0.5)%3
    draw_sphere(x,3.9,z,0.1,(220,0,0)   if fase==0 else (60,0,0))
    draw_sphere(x,3.6,z,0.1,(220,180,0) if fase==1 else (60,50,0))
    draw_sphere(x,3.3,z,0.1,(0,200,0)   if fase==2 else (0,60,0))

def draw_farola(x,z):
    draw_box(x,0,z,0.1,4.0,0.1,(80,80,80))
    draw_box(x+0.5,3.9,z,1.0,0.08,0.08,(80,80,80))
    draw_sphere(x+1.0,3.9,z,0.2,(255,240,180))
    draw_sphere(x+1.0,3.9,z,0.15,(255,255,220))

def draw_banco(x,z):
    draw_box(x,0.4,z,1.5,0.08,0.5,(120,80,40))
    draw_box(x,0.6,z-.2,1.5,0.08,0.08,(120,80,40))
    for px in [-0.6,0.6]:
        draw_box(x+px,0,z,0.08,0.65,0.08,(100,65,30))

# ==========================
# PERSONAJES Y ANIMALES
# ==========================
def draw_persona(x,z,fase):
    p=math.sin(fase)*0.25
    draw_box(x-.1,0,z+p,.15,.7,.15,(50,50,150))
    draw_box(x+.1,0,z-p,.15,.7,.15,(50,50,150))
    draw_box(x,.7,z,.35,.6,.25,(200,100,50))
    brazo=math.sin(fase)*0.2
    draw_box(x-.25,.85,z+brazo,.12,.5,.12,(220,160,100))
    draw_box(x+.25,.85,z-brazo,.12,.5,.12,(220,160,100))
    draw_sphere(x,1.45,z,.22,(220,160,110))

def draw_pajaro(x,y,z,fase):
    draw_sphere(x,y,z,0.18,(30,30,30))
    ala=math.sin(fase)*0.3
    glBegin(GL_TRIANGLES); sc(20,20,20)
    glVertex3f(x,y,z-.18);glVertex3f(x-.6,y+ala,z-.1);glVertex3f(x-.3,y,z-.05)
    glVertex3f(x,y,z+.18);glVertex3f(x+.6,y+ala,z+.1);glVertex3f(x+.3,y,z+.05)
    glEnd()

def draw_oveja(x,z,fase):
    draw_sphere(x,0.55,z,0.55,(240,240,240))
    draw_sphere(x+0.2,0.6,z+0.25,0.35,(235,235,235))
    draw_sphere(x+0.2,0.6,z-0.25,0.35,(235,235,235))
    draw_sphere(x+0.65,0.7,z,0.28,(220,210,200))
    for ox,oz in [(0.25,0.2),(0.25,-0.2),(-0.25,0.2),(-0.25,-0.2)]:
        draw_box(x+ox,0,z+oz,0.12,0.4,0.12,(200,190,180))

def draw_caballo(x,z,fase):
    draw_box(x,0.9,z,2.2,1.0,1.0,(140,100,60))
    draw_box(x+1.0,1.2,z,0.5,1.0,0.55,(145,105,65))
    draw_box(x+1.3,2.0,z,0.9,0.6,0.5,(140,100,60))
    p=math.sin(fase)*0.2
    draw_box(x+0.6,0,z+0.38+p,.22,.92,.22,(120,85,45))
    draw_box(x+0.6,0,z-0.38-p,.22,.92,.22,(120,85,45))
    draw_box(x-0.6,0,z+0.38-p,.22,.92,.22,(120,85,45))
    draw_box(x-0.6,0,z-0.38+p,.22,.92,.22,(120,85,45))
    draw_box(x-1.1,1.2,z,0.08,0.08,0.7,(80,50,20))

def draw_perro(x,z,fase):
    draw_box(x,0.35,z,0.9,0.4,0.45,(180,140,80))
    draw_sphere(x+0.5,0.8,z,0.28,(190,150,90))
    draw_box(x+0.72,0.68,z,0.22,0.15,0.2,(200,160,100))
    p=math.sin(fase)*0.15
    draw_box(x+0.3,0,z+0.18+p,.15,.38,.15,(170,130,70))
    draw_box(x+0.3,0,z-0.18-p,.15,.38,.15,(170,130,70))
    draw_box(x-0.3,0,z+0.18-p,.15,.38,.15,(170,130,70))
    draw_box(x-0.3,0,z-0.18+p,.15,.38,.15,(170,130,70))

def draw_auto(x,z,color):
    draw_box(x,0.3,z,2.2,0.7,1.0,color)
    draw_box(x,1.0,z,1.4,0.6,0.9,color)
    for wx,wz in [(-.7,-.55),(.7,-.55),(-.7,.55),(.7,.55)]:
        draw_cylinder(x+wx,0,z+wz,0.3,0.25,(30,30,30))

def draw_globo():
    gx=5+math.sin(globo_fase*0.3)*8
    gy=16+math.sin(globo_fase*0.5)*2
    gz=-22
    draw_box(gx,gy-3,gz,0.8,0.6,0.8,(139,90,43))
    for ox,oz in [(-0.3,-0.3),(0.3,-0.3),(-0.3,0.3),(0.3,0.3)]:
        draw_box(gx+ox,gy-2.5,gz+oz,0.04,2.5,0.04,(100,70,30))
    draw_sphere(gx,gy,gz,2.5,(220,50,50))
    draw_sphere(gx,gy,gz,2.3,(255,255,50))
    draw_sphere(gx,gy+0.5,gz,2.0,(50,50,220))
    draw_sphere(gx,gy-0.5,gz,2.0,(50,200,50))
    draw_sphere(gx,gy-1.8,gz,0.3,(255,150,0))

# ==========================
# ESCENA COMPLETA
# ==========================
def draw_scene_3d():
    glScalef(SCENE_SCALE,SCENE_SCALE,SCENE_SCALE)

    # Fondo y terreno base
    draw_montanas()
    draw_sol()
    draw_nubes()
    draw_terrain()
    draw_rio()

    # Agua
    draw_lago(-15,-12)
    draw_lago(40,-8)
    draw_puente(0,15)

    # Zona residencial (izquierda)
    for bx,bz in casas_pos:
        draw_casa(bx,bz)

    # Edificios especiales
    draw_escuela(-45, -15)
    draw_hospital(45, -15)
    draw_iglesia( 0,  -30)
    draw_granja( -45,  15)
    draw_estadio( 45,  15)
    draw_torre_agua(20, -20)
    draw_edificio_moderno(-5, -40)
    draw_edificio_moderno( 5, -40)
    draw_molino(30,-14)

    # Mobiliario urbano
    for bx,bz in bancos_pos:
        draw_banco(bx,bz)
    for sx in semaforos_x:
        draw_semaforo(sx,4.2)
    for fx in farolas_x:
        draw_farola(fx,3.5)

    # Vegetación
    for tx,tz in arboles_pos:
        draw_arbol(tx,tz)
    for tx,tz in pinos_pos:
        draw_pino(tx,tz)
    # Palmeras junto al lago
    for px in range(-2,3):
        draw_palmera(-15+px*2,-6)
        draw_palmera(40+px*2,-3)

    # Flores y girasoles
    palette=[(255,80,200),(255,50,50),(100,100,255)]
    for i,(fx,fz) in enumerate(flores_pos):
        c=palette[i%3]
        draw_flor(fx,fz,c,(c[0]//2,c[1]//2,c[2]//2))
    for gx in range(-30,30,6):
        draw_girasol(gx,-14)

    # Vehículos
    for a in autos_anim:
        draw_auto(a[0],a[4],a[2])

    # Personas
    for p in personas:
        draw_persona(p[0],p[1],p[2])

    # Animales
    draw_caballo(caballo[0],caballo[1],caballo[2])
    for o in ovejas:
        draw_oveja(o[0],o[1],o[2])
    draw_perro(perro_st[0],perro_st[1],perro_st[2])

    # Pájaros y globo
    for p in pajaros:
        draw_pajaro(p[0],p[1],p[2],p[3])
    draw_globo()

# ==========================
# FONDO CÁMARA
# ==========================
def init_bg_texture():
    global bg_tex
    bg_tex = glGenTextures(1)

def draw_background(frame):
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = np.ascontiguousarray(np.flipud(img))
    h,w = img.shape[:2]
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    glOrtho(0,1,0,1,-1,1)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D,bg_tex)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,w,h,0,GL_RGB,GL_UNSIGNED_BYTE,img)
    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    glTexCoord2f(0,0);glVertex2f(0,0)
    glTexCoord2f(1,0);glVertex2f(1,0)
    glTexCoord2f(1,1);glVertex2f(1,1)
    glTexCoord2f(0,1);glVertex2f(0,1)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glMatrixMode(GL_MODELVIEW);  glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

# ==========================
# POSE ARUCO → OPENGL
# ==========================
def build_projection(fx,fy,cx,cy,w,h,near=0.001,far=2000.0):
    return np.array([
        [2*fx/w,    0,(w-2*cx)/w,                   0],
        [0,    2*fy/h,(h-2*cy)/h,                   0],
        [0,         0,-(far+near)/(far-near),-2*far*near/(far-near)],
        [0,         0,          -1,                  0],
    ],dtype=np.float64)

def get_modelview(rvec,tvec):
    R,_ = cv2.Rodrigues(rvec.reshape(3,1))
    mat = np.eye(4,dtype=np.float64)
    mat[:3,:3] = R
    mat[:3, 3] = tvec.flatten()
    mat = np.diag([1,-1,-1,1]).astype(np.float64) @ mat
    return mat.T.flatten()

def smooth_pose(rvec, tvec):
    """Filtro exponencial sobre rvec y tvec — elimina el temblor."""
    global _rvec_smooth, _tvec_smooth
    rv = rvec.flatten()
    tv = tvec.flatten()
    if _rvec_smooth is None:
        _rvec_smooth = rv.copy()
        _tvec_smooth = tv.copy()
    else:
        _rvec_smooth = SMOOTH_ALPHA*rv + (1-SMOOTH_ALPHA)*_rvec_smooth
        _tvec_smooth = SMOOTH_ALPHA*tv + (1-SMOOTH_ALPHA)*_tvec_smooth
    return _rvec_smooth.reshape(3,1), _tvec_smooth.reshape(3,1)

# ==========================
# ANIMACIONES
# ==========================
def update(dt):
    global t,molino_angulo,rio_onda,globo_fase
    t+=dt; molino_angulo=(molino_angulo+60*dt)%360
    rio_onda+=dt*1.5; globo_fase+=dt
    for i in range(5):
        nubes_off[i]+=nubes_vel[i]*dt*30
        if nubes_off[i]>120: nubes_off[i]=-120
    for p in pajaros:
        p[0]+=2.5*dt; p[3]+=dt*8
        if p[0]>70: p[0]=-70
    for a in autos_anim:
        a[0]+=a[3]
        if a[0]>65: a[0]=-65
    for p in personas:
        p[0]+=p[3]*0.4*dt; p[2]+=dt*3
        if p[0]>60: p[0]=-60
        if p[0]<-60: p[0]=60
    caballo[0]+=1.2*dt; caballo[2]+=dt*4
    if caballo[0]>40: caballo[0]=-20
    for o in ovejas:
        o[0]+=o[3]*0.5*dt; o[2]+=dt*2
        if o[0]>35: o[3]=-1
        if o[0]<5:  o[3]=1
    perro_st[0]+=perro_st[3]*0.8*dt; perro_st[2]+=dt*5
    if perro_st[0]>30:  perro_st[3]=-1
    if perro_st[0]<-10: perro_st[3]=1

# ==========================
# MEDIAPIPE GESTOS
# ==========================
def process_hand_gestures(frame_rgb):
    global zoom_factor,pan_offset
    global _pinch_dist_prev,_pinch_active,_pan_prev_pos,_pan_active
    results = hands_detector.process(frame_rgb)
    h,w = frame_rgb.shape[:2]
    annotated = frame_rgb.copy()
    if not results.multi_hand_landmarks:
        _pinch_dist_prev=None; _pinch_active=False
        _pan_prev_pos=None;    _pan_active=False
        return annotated
    lm = results.multi_hand_landmarks[0]
    mp_drawing.draw_landmarks(annotated,lm,mp_hands.HAND_CONNECTIONS)
    thumb = lm.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index = lm.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    wrist = lm.landmark[mp_hands.HandLandmark.WRIST]
    pinch_dist = math.hypot(thumb.x-index.x, thumb.y-index.y)
    cx=int((thumb.x+index.x)/2*w); cy=int((thumb.y+index.y)/2*h)
    if pinch_dist < PINCH_THRESHOLD:
        cv2.circle(annotated,(cx,cy),18,(0,255,100),3)
        cv2.putText(annotated,f"ZOOM x{zoom_factor:.1f}",(cx+22,cy),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,100),2)
        if _pinch_active and _pinch_dist_prev is not None:
            delta = pinch_dist-_pinch_dist_prev
            zoom_factor *= (1.0+delta*25.0)
            zoom_factor  = max(0.05,min(zoom_factor,100.0))
        _pinch_dist_prev=pinch_dist; _pinch_active=True
        _pan_active=False; _pan_prev_pos=None
    elif pinch_dist > PAN_OPEN_THR:
        px2=wrist.x; py2=wrist.y
        cv2.circle(annotated,(int(px2*w),int(py2*h)),22,(255,180,0),3)
        cv2.putText(annotated,"MOVER",(int(px2*w)+25,int(py2*h)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,180,0),2)
        if _pan_active and _pan_prev_pos is not None:
            dx=px2-_pan_prev_pos[0]; dy=py2-_pan_prev_pos[1]
            sens=0.3/zoom_factor
            pan_offset[0]+=dx*sens; pan_offset[1]-=dy*sens
        _pan_prev_pos=(px2,py2); _pan_active=True
        _pinch_active=False; _pinch_dist_prev=None
    else:
        _pinch_active=False; _pinch_dist_prev=None
        _pan_active=False;   _pan_prev_pos=None
    return annotated

# ==========================
# MAIN
# ==========================
def main():
    global zoom_factor,pan_offset,_rvec_smooth,_tvec_smooth
    if not glfw.init():
        print("ERROR GLFW"); return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    window = glfw.create_window(VIEW_W,VIEW_H,"Paisaje AR — ArUco",None,None)
    if not window:
        print("ERROR ventana"); glfw.terminate(); return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    def key_cb(win,key,sc2,action,mods):
        global zoom_factor,_rvec_smooth,_tvec_smooth
        if key==glfw.KEY_ESCAPE and action==glfw.PRESS:
            glfw.set_window_should_close(win,True)
        if action in (glfw.PRESS,glfw.REPEAT):
            if key==glfw.KEY_R:
                zoom_factor=4.0; pan_offset[:]=[0,0,0]
                _rvec_smooth=None; _tvec_smooth=None
            if key in (glfw.KEY_EQUAL,glfw.KEY_KP_ADD):
                zoom_factor=min(zoom_factor*1.1,100.0)
            if key in (glfw.KEY_MINUS,glfw.KEY_KP_SUBTRACT):
                zoom_factor=max(zoom_factor*0.9,0.05)
    glfw.set_key_callback(window,key_cb)

    glEnable(GL_DEPTH_TEST)
    init_bg_texture()
    fx=camera_matrix[0,0]; fy=camera_matrix[1,1]
    cx=camera_matrix[0,2]; cy=camera_matrix[1,2]
    proj=build_projection(fx,fy,cx,cy,VIEW_W,VIEW_H)
    last_time=glfw.get_time()

    print("="*55)
    print("  PAISAJE AR — ArUco ")
    print(f"  Marcador: {MARKER_SIZE*100:.0f} cm")
    print("  Pinch dedos    → ZOOM")
    print("  Mano abierta   → MOVER")
    print("  + / -          → Zoom teclado")
    print("  R              → Reset")
    print("  ESC            → Salir")
    print("="*55)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        now=glfw.get_time(); dt=now-last_time
        if dt<1/60: continue
        last_time=now
        update(dt)

        ret,frame=cap.read()
        if not ret: continue
        frame=cv2.flip(frame,1)

        # MediaPipe gestos
        frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame_rgb=process_hand_gestures(frame_rgb)
        frame=cv2.cvtColor(frame_rgb,cv2.COLOR_RGB2BGR)

        # Detección ArUco
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        corners,ids,_=aruco_detector.detectMarkers(gray)

        marker_found=False; current_mv=None

        if ids is not None and len(ids)>0:
            img_pts=corners[0][0].astype(np.float32)
            ok,rvec,tvec=cv2.solvePnP(
                obj_pts,img_pts,camera_matrix,dist_coeffs,
                flags=cv2.SOLVEPNP_IPPE_SQUARE)
            if ok:
                # ESTABILIZACIÓN: filtro exponencial sobre rvec y tvec
                rvec_s,tvec_s = smooth_pose(rvec,tvec)
                tvec_zoom = tvec_s.flatten()/zoom_factor
                current_mv = get_modelview(rvec_s,tvec_zoom)
                marker_found=True
                aruco.drawDetectedMarkers(frame,corners,ids)
                cv2.drawFrameAxes(frame,camera_matrix,dist_coeffs,
                                  rvec,tvec,MARKER_SIZE*0.4)
                cv2.putText(frame,"MARCADOR DETECTADO",(20,45),
                            cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0),2)
        else:
            # Resetear suavizado cuando se pierde el marcador
            _rvec_smooth=None; _tvec_smooth=None
            cv2.putText(frame,"Buscando ArUco...",(20,45),
                        cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,120,255),2)

        # Render OpenGL
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_background(frame)
        glMatrixMode(GL_PROJECTION); glLoadMatrixd(proj.T.flatten())
        glMatrixMode(GL_MODELVIEW);  glLoadIdentity()

        if marker_found and current_mv is not None:
            glPushMatrix()
            glLoadMatrixd(current_mv)
            glTranslatef(pan_offset[0],pan_offset[1],pan_offset[2])
            glRotatef(90,1,0,0)
            draw_scene_3d()
            glPopMatrix()

        glfw.swap_buffers(window)

    cap.release()
    hands_detector.close()
    glfw.terminate()
    print("Saliendo...")

if __name__=="__main__":
    main()
PYEOF
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import mediapipe as mp
import cv2
import numpy as np
import math
import random

# ==========================
# CONFIGURACION
# ==========================
VIEW_W = 1280
VIEW_H = 720

cam_x   = 0.0
cam_y   = 2.0
cam_z   = 10.0
cam_yaw = 0.0

random.seed(42)
np.random.seed(42)

# ==========================
# ESTADO DE ANIMACION
# ==========================
t = 0.0  

# Autos animados: [x_actual, z, color, velocidad, carril_z]
autos_anim = [
    [-10.0, 6.5, (0,0,220),  0.12, 6.5],
    [ -4.0, 7.5, (220,0,0),  0.09, 7.5],
    [  3.0, 6.5, (0,220,220),0.11, 6.5],
    [ 20.0, 7.5, (255,200,0),0.08, 7.5],
    [-30.0, 6.5, (180,0,180),0.13, 6.5],
]

# Nubes: [x_offset]
nubes_base = [(-30,18,-30),(-10,20,-28),(15,19,-32),(30,17,-29),(5,21,-35)]
nubes_vel  = [0.02, 0.015, 0.025, 0.018, 0.022]
nubes_off  = [0.0]*5

# Pájaros: [x, y, z, fase]
pajaros = [
    [-20.0, 12.0, -15.0, 0.0],
    [ -5.0, 14.0, -18.0, 1.2],
    [ 10.0, 11.5, -12.0, 2.4],
    [ 25.0, 13.0, -20.0, 0.8],
    [ -35.0,10.5, -10.0, 1.6],
    [  0.0, 15.0, -25.0, 3.0],
]

semaforos_x = [-20, -5, 15, 35]

farolas_x = list(range(-55, 60, 10))

# Personas: [x, z, fase_caminar, dir]
personas = [
    [-12.0, 4.0, 0.0,  1],
    [  5.0, 4.0, 1.5, -1],
    [ 18.0, 4.0, 0.8,  1],
    [-28.0, 4.0, 2.1, -1],
    [ 32.0, 4.0, 0.3,  1],
]

# Caballo: posición y fase
caballo = [-5.0, -8.0, 0.0]   # x, z, fase
# Ovejas: lista [x, z, fase, dir]
ovejas = [
    [10.0, -8.0, 0.0,  1],
    [13.0, -9.0, 1.0, -1],
    [16.0, -8.5, 2.0,  1],
]
# Perro: [x, z, fase, dir]
perro_state = [-8.0, -7.0, 0.0, 1]

# Globo aerostático: fase
globo_fase = 0.0

# Molino: ángulo de aspas
molino_angulo = 0.0

# Río: offset ondas
rio_onda = 0.0

# ==========================
# MEDIAPIPE
# ==========================
mp_hands = mp.solutions.hands
hands_mp = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ==========================
# PRIMITIVAS 3D
# ==========================

def set_color(r, g, b):
    glColor3f(r/255.0, g/255.0, b/255.0)

def draw_box(x, y, z, w, h, d, color):
    r,g,b = color
    x0,x1 = x-w/2, x+w/2
    y0,y1 = y,     y+h
    z0,z1 = z-d/2, z+d/2
    glBegin(GL_QUADS)
    set_color(r,g,b);                     glVertex3f(x0,y0,z1);glVertex3f(x1,y0,z1);glVertex3f(x1,y1,z1);glVertex3f(x0,y1,z1)
    set_color(int(r*.8),int(g*.8),int(b*.8)); glVertex3f(x1,y0,z0);glVertex3f(x0,y0,z0);glVertex3f(x0,y1,z0);glVertex3f(x1,y1,z0)
    set_color(int(r*.7),int(g*.7),int(b*.7)); glVertex3f(x0,y0,z0);glVertex3f(x0,y0,z1);glVertex3f(x0,y1,z1);glVertex3f(x0,y1,z0)
    set_color(int(r*.9),int(g*.9),int(b*.9)); glVertex3f(x1,y0,z1);glVertex3f(x1,y0,z0);glVertex3f(x1,y1,z0);glVertex3f(x1,y1,z1)
    set_color(min(255,int(r*1.1)),min(255,int(g*1.1)),min(255,int(b*1.1))); glVertex3f(x0,y1,z1);glVertex3f(x1,y1,z1);glVertex3f(x1,y1,z0);glVertex3f(x0,y1,z0)
    set_color(int(r*.5),int(g*.5),int(b*.5)); glVertex3f(x0,y0,z0);glVertex3f(x1,y0,z0);glVertex3f(x1,y0,z1);glVertex3f(x0,y0,z1)
    glEnd()

def draw_pyramid(x,y,z,bw,bd,h,color):
    r,g,b = color
    x0,x1 = x-bw/2,x+bw/2
    z0,z1 = z-bd/2,z+bd/2
    tx,ty,tz = x,y+h,z
    glBegin(GL_TRIANGLES)
    set_color(r,g,b);                     glVertex3f(x0,y,z1);glVertex3f(x1,y,z1);glVertex3f(tx,ty,tz)
    set_color(int(r*.7),int(g*.7),int(b*.7)); glVertex3f(x1,y,z0);glVertex3f(x0,y,z0);glVertex3f(tx,ty,tz)
    set_color(int(r*.85),int(g*.85),int(b*.85));glVertex3f(x0,y,z0);glVertex3f(x0,y,z1);glVertex3f(tx,ty,tz)
    set_color(int(r*.9),int(g*.9),int(b*.9)); glVertex3f(x1,y,z1);glVertex3f(x1,y,z0);glVertex3f(tx,ty,tz)
    glEnd()
    glBegin(GL_QUADS)
    set_color(int(r*.5),int(g*.5),int(b*.5)); glVertex3f(x0,y,z0);glVertex3f(x1,y,z0);glVertex3f(x1,y,z1);glVertex3f(x0,y,z1)
    glEnd()

def draw_cylinder(x,y,z,radius,height,color,segments=16):
    r,g,b = color
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        a = 2*math.pi*i/segments
        cx = x+radius*math.cos(a); cz = z+radius*math.sin(a)
        shade = 0.7+0.3*math.cos(a)
        glColor3f(r/255*shade,g/255*shade,b/255*shade)
        glVertex3f(cx,y,cz); glVertex3f(cx,y+height,cz)
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    set_color(min(255,int(r*1.2)),min(255,int(g*1.2)),min(255,int(b*1.2)))
    glVertex3f(x,y+height,z)
    for i in range(segments+1):
        a=2*math.pi*i/segments; glVertex3f(x+radius*math.cos(a),y+height,z+radius*math.sin(a))
    glEnd()

def draw_sphere(x,y,z,radius,color,stacks=8,slices=8):
    r,g,b = color
    for i in range(stacks):
        lat0=math.pi*(-0.5+i/stacks); lat1=math.pi*(-0.5+(i+1)/stacks)
        lz0,lzr0=math.sin(lat0),math.cos(lat0)
        lz1,lzr1=math.sin(lat1),math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(slices+1):
            lng=2*math.pi*j/slices; cx,cy=math.cos(lng),math.sin(lng)
            shade=0.7+0.3*lz1
            glColor3f(r/255*shade,g/255*shade,b/255*shade)
            glVertex3f(x+cx*lzr1*radius,y+lz1*radius,z+cy*lzr1*radius)
            glVertex3f(x+cx*lzr0*radius,y+lz0*radius,z+cy*lzr0*radius)
        glEnd()

# ==========================
# CIELO Y TERRENO
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

def draw_terrain():
    glBegin(GL_QUADS)
    set_color(50,180,50)
    glVertex3f(-60,0,-60);glVertex3f(60,0,-60);glVertex3f(60,0,60);glVertex3f(-60,0,60)
    glEnd()
    # Carretera
    glBegin(GL_QUADS); set_color(70,70,70)
    glVertex3f(-60,0.02,5);glVertex3f(60,0.02,5);glVertex3f(60,0.02,9);glVertex3f(-60,0.02,9)
    glEnd()
    for xi in range(-58,60,8):
        glBegin(GL_QUADS); set_color(255,255,255)
        glVertex3f(xi,0.03,6.8);glVertex3f(xi+4,0.03,6.8);glVertex3f(xi+4,0.03,7.2);glVertex3f(xi,0.03,7.2)
        glEnd()
    # Aceras
    glBegin(GL_QUADS); set_color(180,170,160)
    glVertex3f(-60,0.02,4);glVertex3f(60,0.02,4);glVertex3f(60,0.02,5);glVertex3f(-60,0.02,5)
    glEnd()
    glBegin(GL_QUADS); set_color(180,170,160)
    glVertex3f(-60,0.02,9);glVertex3f(60,0.02,9);glVertex3f(60,0.02,10);glVertex3f(-60,0.02,10)
    glEnd()

def draw_rio_animado():

    num_franjas = 20
    for i in range(num_franjas):
        fz = 15 + (i/num_franjas)*7
        offset = math.sin(fz*1.5 + rio_onda)*0.5
        r = int(80 + offset*20)
        g = int(120 + offset*15)
        b = int(220 + offset*10)
        glBegin(GL_QUADS)
        glColor3f(r/255,g/255,b/255)
        glVertex3f(-60,0.01,fz);glVertex3f(60,0.01,fz)
        glVertex3f(60,0.01,fz+7/num_franjas);glVertex3f(-60,0.01,fz+7/num_franjas)
        glEnd()

# ==========================
# SOL REALISTA con halo y rayos
# ==========================

def draw_sol_realista():
    sx,sy,sz = 25,18,-42
    # Halo exterior difuso
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    draw_sphere(sx,sy,sz, 6.0,(255,160,50),6,6)
    draw_sphere(sx,sy,sz, 4.5,(255,190,80),6,6)
    draw_sphere(sx,sy,sz, 3.0,(255,220,120),8,8)
    # Disco principal
    draw_sphere(sx,sy,sz, 2.0,(255,255,180),8,8)
    # Centro brillante
    draw_sphere(sx,sy,sz, 1.0,(255,255,255),8,8)
    # Rayos (líneas-cajas en 8 direcciones)
    for ang in range(0,360,30):
        rad = math.radians(ang)
        rx = sx + math.cos(rad)*5
        ry = sy + math.sin(rad)*5
        draw_box(sx+math.cos(rad)*3.5, sy+math.sin(rad)*3.5-0.05, sz,
                 0.08, 0.08, 0.08, (255,230,100))
    glDisable(GL_BLEND)

# ==========================
# MONTAÑAS Y NUBES
# ==========================

def draw_montanas():
    positions = [(-40,-22),(-20,-26),(0,-23),(20,-25),(40,-21),
                 (-50,-19),(-30,-24),(10,-22),(30,-24),(50,-20)]
    heights   = [9,11,10,12,9,8,10,9,11,8]
    colors    = [(160,140,130),(150,130,120),(170,155,140),(145,125,115),(165,145,135),
                 (155,135,125),(158,138,128),(162,142,132),(148,128,118),(168,148,138)]
    for (mx,mz),mh,mc in zip(positions,heights,colors):
        draw_pyramid(mx,0,mz,14,14,mh,mc)
        draw_pyramid(mx,0,mz-0.5,12,12,mh*0.95,(int(mc[0]*.9),int(mc[1]*.9),int(mc[2]*.9)))
        draw_pyramid(mx,mh*0.68,mz,3.5,3.5,mh*0.32,(255,255,255))

def draw_nubes_animadas():
    for i,(cx,cy,cz) in enumerate(nubes_base):
        ox = nubes_off[i]
        draw_sphere(cx+ox,   cy,   cz,  2.5,(255,255,255))
        draw_sphere(cx+ox+2, cy+1, cz,  2.0,(240,240,240))
        draw_sphere(cx+ox-2, cy+.5,cz,  2.0,(240,240,240))
        draw_sphere(cx+ox+1, cy,   cz+1,1.5,(250,250,250))
        draw_sphere(cx+ox,   cy+1.5,cz, 1.8,(245,245,245))

# ==========================
# PAJAROS ANIMADOS
# ==========================

def draw_pajaro(x,y,z,fase):
    # Cuerpo
    draw_sphere(x,y,z, 0.18,(30,30,30))
    # Alas batiendo
    ala = math.sin(fase)*0.3
    glBegin(GL_TRIANGLES)
    set_color(20,20,20)
    # Ala izquierda
    glVertex3f(x,y,z-0.18)
    glVertex3f(x-0.6,y+ala,z-0.1)
    glVertex3f(x-0.3,y,z-0.05)
    # Ala derecha
    glVertex3f(x,y,z+0.18)
    glVertex3f(x+0.6,y+ala,z+0.1)
    glVertex3f(x+0.3,y,z+0.05)
    glEnd()

def draw_pajaros():
    for p in pajaros:
        draw_pajaro(p[0],p[1],p[2],p[3])

# ==========================
# GLOBO AEROSTÁTICO
# ==========================

def draw_globo():
    gx = 5 + math.sin(globo_fase*0.3)*8
    gy = 16 + math.sin(globo_fase*0.5)*2
    gz = -22
    # Cesta
    draw_box(gx,gy-3,gz, 0.8,0.6,0.8,(139,90,43))
    # Cuerdas (4 esquinas)
    for ox,oz in [(-0.3,-0.3),(0.3,-0.3),(-0.3,0.3),(0.3,0.3)]:
        draw_box(gx+ox,gy-2.5,gz+oz, 0.04,2.5,0.04,(100,70,30))
    # Globo (esferas multicapa = colores por bandas)
    draw_sphere(gx,gy,gz, 2.5,(220,50,50))
    draw_sphere(gx,gy,gz, 2.3,(255,255,50))
    draw_sphere(gx,gy+0.5,gz, 2.0,(50,50,220))
    draw_sphere(gx,gy-0.5,gz, 2.0,(50,200,50))
    # Quemador (luz naranja)
    draw_sphere(gx,gy-1.8,gz, 0.3,(255,150,0))

# ==========================
# SEMÁFOROS
# ==========================

def draw_semaforo(x, z):
    # Poste
    draw_box(x,0,z, 0.12,3.5,0.12,(60,60,60))
    # Caja semáforo
    draw_box(x,3.3,z, 0.3,0.9,0.3,(40,40,40))
    # Luz roja (parpadea con tiempo)
    fase_sem = int(t*0.5) % 3
    cr = (220,0,0)   if fase_sem==0 else (60,0,0)
    ca = (220,180,0) if fase_sem==1 else (60,50,0)
    cv2c=(0,200,0)   if fase_sem==2 else (0,60,0)
    draw_sphere(x,3.9,z, 0.1,cr)
    draw_sphere(x,3.6,z, 0.1,ca)
    draw_sphere(x,3.3,z, 0.1,cv2c)

# ==========================
# FAROLAS
# ==========================

def draw_farola(x, z):
    draw_box(x,0,z, 0.1,4.0,0.1,(80,80,80))
    # Brazo curvo (aproximado)
    draw_box(x+0.5,3.9,z, 1.0,0.08,0.08,(80,80,80))
    # Lámpara
    draw_sphere(x+1.0,3.9,z, 0.2,(255,240,180))
    draw_sphere(x+1.0,3.9,z, 0.15,(255,255,220))

# ==========================
# PERSONAS CAMINANDO
# ==========================

def draw_persona(x, z, fase):
    # Piernas con balanceo
    pierna = math.sin(fase)*0.25
    draw_box(x-0.1,0,z+pierna,  0.15,0.7,0.15,(50,50,150))
    draw_box(x+0.1,0,z-pierna,  0.15,0.7,0.15,(50,50,150))
    # Cuerpo
    draw_box(x,0.7,z, 0.35,0.6,0.25,(200,100,50))
    # Brazos
    brazo = math.sin(fase)*0.2
    draw_box(x-0.25,0.85,z+brazo, 0.12,0.5,0.12,(220,160,100))
    draw_box(x+0.25,0.85,z-brazo, 0.12,0.5,0.12,(220,160,100))
    # Cabeza
    draw_sphere(x,1.45,z, 0.22,(220,160,110))

# ==========================
# ANIMALES
# ==========================

def draw_perro(x, z, fase):
    # Cuerpo
    draw_box(x,0.35,z, 0.9,0.4,0.45,(180,140,80))
    # Cabeza
    draw_sphere(x+0.5,0.8,z, 0.28,(190,150,90))
    # Hocico
    draw_box(x+0.72,0.68,z, 0.22,0.15,0.2,(200,160,100))
    # Ojo
    draw_sphere(x+0.68,0.85,z+0.12, 0.05,(0,0,0))
    draw_sphere(x+0.68,0.85,z-0.12, 0.05,(0,0,0))
    # Orejas
    draw_box(x+0.42,0.98,z+0.2, 0.12,0.2,0.18,(160,120,60))
    draw_box(x+0.42,0.98,z-0.2, 0.12,0.2,0.18,(160,120,60))
    # Patas
    p = math.sin(fase)*0.15
    draw_box(x+0.3, 0,z+0.18+p, 0.15,0.38,0.15,(170,130,70))
    draw_box(x+0.3, 0,z-0.18-p, 0.15,0.38,0.15,(170,130,70))
    draw_box(x-0.3, 0,z+0.18-p, 0.15,0.38,0.15,(170,130,70))
    draw_box(x-0.3, 0,z-0.18+p, 0.15,0.38,0.15,(170,130,70))
    # Cola
    draw_box(x-0.5,0.55,z, 0.06,0.06,0.4,(160,120,60))

def draw_oveja(x, z, fase):
    # Cuerpo esponjoso
    draw_sphere(x,0.55,z, 0.55,(240,240,240))
    draw_sphere(x+0.2,0.6,z+0.25, 0.35,(235,235,235))
    draw_sphere(x+0.2,0.6,z-0.25, 0.35,(235,235,235))
    # Cabeza
    draw_sphere(x+0.65,0.7,z, 0.28,(220,210,200))
    # Ojos
    draw_sphere(x+0.85,0.78,z+0.12, 0.05,(0,0,0))
    draw_sphere(x+0.85,0.78,z-0.12, 0.05,(0,0,0))
    # Patas
    p = math.sin(fase)*0.1
    for ox,oz in [(0.25,0.2),(0.25,-0.2),(-0.25,0.2),(-0.25,-0.2)]:
        draw_box(x+ox, 0,z+oz, 0.12,0.4,0.12,(200,190,180))

def draw_caballo(x, z, fase):
    # Cuerpo
    draw_box(x,0.9,z, 2.2,1.0,1.0,(140,100,60))
    # Cuello
    draw_box(x+1.0,1.2,z, 0.5,1.0,0.55,(145,105,65))
    # Cabeza
    draw_box(x+1.3,2.0,z, 0.9,0.6,0.5,(140,100,60))
    # Hocico
    draw_box(x+1.8,1.9,z, 0.4,0.35,0.45,(150,110,70))
    # Ojo
    draw_sphere(x+1.7,2.2,z+0.28, 0.07,(0,0,0))
    draw_sphere(x+1.7,2.2,z-0.28, 0.07,(0,0,0))
    # Crin
    draw_box(x+0.7,2.2,z, 1.3,0.15,0.12,(80,50,20))
    # Patas
    p = math.sin(fase)*0.2
    draw_box(x+0.6, 0,z+0.38+p, 0.22,0.92,0.22,(120,85,45))
    draw_box(x+0.6, 0,z-0.38-p, 0.22,0.92,0.22,(120,85,45))
    draw_box(x-0.6, 0,z+0.38-p, 0.22,0.92,0.22,(120,85,45))
    draw_box(x-0.6, 0,z-0.38+p, 0.22,0.92,0.22,(120,85,45))
    # Cola
    draw_box(x-1.1,1.2,z, 0.08,0.08,0.7,(80,50,20))
    draw_sphere(x-1.1,1.2,z+0.75, 0.18,(70,45,15))

# ==========================
# LAGO
# ==========================

def draw_lago(x,z):
    glBegin(GL_QUADS); set_color(60,170,60)
    glVertex3f(x-5,0.01,z-4);glVertex3f(x+5,0.01,z-4);glVertex3f(x+5,0.01,z+4);glVertex3f(x-5,0.01,z+4)
    glEnd()
    glBegin(GL_QUADS); set_color(100,140,200)
    glVertex3f(x-4,0.02,z-3);glVertex3f(x+4,0.02,z-3);glVertex3f(x+4,0.02,z+3);glVertex3f(x-4,0.02,z+3)
    glEnd()
    # Reflejo del sol
    rf = abs(math.sin(rio_onda*0.5))*0.4+0.6
    glBegin(GL_QUADS)
    glColor3f(rf,rf*0.9,0.3)
    glVertex3f(x-1.5,0.03,z-0.8);glVertex3f(x+1.5,0.03,z-0.8);glVertex3f(x+1.5,0.03,z+0.8);glVertex3f(x-1.5,0.03,z+0.8)
    glEnd()

# ==========================
# PUENTE
# ==========================

def draw_puente(x,z):
    draw_box(x,0.5,z,14,0.3,2.0,(90,90,90))
    for px in range(-6,7,2):
        draw_box(x+px,0.5,z-1.0,0.15,2.0,0.15,(50,50,50))
        draw_box(x+px,0.5,z+1.0,0.15,2.0,0.15,(50,50,50))
    draw_box(x,2.3,z-1.0,14,0.1,0.1,(60,60,60))
    draw_box(x,2.3,z+1.0,14,0.1,0.1,(60,60,60))

# ==========================
# EDIFICIOS
# ==========================

def draw_casa(x,z):
    draw_box(x+0.1,0,z+0.1,3.6,0.05,3.1,(80,80,80))
    draw_box(x,0,z,3.5,2.5,3.0,(200,220,240))
    draw_box(x+1.5,0,z,0.5,2.5,3.0,(170,190,210))
    draw_pyramid(x,2.5,z,4.0,3.5,1.5,(120,40,40))
    draw_box(x,0,z+1.51,0.6,1.2,0.05,(90,60,40))
    draw_box(x,0.1,z+1.52,0.5,1.0,0.04,(130,90,60))
    for wx in [-0.9,0.9]:
        draw_box(x+wx,1.0,z+1.51,0.7,0.6,0.05,(230,230,230))
        draw_box(x+wx,1.05,z+1.52,0.6,0.5,0.04,(180,220,255))
        draw_box(x+wx,1.0,z+1.53,0.05,0.6,0.03,(80,80,80))
        draw_box(x+wx,1.3,z+1.53,0.7,0.05,0.03,(80,80,80))

def draw_escuela(x,z):
    draw_box(x+0.15,0,z+0.15,5.1,0.05,4.1,(80,80,80))
    draw_box(x,0,z,5.0,3.5,4.0,(180,220,255))
    draw_box(x-2.4,0,z,0.12,3.5,4.0,(220,240,255))
    draw_pyramid(x,3.5,z,5.5,4.5,1.8,(40,40,180))
    draw_box(x,0,z+2.01,0.8,1.8,0.05,(80,120,160))
    draw_box(x+0.25,0.85,z+2.03,0.08,0.08,0.03,(0,220,220))
    for wx in [-1.5,-0.5,0.5,1.5]:
        draw_box(x+wx,2.0,z+2.01,0.6,0.6,0.05,(255,255,255))
        draw_box(x+wx,2.05,z+2.02,0.5,0.5,0.04,(255,255,200))
        draw_box(x+wx,2.0,z+2.03,0.04,0.6,0.03,(0,0,0))
        draw_box(x+wx,2.3,z+2.03,0.6,0.04,0.03,(0,0,0))
    draw_box(x,3.55,z+2.0,2.5,0.5,0.08,(255,255,255))

def draw_hospital(x,z):
    draw_box(x+0.15,0,z+0.15,5.1,0.05,4.1,(90,90,90))
    draw_box(x,0,z,5.0,4.0,4.0,(245,245,245))
    draw_box(x-2.4,0,z,0.1,4.0,4.0,(255,255,255))
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
    draw_box(x+0.12,0,z+0.12,4.1,0.05,4.1,(80,80,80))
    draw_box(x,0,z,4.0,3.5,4.0,(220,220,220))
    draw_box(x-1.9,0,z,0.08,3.5,4.0,(245,245,245))
    draw_pyramid(x,3.5,z,4.5,4.5,2.0,(60,60,160))
    draw_box(x,3.5,z,1.0,3.0,1.0,(170,170,170))
    draw_pyramid(x,6.5,z,1.2,1.2,1.5,(60,60,160))
    draw_box(x,7.8,z,0.1,1.0,0.1,(0,220,220))
    draw_box(x,8.3,z,0.5,0.1,0.1,(0,220,220))
    draw_box(x,0,z+2.01,0.7,1.5,0.05,(70,90,140))
    draw_box(x-1.2,1.2,z+2.01,0.5,1.2,0.06,(200,60,60))
    draw_box(x+1.2,1.2,z+2.01,0.5,1.2,0.06,(60,100,200))

def draw_granja(x,z):
    draw_box(x+0.15,0,z+0.15,5.1,0.05,4.1,(70,70,70))
    draw_box(x,0,z,5.0,3.5,4.0,(40,40,180))
    draw_pyramid(x,3.5,z,5.5,4.5,2.0,(20,20,120))
    draw_box(x,0,z+2.01,1.2,2.0,0.05,(80,120,180))
    draw_cylinder(x+3.2,0,z,0.7,4.5,(180,180,180))
    draw_pyramid(x+3.2,4.5,z,1.6,1.6,0.8,(200,200,200))
    for fi in range(-4,5):
        draw_box(x+fi*1.0,0,z+3.5,0.08,1.0,0.08,(80,120,180))
    draw_box(x,0.6,z+3.5,8.0,0.08,0.08,(80,120,180))
    draw_box(x,0.3,z+3.5,8.0,0.08,0.08,(80,120,180))

def draw_molino_animado(x,z):
    draw_box(x,0,z,2.0,5.0,2.0,(170,190,220))
    draw_pyramid(x,5.0,z,2.2,2.2,1.5,(50,50,150))
    draw_box(x,0,z+1.01,0.5,1.2,0.05,(80,120,160))
    draw_box(x,1.8,z+1.01,0.5,0.5,0.05,(255,255,255))
    draw_box(x,3.0,z+1.01,0.5,0.5,0.05,(255,255,255))
    draw_sphere(x,5.5,z+1.1,0.25,(120,120,120))
    # Aspas girando
    glPushMatrix()
    glTranslatef(x, 5.5, z+1.1)
    glRotatef(molino_angulo, 0, 0, 1)
    glTranslatef(-x, -5.5, -(z+1.1))
    draw_box(x,5.5,z+1.1,0.12,3.5,0.08,(255,255,255))
    draw_box(x,5.5,z+1.1,3.5,0.12,0.08,(255,255,255))
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, 5.5, z+1.1)
    glRotatef(molino_angulo+45, 0, 0, 1)
    glTranslatef(-x, -5.5, -(z+1.1))
    draw_box(x,5.5,z+1.1,0.1,3.0,0.07,(220,220,220))
    draw_box(x,5.5,z+1.1,3.0,0.1,0.07,(220,220,220))
    glPopMatrix()

def draw_estadio(x,z):
    draw_box(x+0.2,0,z+0.2,9.5,0.05,7.5,(80,80,80))
    for i in range(16):
        a=2*math.pi*i/16
        draw_box(x+4.5*math.cos(a),0,z+3.0*math.sin(a),1.2,2.0,1.2,(160,160,160))
    for i in range(16):
        a=2*math.pi*i/16
        draw_box(x+3.5*math.cos(a),0,z+2.2*math.sin(a),0.9,1.5,0.9,(130,130,130))
    glBegin(GL_QUADS); set_color(50,200,50)
    glVertex3f(x-3,0.01,z-2);glVertex3f(x+3,0.01,z-2);glVertex3f(x+3,0.01,z+2);glVertex3f(x-3,0.01,z+2)
    glEnd()
    glBegin(GL_QUADS); set_color(255,255,255)
    glVertex3f(x-.05,0.02,z-2);glVertex3f(x+.05,0.02,z-2);glVertex3f(x+.05,0.02,z+2);glVertex3f(x-.05,0.02,z+2)
    glEnd()
    for px in [-3.0,3.0]:
        draw_box(x+px,0,z,0.2,0.8,1.5,(255,255,255))
        draw_box(x+px,0.75,z,0.2,0.08,1.5,(255,255,255))
    for px in [-5.5,5.5]:
        draw_box(x+px,0,z,0.2,4.5,0.2,(120,120,120))
        draw_box(x+px,4.3,z,1.2,0.3,0.6,(220,220,220))

def draw_torre_agua(x,z):
    for ox,oz in [(-1,-1),(1,-1),(-1,1),(1,1)]:
        draw_box(x+ox*0.9,0,z+oz*0.9,0.18,5.0,0.18,(120,120,120))
    draw_box(x,2.5,z,2.2,0.1,0.1,(140,140,140))
    draw_box(x,2.5,z,0.1,0.1,2.2,(140,140,140))
    draw_cylinder(x,4.8,z,1.5,1.8,(200,200,200))
    draw_pyramid(x,6.6,z,3.2,3.2,0.8,(180,180,200))
    draw_box(x+1.7,0,z,0.05,5.0,0.05,(100,100,100))
    draw_box(x+1.95,0,z,0.05,5.0,0.05,(100,100,100))
    for yi in range(0,50,6):
        draw_box(x+1.82,yi/10.0,z,0.3,0.04,0.05,(100,100,100))

# Edificio moderno (rascacielos)
def draw_edificio_moderno(x,z):
    draw_box(x,0,z,4.0,12.0,4.0,(160,180,210))
    for piso in range(0,12):
        for col in range(3):
            draw_box(x-1.2+col*1.2,0.5+piso*1.0,z+2.01,0.6,0.5,0.04,(200,230,255))
    draw_box(x,12.0,z,0.2,1.5,0.2,(180,180,200))  # antena

# Banco de parque
def draw_banco(x,z):
    draw_box(x,0.4,z,1.5,0.08,0.5,(120,80,40))
    draw_box(x,0.6,z-0.2,1.5,0.08,0.08,(120,80,40))
    for px in [-0.6,0.6]:
        draw_box(x+px,0,z,0.08,0.65,0.08,(100,65,30))

# ==========================
# ÁRBOLES Y FLORES
# ==========================

def draw_arbol(x,z):
    draw_cylinder(x,0,z,0.2,1.5,(40,80,140))
    draw_sphere(x,  1.8,z,  1.2,(0,130,0))
    draw_sphere(x-.5,1.4,z, 1.0,(0,160,0))
    draw_sphere(x+.5,1.4,z, 1.0,(0,150,0))

def draw_arbol_pino(x,z):
    draw_cylinder(x,0,z,0.15,1.0,(80,50,20))
    draw_pyramid(x,0.8,z,2.0,2.0,2.5,(0,120,30))
    draw_pyramid(x,2.0,z,1.5,1.5,2.0,(0,140,40))
    draw_pyramid(x,3.2,z,1.0,1.0,1.5,(0,160,50))

def draw_arbol_palmera(x,z):
    # Tronco curvo (apilado)
    for i in range(5):
        draw_cylinder(x+i*0.05,i*0.8,z,0.15,0.85,(160,120,60))
    # Hojas
    for ang in range(0,360,60):
        rad = math.radians(ang)
        draw_box(x+0.25+math.cos(rad)*0.8,3.8+math.sin(rad)*0.2,z+math.sin(rad)*0.8,
                 1.2,0.06,0.08,(0,160,60))

def draw_flor(x,z,color1=(255,80,200),color2=(255,0,180)):
    draw_box(x,0,z,0.07,1.0,0.07,(0,160,0))
    draw_sphere(x,   1.1,z,   0.15,color1)
    draw_sphere(x+.2,1.0,z,   0.13,color2)
    draw_sphere(x-.2,1.0,z,   0.13,color2)
    draw_sphere(x,   1.0,z+.2,0.13,color2)
    draw_sphere(x,   1.0,z-.2,0.13,color2)
    draw_sphere(x,   1.05,z,  0.08,(0,220,255))

def draw_girasol(x,z):
    draw_box(x,0,z,0.08,1.5,0.08,(0,140,0))
    for ang in range(0,360,40):
        rad=math.radians(ang)
        draw_sphere(x+math.cos(rad)*0.2,1.7,z+math.sin(rad)*0.2,0.15,(255,200,0))
    draw_sphere(x,1.7,z,0.18,(80,40,0))

# ==========================
# AUTOS ANIMADOS
# ==========================

def draw_auto(x,z,color):
    draw_box(x,0,z,2.3,0.04,1.1,(50,50,50))
    draw_box(x,0.3,z,2.2,0.7,1.0,color)
    draw_box(x,1.0,z,1.4,0.6,0.9,color)
    draw_box(x,1.05,z+0.46,1.0,0.4,0.05,(180,220,255))
    draw_box(x,1.05,z-0.46,1.0,0.4,0.05,(180,220,255))
    draw_box(x,1.0,z+0.47,0.05,0.6,0.04,(80,80,80))
    for wx,wz in [(-0.7,-0.55),(0.7,-0.55),(-0.7,0.55),(0.7,0.55)]:
        draw_cylinder(x+wx,0,z+wz,0.3,0.25,(30,30,30))
        draw_cylinder(x+wx,0.01,z+wz,0.13,0.24,(180,180,180))
    draw_box(x+1.1,0.55,z+0.46,0.05,0.12,0.12,(200,255,255))
    draw_box(x+1.1,0.55,z-0.46,0.05,0.12,0.12,(200,255,255))
    draw_box(x-1.1,0.55,z+0.46,0.05,0.12,0.12,(0,0,220))
    draw_box(x-1.1,0.55,z-0.46,0.05,0.12,0.12,(0,0,220))
    draw_box(x+1.1,0.4,z,0.04,0.1,1.0,(180,180,180))
    draw_box(x+0.3,0.75,z+0.5,0.25,0.04,0.03,(200,200,200))

def draw_camion(x,z):
    draw_box(x,0,z,4.7,0.04,1.4,(50,50,50))
    draw_box(x-1.0,0.4,z,4.5,1.2,1.3,(255,120,0))
    draw_box(x+1.8,0.4,z,1.5,1.5,1.3,(200,60,0))
    draw_box(x+1.9,1.2,z,1.0,0.6,0.06,(220,220,220))
    draw_box(x+0.55,0.4,z,0.05,1.2,1.3,(0,0,0))
    for wx,wz in [(-1.5,-0.8),(0.0,-0.8),(1.5,-0.8),(-1.5,0.8),(0.0,0.8),(1.5,0.8)]:
        draw_cylinder(x+wx,0,z+wz,0.35,0.28,(30,30,30))
        draw_cylinder(x+wx,0.01,z+wz,0.15,0.27,(180,180,180))

def draw_vaca(x,z):
    draw_box(x,0,z,2.2,0.04,1.3,(0,0,0))
    draw_box(x,0.8,z,2.0,1.0,1.2,(255,255,255))
    draw_box(x+1.0,0.9,z,0.5,0.7,0.7,(255,255,255))
    draw_sphere(x+1.4,1.6,z,0.5,(255,255,255))
    draw_sphere(x+1.7,1.75,z+0.25,0.07,(0,0,0))
    draw_sphere(x+1.7,1.75,z-0.25,0.07,(0,0,0))
    draw_sphere(x+1.85,1.55,z,0.18,(200,180,180))
    draw_box(x+1.35,1.95,z+0.55,0.12,0.3,0.18,(255,255,255))
    draw_box(x+1.35,1.95,z-0.55,0.12,0.3,0.18,(255,255,255))
    draw_box(x-0.3,1.1,z+0.61,0.4,0.3,0.05,(0,0,0))
    draw_box(x+0.3,1.1,z+0.61,0.35,0.25,0.05,(0,0,0))
    for px,pz in [(-0.6,-0.4),(0.0,-0.4),(-0.6,0.4),(0.0,0.4)]:
        draw_box(x+px,0,z+pz,0.22,0.82,0.22,(240,240,240))
    draw_box(x-1.0,1.2,z,0.06,0.06,0.6,(0,0,0))
    draw_sphere(x-1.0,1.2,z+0.65,0.12,(0,0,0))

# ==========================
# POSICIONES FIJAS
# ==========================
casas_pos    = [(-25,-5),(-20,-5),(-14,-5),(-8,-5),(-35,-5),(-40,-5)]
arboles_pos  = [(x*4-55,-3) for x in range(28)]
pinos_pos    = [(x*5-50,-18) for x in range(20)]
palmeras_pos = [(-40,-2),(-38,-2),(38,-2),(40,-2)]
flores_pos   = [(x*3-55,11) for x in range(36)]
girasoles_pos= [(x*4-50,-11) for x in range(12)]
bancos_pos   = [(-15,3),(-5,3),(8,3),(22,3)]

# ==========================
# ACTUALIZAR ANIMACIONES
# ==========================

def update(dt):
    global t, molino_angulo, rio_onda, globo_fase

    t            += dt
    molino_angulo = (molino_angulo + 60*dt) % 360
    rio_onda     += dt * 1.5
    globo_fase   += dt

    # Nubes
    for i in range(5):
        nubes_off[i] += nubes_vel[i]*dt*30
        if nubes_off[i] > 120:
            nubes_off[i] = -120

    # Pájaros
    for p in pajaros:
        p[0] += 2.5*dt           # vuelan hacia la derecha
        p[3] += dt * 8           # baten alas
        if p[0] > 70: p[0] = -70

    # Autos animados en carretera
    for a in autos_anim:
        a[0] += a[3]
        if a[0] > 65: a[0] = -65

    # Personas caminando
    for p in personas:
        p[0] += p[3]*0.4*dt
        p[2] += dt*3
        if p[0] > 60:  p[0]=-60
        if p[0] < -60: p[0]=60

    # Caballo
    caballo[0] += 1.2*dt
    caballo[2] += dt*4
    if caballo[0] > 40: caballo[0] = -20

    # Ovejas
    for o in ovejas:
        o[0] += o[3]*0.5*dt
        o[2] += dt*2
        if o[0] > 35: o[3]=-1
        if o[0] < 5:  o[3]=1

    # Perro
    perro_state[0] += perro_state[3]*0.8*dt
    perro_state[2] += dt*5
    if perro_state[0] > 30: perro_state[3]=-1
    if perro_state[0] < -10: perro_state[3]=1

# ==========================
# DRAW SCENE
# ==========================

def draw_scene():
    draw_sky()
    glLoadIdentity()
    look_x = cam_x + math.sin(math.radians(cam_yaw))
    look_z = cam_z - math.cos(math.radians(cam_yaw))
    gluLookAt(cam_x,cam_y,cam_z, look_x,cam_y,look_z, 0,1,0)

    draw_montanas()
    draw_sol_realista()
    draw_nubes_animadas()
    draw_terrain()
    draw_rio_animado()
    draw_lago(-15,-12)
    draw_puente(0,18)

    # Edificios originales
    for bx,bz in casas_pos:
        draw_casa(bx,bz)
    draw_escuela(-2,-14)
    draw_hospital(6,-14)
    draw_iglesia(14,-14)
    draw_granja(22,-14)
    draw_molino_animado(30,-14)
    draw_estadio(20,-3)
    draw_torre_agua(35,0)
    # Nuevos
    draw_edificio_moderno(-42,-12)
    draw_edificio_moderno(-48,-12)

    # Bancos de parque
    for bx,bz in bancos_pos:
        draw_banco(bx,bz)

    # Árboles variados
    for tx,tz in arboles_pos:
        draw_arbol(tx,tz)
    for tx,tz in pinos_pos:
        draw_arbol_pino(tx,tz)
    for tx,tz in palmeras_pos:
        draw_arbol_palmera(tx,tz)

    # Flores variadas
    for i,(fx,fz) in enumerate(flores_pos):
        if i%3==0: draw_flor(fx,fz,(255,80,200),(255,0,180))
        elif i%3==1: draw_flor(fx,fz,(255,50,50),(220,0,0))
        else: draw_flor(fx,fz,(100,100,255),(50,50,220))
    for gx,gz in girasoles_pos:
        draw_girasol(gx,gz)

    # Autos animados
    for a in autos_anim:
        draw_auto(a[0],a[4],a[2])
    draw_camion(10,7)

    # Semáforos y farolas
    for sx in semaforos_x:
        draw_semaforo(sx,4.2)
    for fx in farolas_x:
        draw_farola(fx,3.5)

    # Personas
    for p in personas:
        draw_persona(p[0],p[1],p[2])

    # Animales
    draw_vaca(28,-5)
    draw_caballo(caballo[0],caballo[1],caballo[2])
    for o in ovejas:
        draw_oveja(o[0],o[1],o[2])
    draw_perro(perro_state[0],perro_state[1],perro_state[2])

    # Pájaros
    draw_pajaros()

    # Globo aerostático
    draw_globo()

# ==========================
# MAIN (GLFW)
# ==========================

def main():
    global cam_x, cam_y, cam_z, cam_yaw

    if not glfw.init():
        print("ERROR: No se pudo inicializar GLFW"); return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    window = glfw.create_window(VIEW_W,VIEW_H,"PAISAJE 3D PRO - Control con Mano",None,None)
    if not window:
        print("ERROR: No se pudo crear ventana GLFW"); glfw.terminate(); return

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    def key_callback(win,key,scancode,action,mods):
        if key==glfw.KEY_ESCAPE and action==glfw.PRESS:
            glfw.set_window_should_close(win,True)
    glfw.set_key_callback(window,key_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1,0.1,0.2,1.0)
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(60,VIEW_W/VIEW_H,0.1,300.0)
    glMatrixMode(GL_MODELVIEW)

    cam_speed=0.0; cam_turn=0.0; zoom_val=2.0
    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        now = glfw.get_time()
        dt  = now - last_time
        if dt < 1/60: continue
        last_time = now

        update(dt)

        ret,frame = cap.read()
        if ret:
            frame  = cv2.flip(frame,1)
            rgb    = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            result = hands_mp.process(rgb)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
                ix=hand.landmark[8].x; iy=hand.landmark[8].y
                cam_turn  = (ix-0.5)*4.0
                cam_speed = (0.5-iy)*3.0
                tx=hand.landmark[4].x; ty=hand.landmark[4].y
                dist=math.sqrt((ix-tx)**2+(iy-ty)**2)
                zoom_val=float(np.interp(dist,[0.03,0.25],[1.0,5.0]))
                cv2.putText(frame,f"Giro:{cam_turn:+.1f}",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                cv2.putText(frame,f"Vel:{cam_speed:+.1f}",(20,70),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
                cv2.putText(frame,f"Alt:{zoom_val:.1f}",(20,100),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2)
            else:
                cam_speed=0.0; cam_turn=0.0

            cv2.imshow("CAMARA (MediaPipe)",frame)
            cv2.waitKey(1)

        cam_yaw += cam_turn*0.8
        cam_x   += math.sin(math.radians(cam_yaw))*cam_speed*0.12
        cam_z   -= math.cos(math.radians(cam_yaw))*cam_speed*0.12
        cam_y    = zoom_val

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_scene()
        glfw.swap_buffers(window)

    cap.release()
    cv2.destroyAllWindows()
    glfw.terminate()

if __name__=="__main__":
    main()
PYEOF
Figuras con opengl

Introducción

El modelado tridimensional es una de las aplicaciones más importantes de la computación gráfica, ya que permite representar objetos y escenarios virtuales mediante figuras geométricas básicas. En esta práctica se utiliza OpenGL junto con GLFW para construir una pequeña colonia compuesta por varias casas tridimensionales, aplicando transformaciones, iluminación y renderizado en tiempo real.

El objetivo principal es comprender cómo se pueden combinar primitivas geométricas para crear modelos más complejos y cómo organizar múltiples objetos dentro de una misma escena 3D.

Descripción

El programa genera una escena tridimensional en la que se representa una colonia formada por varias casas distribuidas sobre un terreno plano. Para ello se emplean diferentes funciones que construyen cada parte de la vivienda, incluyendo paredes, techo, ventanas, puerta, chimenea, humo y detalles decorativos.

La escena utiliza iluminación básica para mejorar la apariencia visual de los objetos y generar una sensación de profundidad. Además, se implementa una cámara mediante la función gluLookAt, permitiendo observar la colonia desde una perspectiva elevada.

La casa principal se ubica en el centro de la escena y cuenta con un camino de acceso. Posteriormente se generan otras viviendas alrededor mediante transformaciones de traslación, rotación y escalado, creando la apariencia de un pequeño vecindario.

Finalmente, todas las construcciones se colocan sobre un terreno verde que representa el suelo de la colonia, proporcionando un entorno más completo y organizado.

Codigo
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_pos = [5, 10, 5, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ---------------- CASA BASE ----------------

def draw_cube():
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)

    faces = [
        (-1,0,1, 1,0,1, 1,1,1, -1,1,1),
        (-1,0,-1, 1,0,-1, 1,1,-1, -1,1,-1),
        (-1,0,-1, -1,0,1, -1,1,1, -1,1,-1),
        (1,0,-1, 1,0,1, 1,1,1, 1,1,-1)
    ]

    for f in faces:
        glVertex3f(f[0],f[1],f[2])
        glVertex3f(f[3],f[4],f[5])
        glVertex3f(f[6],f[7],f[8])
        glVertex3f(f[9],f[10],f[11])

    glColor3f(0.9,0.6,0.3)
    glVertex3f(-1,1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,1,1)
    glVertex3f(-1,1,1)

    glColor3f(0.6,0.4,0.2)
    glVertex3f(-1,0,-1)
    glVertex3f(1,0,-1)
    glVertex3f(1,0,1)
    glVertex3f(-1,0,1)

    glEnd()

def draw_roof():
    glBegin(GL_TRIANGLES)
    glColor3f(0.9,0.1,0.1)

    for v in [
        (-1,1,1, 1,1,1, 0,2,0),
        (-1,1,-1, 1,1,-1, 0,2,0),
        (-1,1,-1, -1,1,1, 0,2,0),
        (1,1,-1, 1,1,1, 0,2,0)
    ]:
        glVertex3f(v[0],v[1],v[2])
        glVertex3f(v[3],v[4],v[5])
        glVertex3f(v[6],v[7],v[8])

    glEnd()

# ---------------- DETALLES ----------------

def draw_base():
    glColor3f(0.5,0.3,0.2)
    glBegin(GL_QUADS)
    glVertex3f(-1.1,-0.05,1.1)
    glVertex3f(1.1,-0.05,1.1)
    glVertex3f(1.1,0,1.1)
    glVertex3f(-1.1,0,1.1)
    glEnd()

def draw_edges():
    glColor3f(0.4,0.2,0.1)
    glLineWidth(3)
    glBegin(GL_LINES)
    for x in [-1,1]:
        for z in [-1,1]:
            glVertex3f(x,0,z)
            glVertex3f(x,1,z)
    glEnd()
    glLineWidth(1)

def draw_wall_details():
    glColor3f(0.6,0.3,0.1)
    for y in [0.25,0.5,0.75]:
        glBegin(GL_LINES)
        glVertex3f(-1,y,1.01)
        glVertex3f(1,y,1.01)
        glEnd()

def draw_side_details():
    glColor3f(0.5,0.8,1.0)
    glBegin(GL_QUADS)
    glVertex3f(1.01,0.5,-0.5)
    glVertex3f(1.01,0.5,0)
    glVertex3f(1.01,0.8,0)
    glVertex3f(1.01,0.8,-0.5)
    glEnd()

def draw_windows():
    glColor3f(0.5,0.8,1.0)
    glBegin(GL_QUADS)
    glVertex3f(-0.8,0.5,1.01)
    glVertex3f(-0.4,0.5,1.01)
    glVertex3f(-0.4,0.8,1.01)
    glVertex3f(-0.8,0.8,1.01)

    glVertex3f(0.4,0.5,1.01)
    glVertex3f(0.8,0.5,1.01)
    glVertex3f(0.8,0.8,1.01)
    glVertex3f(0.4,0.8,1.01)
    glEnd()

def draw_door():
    glColor3f(0.3,0.1,0)
    glBegin(GL_QUADS)
    glVertex3f(-0.3,0,1.01)
    glVertex3f(0.3,0,1.01)
    glVertex3f(0.3,0.6,1.01)
    glVertex3f(-0.3,0.6,1.01)
    glEnd()

def draw_chimney():
    glColor3f(0.3,0.1,0.1)
    glBegin(GL_QUADS)
    glVertex3f(0.3,1.2,0.3)
    glVertex3f(0.6,1.2,0.3)
    glVertex3f(0.6,1.8,0.3)
    glVertex3f(0.3,1.8,0.3)
    glEnd()

def draw_smoke():
    glDisable(GL_LIGHTING)
    glColor3f(0.8,0.8,0.8)
    glBegin(GL_QUADS)
    glVertex3f(0.35,1.9,0.4)
    glVertex3f(0.55,1.9,0.4)
    glVertex3f(0.55,2.2,0.4)
    glVertex3f(0.35,2.2,0.4)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_path():
    glDisable(GL_LIGHTING)
    glColor3f(0.7,0.7,0.7)
    glBegin(GL_QUADS)
    glVertex3f(-0.5,0.01,1.5)
    glVertex3f(0.5,0.01,1.5)
    glVertex3f(0.5,0.01,4)
    glVertex3f(-0.5,0.01,4)
    glEnd()
    glEnable(GL_LIGHTING)

# ---------------- CASA ----------------

def draw_house_model():
    draw_base()
    draw_cube()
    draw_edges()
    draw_wall_details()
    draw_side_details()
    draw_roof()
    draw_door()
    draw_windows()
    draw_chimney()
    draw_smoke()

# ---------------- ESCENA ----------------

def draw_scene():
    # casa principal
    glPushMatrix()
    draw_house_model()
    draw_path()
    glPopMatrix()

    # casas alrededor
    houses = [
        (4,0,0, 0.8, 45),
        (-4,0,0, 1.2, -30),
        (0,0,4, 0.9, 90),
        (0,0,-4, 1.1, 180)
    ]

    for x,y,z,s,r in houses:
        glPushMatrix()
        glTranslatef(x,y,z)
        glScalef(s,s,s)
        glRotatef(r,0,1,0)
        draw_house_model()
        glPopMatrix()

# ---------------- SUELO ----------------

def draw_ground():
    glDisable(GL_LIGHTING)
    glColor3f(0.2,0.6,0.2)

    glBegin(GL_QUADS)
    glVertex3f(-20,0,20)
    glVertex3f(20,0,20)
    glVertex3f(20,0,-20)
    glVertex3f(-20,0,-20)
    glEnd()

    glEnable(GL_LIGHTING)

# ---------------- RENDER ----------------

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(8,6,12, 0,1,0, 0,1,0)

    draw_ground()
    draw_scene()

    glfw.swap_buffers(window)

# ---------------- MAIN ----------------

def main():
    global window

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800,600,"Colonia sin cielo",None,None)
    glfw.make_context_current(window)

    glViewport(0,0,800,600)
    init()

    while not glfw.window_should_close(window):
        render()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
    
Conclusión

Esta práctica permitió aplicar conceptos fundamentales de gráficos por computadora, como la creación de objetos tridimensionales mediante primitivas geométricas, el uso de iluminación, la manipulación de cámaras y la aplicación de transformaciones espaciales. Asimismo, se demostró cómo reutilizar un mismo modelo para construir escenas más complejas mediante cambios de posición, orientación y tamaño.

El resultado es una representación básica de una colonia en tres dimensiones que sirve como base para el desarrollo de escenarios más elaborados dentro de aplicaciones gráficas y proyectos de visualización 3D.
Actividad: Casa rotacion

Objetivo

Desarrollar una escena tridimensional utilizando Python, OpenGL y GLFW, aplicando conceptos de modelado, transformaciones, iluminación y visualización en gráficos por computadora.

Descripción

En esta actividad se creó una escena 3D compuesta por varias casas y árboles distribuidos sobre un terreno. Para la construcción de los objetos se utilizaron primitivas geométricas básicas de OpenGL, aplicando escalamiento, traslación y rotación para generar diferentes elementos dentro de la escena.

Además, se implementó iluminación para mejorar la percepción de profundidad y realismo. La cámara fue configurada mediante la función gluLookAt, permitiendo visualizar correctamente el entorno tridimensional.

Elementos de la escena

* Casa principal ubicada en el centro de la escena.
* Dos casas adicionales con diferentes tamaños y orientaciones.
* Cuatro árboles colocados alrededor de las construcciones.
* Terreno que representa el suelo de la escena.
* Sistema básico de iluminación.
* Cámara en perspectiva.

Herramientas utilizadas

* Python
* OpenGL
* GLFW

Código Fuente

import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

# ---------------- CÁMARA ----------------
camX, camY, camZ = 50, 1, -5
lookX, lookY, lookZ = 0, 1, 0


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


def draw_cube():
    glBegin(GL_QUADS)

    # lados
    glVertex3f(-1,0,1); glVertex3f(1,0,1); glVertex3f(1,1,1); glVertex3f(-1,1,1)
    glVertex3f(-1,0,-1); glVertex3f(1,0,-1); glVertex3f(1,1,-1); glVertex3f(-1,1,-1)
    glVertex3f(-1,0,-1); glVertex3f(-1,0,1); glVertex3f(-1,1,1); glVertex3f(-1,1,-1)
    glVertex3f(1,0,-1); glVertex3f(1,0,1); glVertex3f(1,1,1); glVertex3f(1,1,-1)

    # techo base
    glVertex3f(-1,1,-1); glVertex3f(1,1,-1); glVertex3f(1,1,1); glVertex3f(-1,1,1)

    # piso
    glVertex3f(-1,0,-1); glVertex3f(1,0,-1); glVertex3f(1,0,1); glVertex3f(-1,0,1)

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

def draw_house_model():
    # base
    glColor3f(0.8, 0.5, 0.2)
    draw_cube()

    # techo
    draw_roof()

    # puerta
    glColor3f(0.3,0.1,0)
    glBegin(GL_QUADS)
    glVertex3f(-0.3,0,1.01)
    glVertex3f(0.3,0,1.01)
    glVertex3f(0.3,0.6,1.01)
    glVertex3f(-0.3,0.6,1.01)
    glEnd()

def draw_tree():
    # tronco
    glColor3f(0.4, 0.2, 0.1)
    glPushMatrix()
    glScalef(0.2, 1, 0.2)
    draw_cube()
    glPopMatrix()

    # hojas con relieve (capas)
    glColor3f(0.1, 0.5, 0.1)

    for i in range(3):
        glPushMatrix()
        glTranslatef(0, 1 + i*0.5, 0)
        glScalef(1.2 - i*0.3, 0.6, 1.2 - i*0.3)
        draw_cube()
        glPopMatrix()

def draw_trees():
    positions = [
        (2,0,2),
        (-2,0,2),
        (3,0,-3),
        (-3,0,-2)
    ]

    for x,y,z in positions:
        glPushMatrix()
        glTranslatef(x,y,z)
        draw_tree()
        glPopMatrix()

def draw_scene():
    # casa principal
    glPushMatrix()
    draw_house_model()
    glPopMatrix()

    # SOLO 2 casas
    houses = [
        (4,0,0, 0.9, 30),
        (-4,0,0, 1.1, -30)
    ]

    for x,y,z,s,r in houses:
        glPushMatrix()
        glTranslatef(x,y,z)
        glScalef(s,s,s)
        glRotatef(r,0,1,0)
        draw_house_model()
        glPopMatrix()

    # árboles
    draw_trees()


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


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(camX, camY, camZ, lookX, lookY, lookZ, 0, 1, 0)

    draw_ground()
    draw_scene()

    glfw.swap_buffers(window)


def main():
    global window

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800,600,"Escena con 2 casas y árboles",None,None)
    glfw.make_context_current(window)

    glViewport(0,0,800,600)
    init()

    while not glfw.window_should_close(window):
        render()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

Resultados

Se obtuvo una escena tridimensional funcional en la que es posible observar varias construcciones y árboles sobre un terreno. La iluminación permite distinguir mejor las formas y la posición de los objetos dentro del espacio 3D.

Conclusiones

Esta práctica permitió reforzar conocimientos relacionados con gráficos por computadora, especialmente en el uso de OpenGL para la creación de objetos tridimensionales, manejo de cámaras, transformaciones geométricas e iluminación básica. También se comprendió cómo organizar una escena utilizando múltiples modelos y elementos distribuidos dentro de un entorno virtual.
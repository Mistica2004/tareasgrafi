Operación Órbita Dual (Graficación 3D / Práctica)

Introducción a la Misión

Agentes, interceptamos fragmentos de un motor de visualización en modo matriz fija (GL_MODELVIEW). El enemigo confunde deliberadamente quién se mueve: el objeto o la cámara. Tu misión es dominar el orden de transformaciones y demostrar que, matemáticamente, “mover la cámara” equivale a componer transformaciones inversas sobre el mundo — pero semánticamente cambia luces, referencias y el diseño del código.


Misión 1: El Espejo de la Matriz (Implementar ambos modos)

La Historia
El binario enemigo solo expone una bandera: MODO_ORBITA. Si está mal cableada, la escena “camina sola” o la cámara atraviesa el modelo.

Las Pistas
Modo A: primero posicionas la vista (glTranslatef(0,0,-d)), luego rotas el objeto.
Modo B: rotas la vista (signo y orden importan), luego alejas; el objeto queda en el origen del mundo.
Tu Tarea
Implementa render_rotating_object() y render_orbiting_camera() con un mismo angle incremental.
Asegúrate de que visualmente (desde la pantalla) la relación objeto–cámara sea coherente con la descripción de cada modo.
Captura dos PNG: m1_objeto_rota.png y m1_camara_orbita.png.
Nota pedagógica: arriba se muestra translate(-Z) y luego rotate para “orbitar cámara”; en el programa GLFW del final, el modo 2 usa la variante rotate(-angle) y luego translate (render_orbiting_camera). La función render_orbiting_camera_variant_b invierte ese orden para que compares. Documenta en tu reporte orden y signo.

Ejecutar: guarda el bloque Programa de referencia como orbita_dual_camara_objeto_glfw.py (o copia y pega en un archivo nuevo) y ejecuta python3 orbita_dual_camara_objeto_glfw.py. Teclas 1 / 2 / 3 cambian modo; ESC o Q cierra.

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

angle = 0.0
mode = 1

def draw_object():
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, 1.0, 32, 32)
    gluDeleteQuadric(quad)

def render_object_rotation():
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(angle, 0, 1, 0)
    draw_object()

def render_camera_orbit():
    glLoadIdentity()
    glRotatef(-angle, 0, 1, 0)
    glTranslatef(0, 0, -5)
    draw_object()

def render_camera_orbit_variant():
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(-angle, 0, 1, 0)
    draw_object()

def key_callback(window, key, scancode, action, mods):
    global mode
    if action == glfw.PRESS:
        if key == glfw.KEY_1:
            mode = 1
        elif key == glfw.KEY_2:
            mode = 2
        elif key == glfw.KEY_3:
            mode = 3
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

def setup():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.15, 1.0)

def main():
    global angle

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Orbita Dual", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    setup()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100)

        glMatrixMode(GL_MODELVIEW)

        if mode == 1:
            render_object_rotation()
        elif mode == 2:
            render_camera_orbit()
        elif mode == 3:
            render_camera_orbit_variant()

        angle += 0.5

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()


Misión 2: El Ojo Declarativo (gluLookAt)

La Historia
El cuartel general prefiere describir la cámara con ojo, objetivo y vector arriba en lugar de encadenar translate + rotate.

Tu Tarea
Implementa render_with_lookat(angle) colocando el ojo en una órbita circular alrededor del origen (radio 5, eje Y fijo).
El objetivo siempre es el origen; “arriba” es (0, 1, 0).
Guarda evidencia: m2_lookat_orbita.png (captura con tecla 3 pulsada).
Implementación: función render_with_lookat en orbita_dual_camara_objeto_glfw.py.

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation = 0.0
mode = 3


def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)


def set_material(specular, shininess):
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)


def draw_eye():
    glPushMatrix()

    glColor3f(0.85, 0.67, 0.65)
    set_material([0.2, 0.2, 0.2, 1.0], 16)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    set_material([0.9, 0.9, 0.9, 1.0], 80)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    glColor3f(0.2, 0.4, 0.9)
    set_material([0.3, 0.3, 0.4, 1.0], 32)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    glColor3f(0.0, 0.0, 0.0)
    set_material([0.0, 0.0, 0.0, 1.0], 4)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()


def setup_lighting():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


def render_object(angle):
    glLoadIdentity()
    glTranslatef(0, 0, -5)
    glRotatef(angle, 0, 1, 0)
    draw_eye()


def render_orbit_camera(angle):
    glLoadIdentity()

    radius = 5.0
    eye_x = math.sin(math.radians(angle)) * radius
    eye_z = math.cos(math.radians(angle)) * radius

    glTranslatef(0, 0, -5)
    glRotatef(-angle, 0, 1, 0)

    draw_eye()


def render_with_lookat(angle):
    glLoadIdentity()

    radius = 5.0
    eye_x = math.sin(math.radians(angle)) * radius
    eye_z = math.cos(math.radians(angle)) * radius

    gluLookAt(
        eye_x, 0.0, eye_z,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )

    draw_eye()


def main():
    global rotation, mode

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Orbita Dual", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    def key_callback(window, key, scancode, action, mods):
        global mode
        if action == glfw.PRESS:
            if key == glfw.KEY_1:
                mode = 1
            elif key == glfw.KEY_2:
                mode = 2
            elif key == glfw.KEY_3:
                mode = 3

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)

        rotation += 0.5

        if mode == 1:
            render_object(rotation)
        elif mode == 2:
            render_orbit_camera(rotation)
        elif mode == 3:
            render_with_lookat(rotation)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()


Misión 3: La Brújula de Luces (Efecto colateral)

La Historia
Si mueves el objeto pero dejas la luz en coordenadas de “cámara” antes de la rotación del objeto, las sombras “mienten”. Si mueves la cámara y la luz está fija al mundo, el contraste cambia de otra forma.

Tu Tarea
Coloca una luz direccional o puntual y documenta en 3–5 líneas qué ocurre en Modo Objeto vs Modo Cámara.
Opcional: captura m3_luz_objeto.png y m3_luz_camara.png.
Pista: en el .py cambia USE_LIGHTING = True y revisa setup_basic_lighting().

codigo:
from __future__ import annotations

import math
import sys
import glfw
from OpenGL.GL import *
from OpenGL.GLU import (
    gluLookAt,
    gluNewQuadric,
    gluPerspective,
    gluQuadricDrawStyle,
    gluSphere,
)

WINDOW_TITLE = "Orbita Dual - Luz"
ORBIT_RADIUS = 5.0
CAM_DISTANCE = 5.0
ANGLE_SPEED = 0.6
INITIAL_MODE = 1
USE_LIGHTING = True

_quadric = None
mode = INITIAL_MODE


def draw_sphere(radius=1.0):
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricDrawStyle(_quadric, GLU_FILL)
    gluSphere(_quadric, radius, 40, 24)


def setup_lighting():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])


def render_object(angle):
    glLoadIdentity()
    glTranslatef(0, 0, -CAM_DISTANCE)
    glRotatef(angle, 0, 1, 0)

    glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])

    glColor3f(0.4, 0.7, 1.0)
    draw_sphere()


def render_camera_manual(angle):
    glLoadIdentity()

    glRotatef(-angle, 0, 1, 0)
    glTranslatef(0, 0, -CAM_DISTANCE)

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 2.0, 1.0])

    glColor3f(1.0, 0.6, 0.3)
    draw_sphere()


def render_lookat(angle):
    glLoadIdentity()

    x = ORBIT_RADIUS * math.sin(math.radians(angle))
    z = ORBIT_RADIUS * math.cos(math.radians(angle))

    gluLookAt(
        x, 0, z,
        0, 0, 0,
        0, 1, 0
    )

    glLightfv(GL_LIGHT0, GL_POSITION, [x, 2.0, z, 1.0])

    glColor3f(1.0, 0.9, 0.4)
    draw_sphere()


def main():
    global mode

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, WINDOW_TITLE, None, None)
    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.15, 1.0)

    if USE_LIGHTING:
        setup_lighting()

    def key(window, k, s, a, m):
        global mode
        if a == glfw.PRESS:
            if k == glfw.KEY_1:
                mode = 1
            if k == glfw.KEY_2:
                mode = 2
            if k == glfw.KEY_3:
                mode = 3

    glfw.set_key_callback(window, key)

    angle = 0.0

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100)

        glMatrixMode(GL_MODELVIEW)

        if mode == 1:
            render_object(angle)
        elif mode == 2:
            render_camera_manual(angle)
        else:
            render_lookat(angle)

        angle += ANGLE_SPEED

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

resultado:
![orbitadual](<orbita dual.png>)


Entregable: Reporte de Misión (Markdown u Org)

Instrucciones
Entrega un archivo reporte_orbita_dual.md (o sección al final de este .org exportada) que incluya:

Capturas de Misiones 1–3 (y 3 si hiciste luces).
Bloque de código final limpio (un solo script o módulo).
Respuestas a las preguntas del analista (abajo).

codigo final:

import glfw
import sys
import math
from OpenGL.GL import *
from OpenGL import GLU

rotation = 0.0
quadric = None

def draw_sphere(r=1.0):
    global quadric
    if quadric is None:
        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
    GLU.gluSphere(quadric, r, 40, 24)

def setup_lighting():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def draw_eye():
    glPushMatrix()

    glColor3f(0.85, 0.67, 0.65)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    glColor3f(0.2, 0.4, 0.9)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()

def main():
    global rotation

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Operación Órbita Dual", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        GLU.gluPerspective(45, 800/600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(0, 0, -5)
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        rotation += 0.5

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()


Análisis del Analista (Reflexiones Finales)

1. Orden de matrices: ¿Por qué en OpenGL fijo el orden en que escribes glTranslatef / glRotatef cambia el resultado aunque uses los mismos números?

En OpenGL fijo las transformaciones no se aplican en el orden en que se escriben, sino en orden inverso debido a la multiplicación de matrices. Cada llamada (glTranslatef, glRotatef) multiplica la matriz actual, así que cambiar el orden cambia el sistema de referencia sobre el que actúa la siguiente transformación. Por eso rotar y luego trasladar no produce lo mismo que trasladar y luego rotar, aunque los valores sean iguales.


2. Objeto vs cámara: En la práctica, ¿cuándo prefieres rotar el modelo y cuándo orbitar la cámara?

Se rota el modelo cuando quieres animar el objeto en sí (por ejemplo, un planeta girando sobre su eje). Se orbita la cámara cuando quieres inspeccionar el objeto desde distintos ángulos sin modificarlo, como en visualizadores 3D o herramientas CAD. En resumen: modelo = animación del objeto, cámara = exploración de la escena.


3. gluLookAt vs translate+rotate: ¿Qué ventaja tiene describir la cámara con ojo–objetivo–arriba para equipos de desarrollo?

gluLookAt simplifica la definición de la cámara porque describe directamente la intención visual (desde dónde miro, hacia dónde y cuál es la orientación vertical). Esto reduce errores de composición de matrices, mejora la legibilidad del código y facilita que varios desarrolladores entiendan y modifiquen la cámara sin tener que razonar sobre transformaciones inversas.


4. Luces: Si la luz se define en el frame de la cámara sin reubicarla al mundo, ¿qué artefacto visual esperas al rotar solo el objeto?

Se produce un efecto de iluminación “pegada a la cámara”, donde la luz parece seguir siempre al observador. Esto elimina sombras coherentes en el espacio y hace que el objeto no muestre cambios realistas al rotar, ya que la dirección de iluminación no es fija en el mundo sino relativa a la vista, generando una apariencia plana o artificial.
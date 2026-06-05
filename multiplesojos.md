Ojos Paramétricos en OpenGL

Introducción

En esta práctica se desarrolló una aplicación gráfica utilizando OpenGL y GLFW para generar diferentes representaciones de ojos en un entorno tridimensional. El programa permite visualizar distintas configuraciones geométricas mediante parámetros que modifican tanto la distribución de los ojos como su forma. Además, se incorporó iluminación básica para mejorar la apariencia visual de los objetos y una animación continua que aporta dinamismo a la escena.

Codigo
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

rotation = 0.0
eye_mode = 0
eye_shape = 0
time_var = 0.0

# =====================================================
# ESFERA
# =====================================================

def draw_sphere(radius, slices, stacks):

    quadric = gluNewQuadric()

    gluQuadricNormals(quadric, GLU_SMOOTH)

    gluSphere(quadric, radius, slices, stacks)

    gluDeleteQuadric(quadric)

# =====================================================
# FORMAS 2D
# =====================================================

def draw_square():

    glBegin(GL_QUADS)

    glVertex3f(-0.8, -0.8, 0)
    glVertex3f( 0.8, -0.8, 0)
    glVertex3f( 0.8,  0.8, 0)
    glVertex3f(-0.8,  0.8, 0)

    glEnd()

# -----------------------------------------------------

def draw_rhombus():

    glBegin(GL_QUADS)

    glVertex3f( 0.0,  1.0, 0)
    glVertex3f( 1.0,  0.0, 0)
    glVertex3f( 0.0, -1.0, 0)
    glVertex3f(-1.0,  0.0, 0)

    glEnd()

# -----------------------------------------------------

def draw_triangle():

    glBegin(GL_TRIANGLES)

    glVertex3f( 0.0,  1.0, 0)
    glVertex3f(-1.0, -1.0, 0)
    glVertex3f( 1.0, -1.0, 0)

    glEnd()

# =====================================================
# DIBUJAR FORMA DEL OJO
# =====================================================

def draw_eye_shape(scale=1.0):

    global eye_shape

    glPushMatrix()

    glScalef(scale, scale, scale)

    # OJO CIRCULAR
    if eye_shape == 0:

        glEnable(GL_LIGHTING)

        draw_sphere(0.8, 30, 30)

    # OJO CUADRADO
    elif eye_shape == 1:

        glDisable(GL_LIGHTING)

        draw_square()

        glEnable(GL_LIGHTING)

    # OJO ROMBO
    elif eye_shape == 2:

        glDisable(GL_LIGHTING)

        draw_rhombus()

        glEnable(GL_LIGHTING)

    # OJO TRIANGULO
    elif eye_shape == 3:

        glDisable(GL_LIGHTING)

        draw_triangle()

        glEnable(GL_LIGHTING)

    glPopMatrix()

# =====================================================
# OJO COMPLETO
# =====================================================

def draw_eye():

    glPushMatrix()

    # -------------------------------------------------
    # BASE BLANCA
    # -------------------------------------------------

    glColor3f(1, 1, 1)

    draw_eye_shape(1.0)

    # -------------------------------------------------
    # IRIS AZUL
    # -------------------------------------------------

    glPushMatrix()

    glTranslatef(0, 0, 0.1)

    glColor3f(0, 0, 1)

    draw_eye_shape(0.5)

    glPopMatrix()

    # -------------------------------------------------
    # PUPILA NEGRA
    # -------------------------------------------------

    glPushMatrix()

    glTranslatef(0, 0, 0.2)

    glColor3f(0, 0, 0)

    draw_eye_shape(0.2)

    glPopMatrix()

    glPopMatrix()

# =====================================================
# MODOS
# =====================================================

def draw_one_eye():

    draw_eye()

# -----------------------------------------------------

def draw_grid_eyes():

    for row in range(3):

        for col in range(3):

            x = (col - 1) * 3
            y = (row - 1) * 3

            glPushMatrix()

            glTranslatef(x, y, 0)

            glScalef(0.4, 0.4, 0.4)

            draw_eye()

            glPopMatrix()

# -----------------------------------------------------
# PARAMETRICA CIRCULAR
# -----------------------------------------------------

def draw_circle_eyes():

    num = 8
    radius = 5

    for i in range(num):

        angle = (2 * math.pi / num) * i

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glPushMatrix()

        glTranslatef(x, y, 0)

        glScalef(0.3, 0.3, 0.3)

        draw_eye()

        glPopMatrix()

# -----------------------------------------------------
# PARAMETRICA ONDA
# -----------------------------------------------------

def draw_wave_eyes():

    global time_var

    for i in range(12):

        x = (i - 6) * 1.5

        y = math.sin(i + time_var) * 2

        glPushMatrix()

        glTranslatef(x, y, 0)

        glScalef(0.25, 0.25, 0.25)

        draw_eye()

        glPopMatrix()

# =====================================================
# DIBUJAR SEGUN eye_mode
# =====================================================

def draw_eyes():

    if eye_mode == 0:

        draw_one_eye()

    elif eye_mode == 1:

        draw_grid_eyes()

    elif eye_mode == 2:

        draw_circle_eyes()

    elif eye_mode == 3:

        draw_wave_eyes()

# =====================================================
# ILUMINACION
# =====================================================

def setup_lighting():

    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)

    glEnable(GL_DEPTH_TEST)

    glEnable(GL_COLOR_MATERIAL)

    light_position = [2, 3, 2, 1]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

# =====================================================
# TECLADO
# =====================================================

def key_callback(window, key, scancode, action, mods):

    global eye_mode
    global eye_shape

    if action == glfw.PRESS:

        # MODOS

        if key == glfw.KEY_1:

            eye_mode = 0
            print("UN OJO")

        elif key == glfw.KEY_2:

            eye_mode = 1
            print("CUADRICULA")

        elif key == glfw.KEY_3:

            eye_mode = 2
            print("CIRCULO")

        elif key == glfw.KEY_4:

            eye_mode = 3
            print("ONDA")

        # FORMAS

        elif key == glfw.KEY_Q:

            eye_shape = 0
            print("OJO CIRCULAR")

        elif key == glfw.KEY_W:

            eye_shape = 1
            print("OJO CUADRADO")

        elif key == glfw.KEY_E:

            eye_shape = 2
            print("OJO ROMBO")

        elif key == glfw.KEY_R:

            eye_shape = 3
            print("OJO TRIANGULO")

# =====================================================
# MAIN
# =====================================================

def main():

    global rotation
    global time_var

    if not glfw.init():

        return

    window = glfw.create_window(
        900,
        700,
        "Ojos Parametricos",
        None,
        None
    )

    if not window:

        glfw.terminate()

        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    glClearColor(0.54, 0.72, 0.84, 1)

    setup_lighting()

    print("=" * 50)
    print("MODOS")
    print("1 = Un ojo")
    print("2 = Cuadricula")
    print("3 = Circulo")
    print("4 = Onda")
    print()
    print("FORMAS")
    print("Q = Circular")
    print("W = Cuadrado")
    print("E = Rombo")
    print("R = Triangulo")
    print("=" * 50)

    while not glfw.window_should_close(window):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # PROYECCION

        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()

        gluPerspective(45, 900 / 700, 0.1, 100)

        # MODELO

        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()

        glTranslatef(0, 0, -20)

        rotation += 0.3

        time_var += 0.03

        glRotatef(rotation, 0, 1, 0)

        glRotatef(15, 1, 0, 0)

        draw_eyes()

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()

# =====================================================

if __name__ == "__main__":

    main()
    
Descripción del código

El programa crea una ventana gráfica donde se renderizan ojos compuestos por tres elementos principales: la esclerótica (parte blanca), el iris y la pupila. Cada uno de estos componentes puede representarse mediante diferentes figuras geométricas, como círculos, cuadrados, rombos o triángulos.

El usuario puede interactuar con la aplicación mediante el teclado para cambiar entre distintos modos de visualización:

* Un único ojo en el centro de la escena.
* Una cuadrícula de ojos distribuidos uniformemente.
* Una disposición circular de ojos utilizando ecuaciones paramétricas.
* Una distribución en forma de onda senoidal animada.

Asimismo, es posible modificar la forma de los ojos utilizando distintas figuras geométricas. El programa emplea transformaciones como traslación, escalado y rotación para posicionar correctamente cada elemento dentro de la escena. También se utiliza iluminación de OpenGL para proporcionar una apariencia más realista a los objetos tridimensionales.

La escena permanece en rotación constante y, en el modo de onda, los ojos cambian de posición dinámicamente utilizando funciones matemáticas basadas en el seno.

Conclusión

Esta práctica permitió aplicar conceptos fundamentales de gráficos por computadora, incluyendo modelado geométrico, transformaciones espaciales, iluminación y animación en OpenGL. Además, se exploró el uso de ecuaciones paramétricas para generar distribuciones dinámicas de objetos dentro de una escena tridimensional. El resultado es una aplicación interactiva que demuestra cómo combinar programación matemática y gráficos 3D para crear visualizaciones complejas y atractivas.
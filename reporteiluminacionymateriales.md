Misión: Iluminación y Materiales en un Ojo 3D (GLFW + PyOpenGL)

Vas a convertir un objeto dibujado con glColor3f() (colores planos) en un objeto con iluminación realista usando OpenGL fijo (lighting clásico) y materiales.


Misiones (checkpoints)

Misión 1: “Enciende la luz”

Objetivo: que OpenGL calcule iluminación (no solo colores planos).

Tareas
Activa estados:
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
Define el color de la luz:
glLightfv(GL_LIGHT0, GL_AMBIENT, [...])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [...])
glLightfv(GL_LIGHT0, GL_SPECULAR, [...])
Criterio de éxito
Al rotar, se ven zonas iluminadas y zonas en sombra (cambio de intensidad por ángulo).
Pista
Pon light_position[3] = 1.0 para luz posicional (más intuitiva que 0.2).

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
rotation = 0.0
def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)  # IMPORTANTE para iluminación
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)
def draw_eye():
    glPushMatrix()
    glMaterialfv(GL_FRONT, GL_AMBIENT,  [0.3, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,  [0.85, 0.67, 0.65, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 20)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_AMBIENT,  [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 80)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_AMBIENT,  [0.2, 0.2, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,  [0.84, 0.85, 0.92, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 40)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_AMBIENT,  [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE,  [0.05, 0.05, 0.05, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 2)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()
    glPopMatrix()
def setup_lighting():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Luz ambiental (base)
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.25, 0.25, 0.25, 1.0])

    # Luz difusa (sombra y volumen)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.9, 0.9, 0.9, 1.0])

    # Luz especular (brillo)
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # IMPORTANTE: habilitar materiales reales
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE)
def main():
    global rotation
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Ojo 3D con Iluminación", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Luz posicional (CLAVE para sombras reales)
        light_position = [2.0, 2.0, 2.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)
        draw_eye()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
if __name__ == "__main__":
    main()

resultado:
![1](<mision iluminacion 1.png>)


Misión 2: “La esfera necesita normales”

Objetivo: que la luz “entienda” la forma.

Tareas
En draw_sphere(), antes de gluSphere(...):
gluQuadricNormals(quad, GLU_SMOOTH)
Criterio de éxito
La iluminación se ve suave (sin artefactos raros) y “redondeada”.

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
rotation = 0.0
def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
    # CLAVE DE LA MISIÓN: normales suaves
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)
def draw_eye():
    glPushMatrix()
    # PIEL
    glColor3f(0.85, 0.67, 0.65)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()
    # ESCLERÓTICA
    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()
    # IRIS
    glColor3f(0.84, 0.85, 0.92)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()
    # PUPILA
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()
    glPopMatrix()
def setup_lighting():
    glEnable(GL_DEPTH_TEST)
    # ENCENDER ILUMINACIÓN REAL
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # Luz (posicional = 1.0)
    light_position = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    # Componentes de luz
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    # Materiales automáticos (IMPORTANTE)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
def main():
    global rotation

    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Ojo 3D con Normales", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)
        draw_eye()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
if __name__ == "__main__":
    main()

respuestas:
![2](<mision iluminacion 2.png>)


Misión 3: “Materiales: esclerótica, iris y pupila”

Objetivo: controlar brillo y apariencia con materiales.

Tareas
Crea una función:
set_material(ambient, diffuse, specular, shininess, face=GL_FRONT)
usando glMaterialfv y glMaterialf.
Aplica materiales distintos antes de cada esfera:
Blanco (esclerótica): especular moderado, shininess medio/alto.
Iris (azul): especular bajo/medio, shininess medio.
Pupila (negro): casi sin especular, shininess bajo.
Piel/rojizo: difuso cálido, especular suave.
Criterio de éxito
El blanco “brilla” más que el iris y la pupila casi no refleja.

Pista
Shininess va de 0 a 128. Prueba 8 (mate), 32 (plástico), 80 (pulido), 128 (muy brillante).

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
rotation = 0.0
def set_material(ambient, diffuse, specular, shininess, face=GL_FRONT):
    glMaterialfv(face, GL_AMBIENT, ambient)
    glMaterialfv(face, GL_DIFFUSE, diffuse)
    glMaterialfv(face, GL_SPECULAR, specular)
    glMaterialf(face, GL_SHININESS, shininess)
def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)
def draw_eye():
    glPushMatrix()
    set_material(
        [0.3, 0.2, 0.2, 1.0],   # ambient
        [0.8, 0.6, 0.55, 1.0],  # diffuse
        [0.2, 0.2, 0.2, 1.0],   # specular
        16                      # shininess (suave)
    )
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()
    set_material(
        [0.6, 0.6, 0.6, 1.0],   # ambient
        [1.0, 1.0, 1.0, 1.0],   # diffuse
        [0.9, 0.9, 0.9, 1.0],   # specular (alto brillo)
        80                      # shininess alto
    )
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()
    set_material(
        [0.2, 0.2, 0.3, 1.0],
        [0.2, 0.4, 0.9, 1.0],
        [0.3, 0.3, 0.4, 1.0],   # especular bajo-medio
        32                      # brillo tipo plástico
    )
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()
    set_material(
        [0.0, 0.0, 0.0, 1.0],
        [0.05, 0.05, 0.05, 1.0],
        [0.0, 0.0, 0.0, 1.0],   # sin reflejo
        4                       # casi mate total
    )
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
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_COLOR_MATERIAL)
def main():
    global rotation
    if not glfw.init():
        return
    window = glfw.create_window(800, 600, "Materiales en Ojo 3D", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)
        draw_eye()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
if __name__ == "__main__":
    main()


Misión 4 (opcional): “Que glColor afecte el material”

Objetivo: combinar glColor3f() con iluminación.

Tareas
Activa:
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
Mantén GL_SPECULAR y GL_SHININESS como material fijo.
Criterio de éxito
Cambiar glColor3f cambia el color con luz (no “plano”), y se conservan brillos.

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
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

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Ojo 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

resultado:
![4](<mision iluminacion 2.png>)


Misión 5: “¿Por qué la luz cambia cuando rota?”

Objetivo: controlar si la luz se mueve con el objeto o se queda fija.

Tareas
Mueve la línea de posición de luz:
Opción A: en el loop, justo después de glLoadIdentity() y gluLookAt(...) (luz fija en “mundo/cámara”).
Opción B: después de rotar el objeto (luz “pegada” al objeto).
Criterio de éxito
Puedes explicar (en 2–3 líneas) por qué la luz cambia: la posición se transforma con la matriz MODELVIEW vigente.

codigo:

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0
light_mode = 0

def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
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

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def key_callback(window, key, scancode, action, mods):
    global light_mode
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            light_mode = 1 - light_mode

def set_light():
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 1.0])

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Luz y Rotación", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        if light_mode == 0:
            set_light()

        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)

        if light_mode == 1:
            set_light()

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

resultados:
![5](<mision iluminacion 5.png>)


Entregable
Tu script final (.py) con:
iluminación activa
normales en GLU quadric
materiales (o color-material) aplicados a cada esfera

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

def draw_sphere(radius, slices=30, stacks=30):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def set_material(ambient, diffuse, specular, shininess):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

def draw_eye():
    glPushMatrix()

    set_material(
        [0.3, 0.2, 0.2, 1.0],
        [0.85, 0.67, 0.65, 1.0],
        [0.2, 0.2, 0.2, 1.0],
        16
    )
    glColor3f(0.85, 0.67, 0.65)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    set_material(
        [0.8, 0.8, 0.8, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [0.9, 0.9, 0.9, 1.0],
        80
    )
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    set_material(
        [0.2, 0.2, 0.3, 1.0],
        [0.2, 0.4, 0.9, 1.0],
        [0.3, 0.3, 0.4, 1.0],
        32
    )
    glColor3f(0.2, 0.4, 0.9)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    set_material(
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        4
    )
    glColor3f(0.0, 0.0, 0.0)
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
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.9, 0.9, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Ojo Iluminado 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glClearColor(0.54, 0.72, 0.84, 1.0)
    setup_lighting()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)

        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

rotation = 0.0

# ---------------------------
# Misión 3: función de material
# ---------------------------
def set_material(ambient, diffuse, specular, shininess, face=GL_FRONT):
    glMaterialfv(face, GL_AMBIENT, ambient)
    glMaterialfv(face, GL_DIFFUSE, diffuse)
    glMaterialfv(face, GL_SPECULAR, specular)
    glMaterialf(face, GL_SHININESS, shininess)

def draw_sphere(radius, slices=30, stacks=30):
    """Función auxiliar para dibujar esferas usando GLU"""
    quad = gluNewQuadric()

    # ---------------------------
    # Misión 2: normales suaves
    # ---------------------------
    gluQuadricNormals(quad, GLU_SMOOTH)

    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_eye():
    glPushMatrix()

    # ---------------------------
    # PIEL
    # ---------------------------
    set_material(
        [0.2, 0.15, 0.15, 1.0],   # ambient
        [0.85, 0.67, 0.65, 1.0],  # diffuse
        [0.2, 0.2, 0.2, 1.0],     # specular
        16                        # shininess (suave)
    )
    glColor3f(0.85, 0.67, 0.65)
    glPushMatrix()
    glTranslatef(0.7, 0, 0)
    draw_sphere(0.54)
    glPopMatrix()

    # ---------------------------
    # ESCLERÓTICA (BLANCO)
    # ---------------------------
    set_material(
        [0.8, 0.8, 0.8, 1.0],
        [1.0, 1.0, 1.0, 1.0],
        [0.9, 0.9, 0.9, 1.0],  # alto especular
        80                     # brillante
    )
    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(0.56, 0, 0)
    draw_sphere(0.6)
    glPopMatrix()

    # ---------------------------
    # IRIS
    # ---------------------------
    set_material(
        [0.2, 0.2, 0.3, 1.0],
        [0.84, 0.85, 0.92, 1.0],
        [0.3, 0.3, 0.4, 1.0],
        32
    )
    glColor3f(0.84, 0.85, 0.92)
    glPushMatrix()
    glTranslatef(0.49, 0, 0)
    draw_sphere(0.55)
    glPopMatrix()

    # ---------------------------
    # PUPILA
    # ---------------------------
    set_material(
        [0.0, 0.0, 0.0, 1.0],
        [0.05, 0.05, 0.05, 1.0],
        [0.0, 0.0, 0.0, 1.0],  # sin brillo
        4
    )
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0.3, 0, 0)
    draw_sphere(0.4)
    glPopMatrix()

    glPopMatrix()

def setup_lighting():
    """Misión 1: configuración completa de luz"""

    # Activar estados
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Luz
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # ---------------------------
    # Misión 4 (opcional)
    # ---------------------------
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():
    global rotation

    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Ojo con Iluminación", None, None)
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

        # ---------------------------
        # Misión 5: luz fija en cámara
        # ---------------------------
        light_position = [1.0, 1.0, 1.0, 1.0]  # posicional
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        gluLookAt(0,0,5, 0,0,0, 0,1,0)

        rotation += 0.5
        glRotatef(rotation, 0, 1, 0)

        draw_eye()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
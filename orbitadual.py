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





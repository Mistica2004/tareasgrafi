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



Ojos Con Iluminacion

Introducción

La iluminación es uno de los elementos más importantes en los gráficos por computadora, ya que permite representar los objetos tridimensionales de manera más realista. Mediante el uso de fuentes de luz, materiales y normales, es posible simular cómo la luz interactúa con las superficies de los objetos, generando efectos de brillo, sombras y profundidad visual.

En esta práctica se desarrolló un modelo tridimensional de un ojo utilizando OpenGL y GLFW. Se aplicaron diferentes configuraciones de iluminación y materiales para representar adecuadamente cada una de las partes del ojo, como la piel, la esclerótica, el iris y la pupila. Además, se implementaron normales suaves para mejorar la apariencia de las superficies curvas y se utilizó una luz posicional para observar los efectos de reflexión sobre los materiales.


Codigo
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
    
Funcionamiento del Código

El programa inicia creando una ventana mediante GLFW y configurando un contexto de OpenGL. Posteriormente se habilitan las características necesarias para el renderizado tridimensional, incluyendo la prueba de profundidad, la iluminación y la fuente de luz principal.

Se implementó una función llamada set_material() que permite asignar propiedades de material a cada objeto. Estas propiedades incluyen componentes ambientales, difusas y especulares, además del nivel de brillo o shininess. Gracias a esto, cada parte del ojo presenta una apariencia visual diferente.

Para la construcción de las figuras se utilizaron cuadráticas de GLU, específicamente esferas. Se configuraron normales suaves mediante gluQuadricNormals(GLU_SMOOTH), lo que permite que la iluminación se distribuya de forma gradual sobre la superficie y genere un aspecto más natural.

Durante cada ciclo de renderizado se establece una cámara en perspectiva utilizando gluPerspective() y gluLookAt(). También se define la posición de una fuente de luz que ilumina la escena. Finalmente, se aplica una rotación continua al modelo para observar cómo cambian los reflejos y las sombras desde diferentes ángulos.

El modelo del ojo está compuesto por varias esferas superpuestas, cada una con materiales específicos que representan la piel, la esclerótica, el iris y la pupila. Esta combinación de geometría, materiales e iluminación permite obtener un resultado visual más realista.

Conclusión

Mediante esta práctica se comprendió la importancia de la iluminación y los materiales dentro de los gráficos tridimensionales. La utilización de componentes ambientales, difusas y especulares permitió simular distintos tipos de superficies y mejorar significativamente la apariencia visual del modelo.

Asimismo, el uso de normales suaves contribuyó a representar correctamente las superficies curvas, mientras que la iluminación posicional permitió apreciar los efectos de reflexión desde diferentes perspectivas. En conjunto, estas técnicas constituyen una base fundamental para el desarrollo de aplicaciones de gráficos por computadora y entornos tridimensionales más realistas.


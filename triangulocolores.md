Triangulo Colores

Introducción

En esta práctica se desarrolló una aplicación gráfica utilizando Python, GLFW y OpenGL para representar un cubo tridimensional con rotación continua. El objetivo principal fue comprender los conceptos básicos de gráficos 3D, incluyendo la creación de ventanas, la configuración del contexto de OpenGL, las transformaciones geométricas y el uso del buffer de profundidad para la correcta visualización de objetos tridimensionales.

La implementación permite visualizar un cubo compuesto por seis caras de distintos colores, el cual gira constantemente sobre los ejes X, Y y Z, generando una percepción espacial y facilitando el estudio de las transformaciones en gráficos por computadora.

Codigo
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

# Variables globales
window = None
angle = 0  # Declaramos angle en el nivel superior

def init():
    # Configuración inicial de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo
    glEnable(GL_DEPTH_TEST)  # Activar prueba de profundidad para 3D
    # Configuración de proyección
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.1, 50.0)
    # Cambiar a la matriz de modelo para los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

    # Configuración de la vista del cubo
    glLoadIdentity()
    glTranslatef(0, 0, 0)  # Alejar el cubo para que sea visible
    glRotatef(angle, 1, 1, 1)   # Rotar el cubo en todos los ejes
    

    #glRotatef(angle, 0, 1, 0)   # Rotar el cubo en todos los ejes

    glBegin(GL_QUADS)  # Iniciar el cubo como un conjunto de caras (quads)

    # Cada conjunto de cuatro vértices representa una cara del cubo
    glColor3f(1.0, 0.0, 1.0)  # Rojo
    glVertex3f( 1, 1,-1)
    glColor3f(0.4, 1.0, 1.0)  # Verde
    glVertex3f(-1, 1,-1)
    glColor3f(0.4, 1.0, 1.0)  # Verde
    glVertex3f(-1, 1, 1)
    glColor3f(0.3, 0.8, 0.1)  # Verde
    glVertex3f( 1, 1, 1)

    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex3f( 1,-1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f(-1,-1,-1)
    glVertex3f( 1,-1,-1)

    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f( 1, 1, 1)
    glVertex3f(-1, 1, 1)
    glVertex3f(-1,-1, 1)
    glVertex3f( 1,-1, 1)

    glColor3f(1.0, 1.0, 0.0)  # Amarillo
    glVertex3f( 1,-1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1, 1,-1)
    glVertex3f( 1, 1,-1)

    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f(-1, 1, 1)
    glVertex3f(-1, 1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1, 1)

    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f( 1, 1,-1)
    glVertex3f( 1, 1, 1)
    glVertex3f( 1,-1, 1)
    glVertex3f( 1,-1,-1)

    glEnd()
    glFlush()

    glfw.swap_buffers(window)  # Intercambiar buffers para animación suave
    angle += 0.1  # Incrementar el ángulo para rotación

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 500, 500
    window = glfw.create_window(width, height, "Cubo 3D Rotando con GLFW", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Configurar el contexto de OpenGL en la ventana
    glfw.make_context_current(window)

    # Configuración de viewport y OpenGL
    glViewport(0, 1, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_cube()
        glfw.poll_events()

    glfw.terminate()  # Cerrar GLFW al salir

if __name__ == "__main__":
    main()
    
Funcionamiento del código

El programa comienza importando las bibliotecas GLFW y OpenGL necesarias para crear la ventana y realizar el renderizado gráfico.

Se define una variable global llamada angle, la cual controla el ángulo de rotación del cubo. Esta variable se incrementa constantemente para producir el efecto de movimiento.

La función init() se encarga de configurar el entorno de OpenGL. En esta sección se establece el color de fondo de la ventana, se activa la prueba de profundidad (GL_DEPTH_TEST) y se configura una proyección en perspectiva mediante la función gluPerspective(). Esto permite que los objetos se visualicen con profundidad, simulando una cámara tridimensional.

La función draw_cube() es responsable del dibujo del cubo. Primero limpia la pantalla y el buffer de profundidad para preparar un nuevo fotograma. Después aplica una rotación utilizando la función glRotatef(), tomando como referencia el valor almacenado en la variable angle.

El cubo se construye utilizando primitivas del tipo GL_QUADS, donde cada grupo de cuatro vértices define una de sus seis caras. Además, se asignan distintos colores a los vértices mediante glColor3f(), lo que genera una apariencia más visual y facilita la identificación de cada cara durante la rotación.

Al finalizar el dibujo, los buffers se intercambian utilizando glfw.swap_buffers(), permitiendo mostrar la nueva imagen en pantalla sin parpadeos. Posteriormente, el valor de angle aumenta ligeramente para que el cubo continúe girando en el siguiente ciclo de renderizado.

La función main() coordina la ejecución general del programa. Inicializa GLFW, crea la ventana, establece el contexto de OpenGL y ejecuta el bucle principal, donde se actualiza continuamente la escena hasta que el usuario cierre la ventana.

Conclusión

Mediante esta práctica fue posible comprender los fundamentos del modelado y renderizado de objetos tridimensionales utilizando OpenGL. Se aprendió a configurar una proyección en perspectiva, manipular transformaciones geométricas y construir figuras mediante vértices y primitivas gráficas.

La animación de rotación permitió observar cómo las transformaciones afectan a los objetos dentro de una escena 3D, mientras que el uso del buffer de profundidad garantizó una representación correcta de las caras visibles del cubo. Este ejercicio constituye una base importante para el desarrollo de aplicaciones más complejas relacionadas con gráficos por computadora, simulaciones y realidad aumentada.
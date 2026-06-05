Triángulo Básico con OpenGL y GLFW

Descripción del proyecto

Este programa tiene como objetivo mostrar el funcionamiento básico de OpenGL mediante el dibujo de un triángulo en una ventana gráfica. Para ello se utiliza la biblioteca GLFW, encargada de crear y administrar la ventana, mientras que OpenGL se utiliza para realizar el renderizado de los gráficos.

Al ejecutarse, el programa crea una ventana de 800 × 600 píxeles y configura una proyección ortográfica en dos dimensiones. Posteriormente, se dibuja un triángulo cuyos vértices poseen colores diferentes: rojo, verde y azul. Gracias a la interpolación de colores realizada por OpenGL, el interior del triángulo presenta un degradado suave entre estos tres colores.

El programa se mantiene en ejecución mediante un bucle principal que actualiza constantemente la ventana, procesa los eventos del usuario y vuelve a dibujar la escena. Finalmente, cuando el usuario cierra la ventana, GLFW libera los recursos utilizados y la aplicación termina de forma correcta.

Este ejemplo representa una introducción al uso de OpenGL y GLFW, permitiendo comprender conceptos fundamentales como la creación de ventanas, la configuración de proyecciones, el manejo del ciclo de renderizado y el dibujo de primitivas gráficas básicas.

Codigo

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_triangle():
    # Dibuja un triángulo con OpenGL
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)  # Rojo
    glVertex2f(-0.5, -0.5)    # Vértice inferior izquierdo
    glColor3f(0.0, 1.0, 0.0)  # Verde
    glVertex2f(0.5, -0.5)     # Vértice inferior derecho
    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex2f(0.0, 0.5)      # Vértice superior
    glEnd()

def main():
    # Inicializa GLFW
    if not glfw.init():
        return

    # Crear la ventana
    window = glfw.create_window(800, 600, "OpenGL Triángulo", None, None)
    if not window:
        glfw.terminate()
        return

    # Hacer el contexto de OpenGL actual para la ventana
    glfw.make_context_current(window)

    # Configurar la proyección (2D simple)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)  # Proyección ortográfica 2D
    glMatrixMode(GL_MODELVIEW)

    # Bucle principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpiar la pantalla con color de fondo

        draw_triangle()  # Dibujar el triángulo

        glfw.swap_buffers(window)  # Intercambiar los buffers
        glfw.poll_events()  # Comprobar eventos

    # Finalizar GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
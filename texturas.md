Texturas

Introducción

En esta práctica se desarrolló una escena tridimensional utilizando Python, OpenGL y GLFW, cuyo objetivo principal fue aplicar el uso de texturas sobre diferentes objetos dentro de un entorno 3D. La escena representa una casa sencilla ubicada sobre un terreno, donde cada elemento utiliza una textura distinta para aumentar el realismo visual.

El proyecto permite comprender cómo cargar imágenes externas y aplicarlas sobre superficies geométricas mediante coordenadas de textura. Además, se emplean conceptos fundamentales de gráficos por computadora como proyecciones en perspectiva, transformaciones de cámara y renderizado de objetos tridimensionales.

Codigo
import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

tex_pasto = None
tex_pared = None
tex_techo = None


def load_texture(path):

    img = Image.open(path).convert("RGB")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.tobytes()

    tex_id = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Filtrado
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Envoltura (tiling)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Subir la textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.width, img.height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Crear mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id


def init():
    global tex_pasto, tex_pared, tex_techo

    glClearColor(0.5, 0.8, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Cargar texturas
    tex_pasto = load_texture("pasto.jpg")
    tex_pared = load_texture("pared.png")
    tex_techo = load_texture("trunk.png")


def draw_ground():
    glBindTexture(GL_TEXTURE_2D, tex_pasto)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    scale = 5

    glTexCoord2f(0, 0);       glVertex3f(-10, 0, 10)
    glTexCoord2f(scale, 0);   glVertex3f( 10, 0, 10)
    glTexCoord2f(scale, scale);glVertex3f( 10, 0,-10)
    glTexCoord2f(0, scale);   glVertex3f(-10, 0,-10)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Casa con textura de pared
# ------------------------------------------------------------
def draw_cube():
    glBindTexture(GL_TEXTURE_2D, tex_pared)

    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)

    # Frente
    glTexCoord2f(0, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1, 1)

    # Atrás
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1,-1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Izquierda
    glTexCoord2f(0, 0); glVertex3f(-1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f(-1, 1,-1)

    # Derecha
    glTexCoord2f(0, 0); glVertex3f( 1, 0,-1)
    glTexCoord2f(1, 0); glVertex3f( 1, 0, 1)
    glTexCoord2f(1, 1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1); glVertex3f( 1, 1,-1)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Techo con textura propia
# ------------------------------------------------------------
def draw_roof():
    glBindTexture(GL_TEXTURE_2D, tex_techo)

    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 1)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1, 1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glTexCoord2f(0, 0);    glVertex3f(-1, 1,-1)
    glTexCoord2f(1, 0);    glVertex3f( 1, 1,-1)
    glTexCoord2f(0.5, 1);  glVertex3f( 0, 2, 0)

    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)


# ------------------------------------------------------------
# Escena principal
# ------------------------------------------------------------
def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(4, 4, 8, 0, 1, 0, 0, 1, 0)

    draw_ground()
    draw_cube()
    draw_roof()

    glfw.swap_buffers(window)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    global window

    if not glfw.init():
        sys.exit()

    window = glfw.create_window(800, 600, "Casa con Varias Texturas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, 800, 600)

    init()

    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
    
Funcionamiento del código

El programa inicia importando las bibliotecas necesarias para trabajar con OpenGL, GLFW y el procesamiento de imágenes mediante la biblioteca PIL.

Se definen tres variables globales destinadas a almacenar las texturas utilizadas en la escena: una para el pasto del terreno, otra para las paredes de la casa y una tercera para el techo.

La función load_texture() es responsable de cargar una imagen desde el disco, convertirla al formato RGB y enviarla a la memoria de la tarjeta gráfica. Durante este proceso se configuran los parámetros de filtrado y repetición de textura, además de generar automáticamente los mipmaps para mejorar la calidad visual cuando los objetos se observan a diferentes distancias.

La función init() configura el entorno gráfico. Se establece un color de fondo que simula un cielo azul, se activa la prueba de profundidad para el renderizado tridimensional y se habilita el uso de texturas. También se define una proyección en perspectiva mediante gluPerspective() y se cargan las tres imágenes utilizadas como texturas.

La función draw_ground() dibuja el terreno de la escena mediante un cuadrilátero grande. Sobre esta superficie se aplica la textura de pasto utilizando coordenadas de textura que permiten repetir la imagen varias veces para cubrir una superficie extensa sin perder calidad visual.

La función draw_cube() construye las paredes de la casa utilizando cuatro caras rectangulares. Cada una de estas superficies recibe la textura de pared mediante coordenadas UV, logrando una apariencia similar a una construcción real.

La función draw_roof() genera el techo utilizando dos triángulos. A estas superficies se les asigna una textura diferente para distinguir visualmente el techo de las paredes de la vivienda.

La función draw_scene() administra el renderizado de toda la escena. Primero limpia la pantalla y el buffer de profundidad, posteriormente posiciona la cámara mediante la función gluLookAt(), lo que permite observar la casa desde una vista elevada y en perspectiva. Finalmente se dibujan el terreno, la estructura principal de la casa y el techo.

La función main() controla la ejecución completa del programa. Inicializa GLFW, crea la ventana de visualización, configura el contexto de OpenGL y ejecuta el ciclo principal de renderizado hasta que el usuario cierre la aplicación.

Conclusión

Durante esta práctica se implementó una escena tridimensional texturizada utilizando OpenGL. Se aplicaron conceptos relacionados con la carga y administración de texturas, la construcción de objetos geométricos básicos y la configuración de cámaras en entornos 3D.

El uso de diferentes imágenes para representar el pasto, las paredes y el techo permitió mejorar significativamente el aspecto visual de la escena, demostrando cómo las texturas contribuyen al realismo en los gráficos por computadora. Asimismo, el proyecto sirvió para reforzar conocimientos sobre renderizado, coordenadas UV y manejo de recursos gráficos dentro de aplicaciones tridimensionales.
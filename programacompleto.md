Programa Completo Con Realidad Aumentada con ArUco y OpenGL

Introducción

La Realidad Aumentada (RA) es una tecnología que permite combinar elementos virtuales con el entorno real capturado por una cámara. Mediante técnicas de visión por computadora es posible detectar objetos o marcadores específicos dentro de una imagen y utilizar su posición para colocar modelos tridimensionales en tiempo real.

En esta práctica se desarrolló una aplicación de Realidad Aumentada utilizando Python, OpenCV, OpenGL y GLFW. El sistema detecta un marcador ArUco mediante la cámara web y calcula su posición y orientación en el espacio. A partir de esta información se renderiza un objeto tridimensional sobre el marcador, logrando la integración entre el mundo real y el virtual.

Codigo
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import (
    GLU_FILL,
    gluNewQuadric,
    gluQuadricDrawStyle,
    gluSphere,
)


CAMERA_INDEX = 0
MARKER_LENGTH_M = 0.10  
ARUCO_DICT = cv2.aruco.DICT_4X4_50
MARKER_ID = 0  
MODEL_SCALE = 0.04  
OBJECT_MODE = "sphere"  
WINDOW_TITLE = "RA: ArUco + OpenGL (T=tetera/esfera, ESC=salir)"
ZNear, ZFar = 0.01, 100.0

SCRIPT_DIR = Path(__file__).resolve().parent
CALIB_NPZ = SCRIPT_DIR / "camera_ar.npz"


def default_camera_matrix(width: int, height: int) -> np.ndarray:
    f = float(max(width, height))
    cx, cy = width / 2.0, height / 2.0
    return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]], dtype=np.float64)


def load_calibration(width: int, height: int):
    if CALIB_NPZ.is_file():
        data = np.load(CALIB_NPZ)
        return data["camera_matrix"], data["dist_coeffs"]
    return default_camera_matrix(width, height), np.zeros((5, 1), dtype=np.float64)


def make_aruco_detector():
    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
    params = cv2.aruco.DetectorParameters()
    if hasattr(cv2.aruco, "ArucoDetector"):
        return cv2.aruco.ArucoDetector(dictionary, params), dictionary
    return None, dictionary


def detect_marker(gray, detector, dictionary):
    if detector is not None:
        corners, ids, _ = detector.detectMarkers(gray)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, dictionary, parameters=cv2.aruco.DetectorParameters()
        )
    if ids is None or len(ids) == 0:
        return None, None, None
    idx = 0
    if MARKER_ID is not None:
        matches = np.where(ids.flatten() == MARKER_ID)[0]
        if len(matches) == 0:
            return None, None, None
        idx = int(matches[0])
    return corners[idx], ids[idx], idx


def marker_object_points(side_length):
    s = side_length / 2.0
    return np.array([[-s, s, 0], [s, s, 0], [s, -s, 0], [-s, -s, 0]], dtype=np.float32)


def estimate_pose(corners, camera_matrix, dist_coeffs):
    image_points = corners[0] if corners.ndim == 3 else corners
    image_points = np.asarray(image_points, dtype=np.float32).reshape(-1, 2)
    obj_pts = marker_object_points(MARKER_LENGTH_M)
    flags = cv2.SOLVEPNP_IPPE_SQUARE if hasattr(cv2, "SOLVEPNP_IPPE_SQUARE") else cv2.SOLVEPNP_ITERATIVE
    ok, rvec, tvec = cv2.solvePnP(obj_pts, image_points, camera_matrix, dist_coeffs, flags=flags)
    if not ok:
        raise RuntimeError("solvePnP falló")
    return rvec, tvec


def projection_from_k(K, width, height, znear, zfar):
    fx, fy = K[0, 0], K[1, 1]
    cx, cy = K[0, 2], K[1, 2]
    P = np.zeros((4, 4), dtype=np.float32)
    P[0, 0] = 2.0 * fx / width
    P[1, 1] = 2.0 * fy / height
    P[0, 2] = (width - 2.0 * cx) / width
    P[1, 2] = (2.0 * cy - height) / height
    P[2, 2] = -(zfar + znear) / (zfar - znear)
    P[2, 3] = -1.0
    P[3, 2] = -2.0 * zfar * znear / (zfar - znear)
    return P


def modelview_from_pose(rvec, tvec) -> np.ndarray:
    R, _ = cv2.Rodrigues(rvec)
    M = np.eye(4, dtype=np.float64)
    M[:3, :3] = R
    M[:3, 3] = tvec.flatten()
    cv_to_gl = np.diag([1.0, -1.0, -1.0, 1.0])
    return (cv_to_gl @ M).T.astype(np.float32)


_quadric = None
_glut_ready = False


def init_glut_for_geometry():
    global _glut_ready
    if _glut_ready:
        return
    from OpenGL.GLUT import glutInit
    glutInit(sys.argv if sys.argv else [""])
    _glut_ready = True


def draw_sphere(radius: float = 1.0) -> None:
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricDrawStyle(_quadric, GLU_FILL)
    gluSphere(_quadric, radius, 32, 16)


def draw_teapot(scale: float) -> None:
    from OpenGL.GLUT import glutSolidTeapot
    glutSolidTeapot(scale)


def draw_ar_object(mode: str, scale: float) -> None:
    glPushMatrix()
    glTranslatef(0.0, 0.0, scale * 0.5)
    if mode == "sphere":
        glColor3f(0.35, 0.75, 1.0)
        draw_sphere(scale)
    else:
        glColor3f(0.85, 0.45, 0.25)
        draw_teapot(scale)
    glPopMatrix()


def setup_lighting() -> None:
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, (0.2, 0.4, 1.0, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 0.95, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.25, 0.25, 0.25, 1.0))
    glEnable(GL_NORMALIZE)


_tex_id = None
_tex_buf = None


def upload_frame_texture(frame_bgr, width, height) -> None:
    global _tex_id, _tex_buf
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgb = cv2.flip(rgb, 0)
    if _tex_buf is None or _tex_buf.shape[:2] != (height, width):
        _tex_buf = np.empty((height, width, 3), dtype=np.uint8)
    np.copyto(_tex_buf, rgb)
    if _tex_id is None:
        _tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, _tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, _tex_buf
    )


def draw_background_quad(width, height) -> None:
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, _tex_id)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(width, height)
    glTexCoord2f(0, 1)
    glVertex2f(0, height)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)


def draw_scene_3d(rvec, tvec, camera_matrix, width, height, mode, scale) -> None:
    P = projection_from_k(camera_matrix, width, height, ZNear, ZFar)
    MV = modelview_from_pose(rvec, tvec)
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(P)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMultMatrixf(MV)
    setup_lighting()
    draw_ar_object(mode, scale)


def main() -> None:
    global OBJECT_MODE, MODEL_SCALE

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.", file=sys.stderr)
        sys.exit(1)

    ret, probe = cap.read()
    if not ret:
        sys.exit(1)

    cam_h, cam_w = probe.shape[:2]
    camera_matrix, dist_coeffs = load_calibration(cam_w, cam_h)
    detector, dictionary = make_aruco_detector()

    if OBJECT_MODE == "teapot":
        init_glut_for_geometry()

    if not glfw.init():
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    window = glfw.create_window(cam_w, cam_h, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    def on_key(win, key, _scancode, action, _mods):
        global OBJECT_MODE, MODEL_SCALE
        if action != glfw.PRESS:
            return
        if key in (glfw.KEY_ESCAPE, glfw.KEY_Q):
            glfw.set_window_should_close(win, True)
        elif key == glfw.KEY_T:
            OBJECT_MODE = "sphere" if OBJECT_MODE == "teapot" else "teapot"
            if OBJECT_MODE == "teapot":
                init_glut_for_geometry()
        elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):
            MODEL_SCALE *= 1.1
        elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):
            MODEL_SCALE /= 1.1

    glfw.set_key_callback(window, on_key)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        ret, frame = cap.read()
        if not ret:
            continue
        h, w = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, _, _ = detect_marker(gray, detector, dictionary)

        glViewport(0, 0, w, h)
        upload_frame_texture(frame, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background_quad(w, h)

        if corners is not None:
            rvec, tvec = estimate_pose(corners, camera_matrix, dist_coeffs)
            draw_scene_3d(rvec, tvec, camera_matrix, w, h, OBJECT_MODE, MODEL_SCALE)

        glfw.swap_buffers(window)
        glfw.poll_events()

    cap.release()
    glfw.terminate()


if __name__ == "__main__":
    main()
    
Funcionamiento del Código

El programa comienza inicializando la cámara web para capturar video en tiempo real. Posteriormente se carga la información de calibración de la cámara, la cual es necesaria para obtener una proyección más precisa de los objetos virtuales sobre la imagen capturada.

Para la detección del marcador se utiliza la biblioteca OpenCV y específicamente los marcadores ArUco. Cada cuadro capturado por la cámara es convertido a escala de grises y analizado para localizar el marcador configurado en el sistema. Una vez detectado, se calculan sus esquinas y se determina su pose mediante el algoritmo SolvePnP, obteniendo así los vectores de rotación y traslación.

Con la información de la pose se construye una matriz de transformación que permite convertir las coordenadas del sistema de visión por computadora al sistema de coordenadas utilizado por OpenGL. Esto hace posible posicionar correctamente el objeto virtual sobre el marcador detectado.

La imagen proveniente de la cámara se utiliza como fondo de la escena mediante una textura aplicada a un cuadrilátero que ocupa toda la ventana. Sobre esta imagen se renderiza posteriormente la escena tridimensional utilizando OpenGL.

El sistema permite mostrar dos modelos diferentes: una esfera o una tetera tridimensional. Estos modelos son iluminados mediante una fuente de luz configurada en OpenGL, lo que mejora su apariencia visual y proporciona sensación de profundidad. Además, se pueden modificar dinámicamente mediante el teclado, permitiendo cambiar entre modelos y ajustar su escala.

Durante la ejecución, el objeto virtual permanece anclado al marcador ArUco. Si el usuario mueve o rota el marcador frente a la cámara, el modelo tridimensional sigue esos movimientos en tiempo real, generando el efecto característico de la Realidad Aumentada.

Conclusión

La práctica permitió comprender el funcionamiento básico de un sistema de Realidad Aumentada basado en marcadores. Mediante la combinación de OpenCV para la detección y estimación de pose, junto con OpenGL para el renderizado gráfico, fue posible integrar objetos tridimensionales dentro de una escena real capturada por una cámara.

Asimismo, se aplicaron conceptos importantes como calibración de cámara, transformación de coordenadas, matrices de proyección, iluminación y renderizado 3D. El resultado demuestra cómo distintas herramientas de visión por computadora y gráficos pueden trabajar de manera conjunta para crear aplicaciones interactivas de Realidad Aumentada en tiempo real.
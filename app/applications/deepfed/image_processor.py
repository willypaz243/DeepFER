import cv2
import dlib
import numpy as np


def enderezar_imagen(gray, angulo):
    x, y = gray.shape
    center = tuple(np.array(gray.shape) / 2)
    giro = cv2.getRotationMatrix2D(center=center, angle=angulo, scale=1)
    gray = cv2.warpAffine(gray, giro, (x, y))
    return gray


def calcular_angulo(reference_points):
    punto1, punto2 = reference_points
    catetos = punto2-punto1
    radio = np.linalg.norm(catetos)
    angulo = np.degrees(np.arcsin(catetos[1] / radio))
    return angulo


def obtener_recorte(gray, point, escala):
    img_shape = min(gray.shape)
    x1, y1 = point - img_shape // np.array(escala)
    x2, y2 = point + img_shape // np.array(escala)
    x1 = x1*int(x1 > 0)
    y1 = y1*int(y1 > 0)
    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))
    gray = gray[y1: y2, x1: x2]
    # if min(gray.shape) > 8:
    #    gray = cv2.resize(gray, (256,256))
    return gray


def rotar_puntos(puntos, angulo, centro):
    vectores = puntos - centro
    radios = np.linalg.norm(vectores, axis=1)
    # print(radios.max())
    x = vectores[:, 0]
    y = vectores[:, 1]
    #angulos = 360*(vectores[:,1] < 0) - (np.degrees(np.arccos(vectores[:,0] / radios)) - angulo)
    angulos = 360*((y < 0) * (x > 0))+180*((x < 0) * (y < 0))+180 * \
        ((x < 0) * (y > 0))+np.degrees(np.arctan(y/(x+1e-100)))
    angulos = np.deg2rad(angulos)
    puntos[:, 0] = radios * np.cos(angulos)
    puntos[:, 1] = radios * np.sin(angulos)
    puntos = puntos + centro
    radios = np.linalg.norm(centro-puntos, axis=1)
    # print(radios.max())
    return np.round(puntos).astype('int')

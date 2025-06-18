import os
import sys

import cv2
import dlib
import numpy as np

from .image_processor import (
    calcular_angulo,
    enderezar_imagen,
    obtener_recorte,
    rotar_puntos,
)

path = os.path.dirname(__file__)
path = os.path.join(path, "shape_predictor_68_face_landmarks.dat")
predictor = dlib.shape_predictor(path)

def escalar_img(gray):
    x, y = gray.shape
    scala = 512 / y
    gray = cv2.resize(gray, (round(y*scala), round(x*scala)))
    return scala, gray

def get_data(partes):
    """Normaliza las parte, una lista con tres matrices de valores 0-255, 
    a matrices con valores del 0-1 y cambia la forma de las matrices tal que
    sea compatible con el Input del modelo de red neuronal.
    
    Arguments:
    
        partes (list): Una lista con 3 matrices `numpy.ndarray`
    
    Returns:
    
        `numpy.ndarray`, una matriz con los valores normalizados y con la forma de
            (1x96x96x1)
    """
    datos = []
    for parte in partes:
        parte = cv2.resize(parte, (96,96))
        parte = parte / 255
        parte = parte.reshape((1,96,96,1))
        datos.append(parte)
    return datos
        
def get_face_parts(gray, key_points):
    """Toma una la que contiene unicamente el rostro y la divide en tres parte
    ojo derecho, ojo izquierdo y labios.
    
    Arguments:
    
        gray (numpy.ndarray): Una matriz que representa una imagen 
            a escalda de grises, la imagen debe de ser la de un rostro humano
        
        key_points (numpy.ndarray): Una matriz de 68 x 2, 68 puntos clave del
            rostro de la imagen
    
    Returns:
    
        Un `tuple` con dos objetos:
        
            --`partes`: Una `list` con tres imagenes las cuales son el ojo derecho,
            el ojo izquierdo y los labios
            --`key_points`: El mismo `numpy.ndarray` que se ingresó por parametro.
    """
    angulo = calcular_angulo([key_points[36], key_points[45]])
    gray = enderezar_imagen(gray, angulo)
    key_points = rotar_puntos(key_points, angulo, np.array(gray.shape) / 2)
    points = [key_points[36:42].mean(axis=0),
              key_points[42:48].mean(axis=0),
              key_points[30]+ [0, 20]]
    #print(key_points[30])
    escalas = [5, 5, [4,5]]
    partes = []
    for punto, escala in zip(points, escalas):
        parte = obtener_recorte(gray, punto, escala)
        partes.append(parte)
    return partes, key_points
    
        
def get_key_points(gray):
    """Obtiene puntos clave ubicadas en lugares caracteristicos del rostro
    en la imagen suponiendo que solo recibirá imagenes con un rostro.
    
    Arguments:
    
        gray (numpy.ndarray): Una matriz que representa una imagen
            a escalda de grises
    
    Returns:
    
        `numpy.ndarray` -- Una matriz de 68 x 2, 68 puntos de foma (x, y).
    """
    
    x,y = gray.shape
    face = dlib.rectangle(0, 0, y, x)
    key_points = predictor(gray, face)
    key_points = key_points_to_numpy(key_points)
    return key_points

def key_points_to_numpy(key_points):
    points = []
    for point in key_points.parts():
        points.append([point.x, point.y])
    return np.array(points)

def get_date_features(key_points):
    """Obtiene algunas caracteristicas de un rostro usando sus `key_points`
    calculando por ejemplo, la distancias entre las cejas, las posición de los
    puntos de los labios con respecto a otros puntos del rostro, etc.
    
    Estas medidas nos servira como datos adicionales para predecir las emociones
    
    Arguments:
        key_points (numpy.ndarray): Una matriz de 68 x 2, 68 puntos clave del
            rostro de la imagen
    
    Returns:
        `numpy.ndarray` -- Una matriz de 1 x 13, 13 caracteristicas del rostro.
    """
    location_pts_init = [21,21,22,19,24,37,44,51,36,45,48]
    location_pts_fin =  [22,31,35,41,46,41,46,57,48,54,54]
    dists = np.linalg.norm(key_points[location_pts_init] - key_points[ location_pts_fin ], axis=1)
    
    dist_lips = np.linalg.norm(key_points[[48,54]].mean(axis=0) - key_points[51])
    dist_eyebrows_to_nose = np.linalg.norm(key_points[[21,22]].mean(axis=0) - key_points[27])
    #print(dist_lips, dist_eyebrows_to_nose, dists)
    dists = np.concatenate([dists, [dist_lips, dist_eyebrows_to_nose]], axis=0)
    
    return dists.reshape((1,13))
from os.path import abspath, join, dirname

import numpy as np
from dlib import get_frontal_face_detector
from tensorflow import concat
from keras.models import load_model

from .process_data import (escalar_img, get_data, get_date_features,
                           get_face_parts, get_key_points)


class FedPredictor:
    def __init__(self):
        path = dirname(__file__)
        path = join(path, 'trained_models/dfer_model.h5')
        self.modelo = load_model(path)
        self.detector = get_frontal_face_detector()

    def predict_one(self, gray):
        """Predice la emocion relacionada con la expresion facial detectada del 
        rostro de una persona en la imagen, en caso de existir mas de un rostro 
        tomara el rostro que este en el primer plano (el mas cercano).

        Arguments:

            gray (numpy.ndarray): Una matriz que representa una 
                imagen que contenga un rostro humano.

        Returns:

            Retorna un `tuple` con dos objetos

                --`rectangulo`: de tipo `numpy.ndarray`, una matriz de 2 x 2
                que marca la localiacion del rostro detectado, la primera fila es 
                la cordenada de punto inical del rectangulo y la segunda 
                fila es el punto final.

                --`prediccion`: un vector `numpy.ndarray` de 7 numeros reales 
                entre 0-1, la posición de cada valor representa una emoción 
                y cada valor representa el porcentaje de cada emoción.

                Pocición | Emoción \n
                ---------+-------- \n
                    0    | Alegria \n
                    1    | Neutral \n
                    2    | Tristeza\n
                    3    | Enfado  \n
                    4    | Asco    \n
                    5    | Sorpresa\n
                    6    | Miedo   \n

            Retorna un `tuple` con dos valores `None` en el caso de no detectar
            algun rostro


        """
        scala, gray = escalar_img(gray)
        faces = self.detector(gray)
        face = self.__face_in_firt_plane(faces)

        if face is not None:
            # obtiene los valores de face en un numpy.ndarray para facilidad de uso.
            rectangulo = np.array([
                [face.left(),  face.top()],
                [face.right(), face.bottom()]
            ])
            # aumenta el margen del rectangulo un 10% del tamaño del rectangulo.
            rectangulo = rectangulo + np.round(rectangulo*0.1).astype('int') * [[-1], [1]]

            (x1, y1), (x2, y2) = rectangulo

            rectangulo = np.int32(rectangulo / scala)
            prediccion = self.__predict([gray[y1: y2, x1: x2]])[0]

            return rectangulo, prediccion
        else:
            return None, None

    def predict_many(self, gray):
        """Predice la emoción relacionada a la expresión facial asociada a 
        cada rostro detectado en una imagen.

        Arguments:
            gray (numpy.ndarray): Una matriz que representa una imagen 
                a escala de grises que contenga un o varios rostros humanos

        Returns:

            Retorna un `tuple` que contiene dos objetos

                --`rectangulos`: Una lista de tipo `numpy.ndarray`
                que contiene una cantidad de elementos `rectangulo` igual a la 
                cantidad de rostros detectados en la imagen

                --`predicciones`: Una lista de tipo `numpy.ndarray` que 
                contiene la misma cantidad de rostros detectados que vectores 
                de tipo `numpy.ndarray` con 7 valores del 0-1, la posición de
                cada valor representa una emoción y cada valor representa 
                el porcentaje de cada emoción.

                Pocición | Emoción \n
                ---------+-------- \n
                    0    | Alegria \n
                    1    | Neutral \n
                    2    | Tristeza\n 
                    3    | Enfado  \n
                    4    | Asco    \n
                    5    | Sorpresa\n
                    6    | Miedo   \n


            Retorna un `tuple` con dos valores `None` en el caso de no detectar
            algun rostro

        """
        scala, gray = escalar_img(gray)
        faces = self.detector(gray)
        gray_images = []
        rectangulos = []
        for face in faces:
            rectangulo = np.array([
                [face.left(),  face.top()],
                [face.right(), face.bottom()]
            ])
            rectangulo = rectangulo + np.round(rectangulo*0.1).astype('int') * [[-1], [1]]
            (x1, y1), (x2, y2) = rectangulo
            gray_images.append(gray[y1: y2, x1: x2])
            rectangulos.append(np.int32(rectangulo / scala))

        if rectangulos:
            rectangulos = np.array(rectangulos)
            predicciones = self.__predict(gray_images)
            return rectangulos, predicciones
        else:
            return None, None

    def __face_in_firt_plane(self, faces):
        """Toma una lista de `dlib.rectangles` de las cuales elige para devolver
        el `dlib.rectangle` de mayor área, es decir el rostro detectado que mas 
        ocupa la imagen.

        Arguments:

            faces (dlib.rectangles): Un listado de rectangulos que marcan la 
            ubicación de los rostros detectados.

        Returns:

            Retorna `dlib.rectangle`: El rectangulo de mayor área de los detectados,
            se puede tomar como el rostro detectado mas cercano a la cámara.
        """
        face_max = None
        for face in faces:
            if face_max is not None:
                if face.area() > face_max.area():
                    face_max = face
            else:
                face_max = face
        return face_max

    def __predict(self, imgs_recortadas):
        """Realiza una predicción usando el un modelo entrenado para clasificar
        emociones mediante el rostro, haciendo previamente un preprocesamiento
        de las imagenes que recibe como entrada.

        El modelo recibe como entrada un `List` o un `numpy.ndarray` que contiene
        `n` cantidad de imagenes preprocesada y divididas en 3 partes concatenada
        con 13 caracteristicas consideradas importantes del rostro y devuelve
        `n` vectores de 7 valores del 0-1.

        Arguments:

            imgs_recortadas (List, numpy.ndarray): Un listado de imagenes con
            un solo rostro en cada imagen y que el rostro ocupe casi toda la imagen.

        Returns:

            Retorna `prediccion` un `numpy.ndarray` 
        """
        imgs_data = []
        features_data = []

        for img_gray in imgs_recortadas:
            key_points = get_key_points(img_gray)
            partes, key_points = get_face_parts(img_gray, key_points)
            data = get_data(partes)
            features_data.append(get_date_features(key_points))
            imgs_data.append(data)

        imgs_data = np.concatenate(imgs_data, axis=1)
        imgs_data = concat(imgs_data, axis=1)
        features_data = concat(features_data, axis=0)
        input_data = list(imgs_data)
        input_data.append(features_data)

        prediccion = self.modelo(input_data).numpy()

        return prediccion

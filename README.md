# Deep Facial Expression Recognition
Reconocimiento de Expresiones faciales con Deep Learning.
_El objetivo de este programa es el de poder reconocer y clasificar las 7 expresiones faciales basicas de un rostro humano
usando deep learning, el programa recibirá una o varias imagenes en el cual podra detectar rostros humanos y predecir su expressión._

## 1. ¿Cómo funciona?

El funcionamiento de este programa se puede dividir en 3 partes pre-procesado de la imagen, extraccion de datos y predicción.

### 1.1 Pre-proceso de imagen.

Esta tares de divide en los siguientes pasos.

#### 1.1.1 Deteccion de rostros.
Antes de hacer una prediccion necesitamos detectar si existe algun rostro en la imagen o imagenes de entrada, para esto usamos
la funcion de la libreria [dlib](http://dlib.net/) *get_frontal_face_detector()* para obtener las cordenadas de uno o varios
rostros en una imagen.

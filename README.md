# Deep Facial Expression Recognition
Reconocimiento de Expresiones faciales con Deep Learning.
_El objetivo de este programa es el de poder reconocer y clasificar las 7 expresiones faciales basicas de un rostro humano
usando deep learning, el programa recibirá una o varias imagenes en el cual podra detectar rostros humanos y predecir su expressión._

## 1. ¿Cómo funciona?

El funcionamiento de este programa se puede dividir en 3 partes pre-procesado de la imagen, extraccion de datos y predicción.

### 1.1 Pre-proceso de imagen.

Esta tares de divide en los siguientes pasos.

#### 1.1.1 Reduccion y Ecualización de la imagen.
Obtenemos una version a escala de grises de la imagen y la reducimos a una escala tal que el ancho de la imagen de entrada sea de 512px esto con el objetivo de hacer el programa mas ligero y rápido.
Ecualizamos la imagen con la libreria de [OpenCV](https://opencv.org/), con la función *cv2.equalizeHist()* para evitar que el resultado final sea afectado por la diferencia de iluminacion en las imagenes.

#### 1.1.2 Recortar y Enderezar el rostro.
Con la libreria [dlib](http://dlib.net/) haciendo uso de *get_frontal_face_detector()* que nos retorna un modelo capaz de localizar rostros en una imagen, Se recorta el rostro o rostros de la imagen y luego se porcede a enderezar aquel rostro, para que el rostro quede derecho rotamos la imagen hasta que los ojos esten a la misma altura con respecto a la altura total de la imagen recortada. para saber la localización de los ojos tambien hacemos uso de [dlib](http://dlib.net/).*shape_predictor("shape_predictor_68_face_landmarks.dat")* esta funcion nos retorna puntos clave (keyPoints) que nos seran utiles para extraer caracteristicas que nos resulten utiles para el objetivo final de este programa.

### 1.2 Extraccion de datos.

El modelo de red neuronal profunda (deep neural network), requiere que se ingresen datos en un formato especifico.
En este caso se usa directamente las imagenes de los rostros que obtuvimos durante el pre-procesamiento, ya que el rostro aparte de expresar emociones tambien tiene caracteristicas unicas en cada rostro, y puede afectar a la prediccion de una expresión en diferentes personas.

Para evitar este sesgo de predicción, Extraeremos tres puntos de interes en el rostro y una serie de caracteristicas determinantes de cada expresión.

#### 1.2.1 Áreas de interéz.
Existes tres Áreas de interés en las que son mas notorias las expreciones faciales, estas son los ojos y los labios, entonces hacien uso se los keypoints obtenidos durante el pre-pocesamiento, se localizan el area de los ojos y labios, obteniendo asi tres imagenes ojo izquierdo, derecho y labios en una lista.

#### 1.2.2 Extraccion de caracteristicas.
Haciendo uso nuevamente de los Keypoints se obtiene una serie de caracteristicas que diferentes en cada exprecion facial, en este caso se utiliza la distancia entre componentes del rostro que varian en cada expresion, por ejemplo: la distancia entre las cejas y los ojos, distancia entre las cejas, distancia entre el labio superior e inferior, etc.

Estos datos irán concatenados a lista de imagenes de Areas de interes para introducirlos como entrada en el modelo de deep learning.

### 1.3 Modelado de Deep Learning y predicción.
 


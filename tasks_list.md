# Tasks for the project

## TODO

* **user story #1**: as an administrator, I can create a video call session and share a link to share with a candidate, in the video call I can perform the following interactions
  * I can activate and deactivate the camera
  * I can activate and deactivate the microphone
  * I can select the camera
  * I can see a frame that will be black if I have the camera disabled and I will see the camera if it is active
  * I can copy the link to share with new candidates
  * I can visualize the queue of candidates in a list
  * I have a "start next" button that allows me to communicate with the next candidate in the queue
  * I can communicate with the candidate smoothly through the video call
  * during a video call, the "start next" button changes to a "Finish" button, when the "start next" button is pressed, it will return to allow me to attend to the next candidate
    * **task #1**: design an interface for the administrator, the design must contain all the necessary interaction elements to meet the requirements, see cameras, see active microphones, activate camera and microphone, see frame where the camera capture will be visualized
    * **task #2** implement the necessary functions to list all available cameras and microphones on the equipment
    * **task #3** implement the functions to visualize the audio and video capture
    * **task #4** implement the functions necessary to visualize the queue of candidates
    * **task #5** implement the functions to start the video call with the first candidate in the queue
    * **task #6** implement the functions to end the video call
* **user story #2** as a candidate who received a link to communicate with an administrator, when I enter I see a video call interface, I can choose the microphone and camera and see what my camera captures when it is active, I can visualize an audio indicator to check that I have audio in the microphone, when the administrator accepts my request, I can communicate with them in real-time
  * **task #1** design a view for the candidate with the same interaction elements concerning the video call
  
* **user story #3** as an administrator, I can analyze the facial gestures of the candidate using a deep learning model and identify emotions using a button to activate and deactivate the analysis software, this stores a history of emotions regarding the time of the video call
  * **task #1** implement the necessary functionalities to receive the images in real-time of the candidate's face
  * **task #2** implement the necessary classes and objects to feed the model with the images and return the prediction result
  * **task #3** implement the functionalities to store a history of the model's results
  * **task #4** transmit the prediction results in real-time to be viewed by the administrator
  * **task #5** implement a web component to visualize the results in real-time

## In progress

* User story #1 - task # 1 [US1-T1]

## In testing

## Done

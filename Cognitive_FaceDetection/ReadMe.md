
## Cognitive Services
This is a simple demostration to find faces in a photo with **Cognitive Services, Microsoft Azure**.

Basicly the application post some photo to *https://[location].api.cognitive.microsoft.com/face/v1.0/detect* to Cognitive Services Face API.

### FACE API
Face API detects faces in a photo and return some information about it. This simple demostration gets face location info from result and draw a rectangle around the face.

Usage of the code is very simple. All you have to do is just run the below code. Be sure that the path location for your photo is correct.


```python
python FindFaces.py --path '/Users/Arda/Desktop/arda.jpg'
```

![alt text](https://github.com/ardacetinkaya/CognitiveServicePlayGround/blob/master/Cognitive_FaceDetection/result.jpg "Example photo")



### Raspberry Pi

This small code also can be run on Raspberry Pi models. This small demostration is done on Raspberry Pi Zero W, but all other models can be used :)

![alt text](https://github.com/ardacetinkaya/CognitiveServicePlayGround/blob/master/Cognitive_FaceDetection/RaspberrPiZero.JPG?raw=true "Raspberry Pi")

For OS, Rasbian is used. And be sure that Cognitive Service Face API SDK for python is installed. You must have this. So just use **pip** to install it.

```python
pip install cognitive_face
```

### Emotions

Face API also provides some information about emotions. So you may learn about more from a people in photos.

![alt text](https://github.com/ardacetinkaya/CognitiveServicePlayGround/blob/master/Cognitive_FaceDetection/TakenByRaspberryPi.jpg "Raspberry Pi")


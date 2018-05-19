
This is a simple demostration to find faces in a photo with Cognitive Services, Microsoft Azure.

Basicly the application post some photo to https://[location].api.cognitive.microsoft.com/face/v1.0/detect to Cognitive Services Face API.

Face API detects faces in a photo and return some information about it. This simple demostration gets face location info from result and draw a rectangle around the face.

Usage of the code is very simple. All you have to do is just run the below code. Be sure that the path location for your photo is correct.


```python
python FindFaces.py ``-``-path '/Users/Arda/Desktop/arda.jpg'
```




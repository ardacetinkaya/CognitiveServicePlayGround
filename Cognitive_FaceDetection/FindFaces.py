import requests
import sys
import argparse
from io import BytesIO
from PIL import Image, ImageDraw
import cognitive_face as CF
import time
import logging
try:
    import picamera
except ImportError:
    pass

KEY = '<WRITE YOUR API KEY>' #Write your Cognitive Service Key
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  

API_URL='https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'  
API_HEADER = {'Ocp-Apim-Subscription-Key': KEY,
          'Content-Type': 'application/octet-stream'}
API_PARAMS = {'language': 'unk'}
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

def takePhoto():
    resultPath='/home/pi/Projects/CameraApp/image.jpg' #Some custom path to save taken photo
    try:
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(1)
            camera.capture(resultPath)
            camera.stop_preview()
    except Exception, e:
        logging.error(str(e))
    
    return resultPath

def getFaceFromURL(img_url):
    faces=None
    try:
        CF.Key.set(KEY)
        CF.BaseUrl.set(BASE_URL)
        faces = CF.face.detect(img_url)
    except Exception, e:
        logging.error(str(e))
    return faces

def getFaceFromPath(photo):
    data= None
    try:
        img = Image.open(photo)
        binaryImg = BytesIO()
        img.save(binaryImg, format='PNG')
        binaryImg.seek(0)
        img = binaryImg.read()
        imagedata = binaryImg.getvalue()
        binaryImg.close()

        response = requests.post(API_URL,
                        params=API_PARAMS,
                        headers=API_HEADER,
                        data=imagedata)

        response.raise_for_status()
        data = response.json()
        logging.log(logging.WARNING,'Response data: '+str(data))
    except Exception, e:
        logging.error(str(e))
    return data

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', type=str)
        parser.add_argument('--path', type=str)
        args = parser.parse_args()

        if (args.url is None) and (args.path is None):
            logging.log(logging.WARNING,'FindFaces.py --path <photo path> [--url <photo url>]')

        if args.url is not None:
            IMAGE_URL=args.url
            faces=getFaceFromURL(IMAGE_URL)
            response = requests.get(IMAGE_URL)
            img = Image.open(BytesIO(response.content))
        elif args.path is not None:
            IMAGE_PATH=args.path
            faces = getFaceFromPath(IMAGE_PATH)
            img = Image.open(IMAGE_PATH)
        else:
            logging.log(logging.WARNING,'No argument is given. Raspberry Pi Cam. will take for your photo.Wait a second... :)')
            IMAGE_PATH=takePhoto()
            faces = getFaceFromPath(IMAGE_PATH)
            img = Image.open(IMAGE_PATH)
        
        draw = ImageDraw.Draw(img)

        if faces is not None:
            if len(faces)==0:
                logging.warning('No photo is taken...')
                sys.exit(12)

            for face in faces:
                draw.rectangle(getRectangle(face), outline='red')
            timestr = time.strftime("%Y%m%d-%H%M%S")
            img.save(timestr+'_result.jpg')
            logging.warning('It''s done.')
    except Exception, e:
        logging.error('Something is wrong!!! ):')
        logging.error(' Detail:'+str(e))

if __name__ == '__main__':
    main()

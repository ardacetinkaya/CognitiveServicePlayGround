import requests
import sys
import argparse
from io import BytesIO
from PIL import Image, ImageDraw
import cognitive_face as CF
import time
import logging

KEY = '<WRITE YOUR API KEY>' #Write your Cogniteve Servie Key
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  

API_URL='https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'  
API_HEADER = {'Ocp-Apim-Subscription-Key': KEY,
          'Content-Type': 'application/octet-stream'}
API_PARAMS = {'language': 'unk'}


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
            print('FindFaces.py --path <photo path> [--url <photo url>]')
            sys.exit()

        if args.url is not None:
            IMAGE_URL=args.url
            faces=getFaceFromURL(IMAGE_URL)
            response = requests.get(IMAGE_URL)
            img = Image.open(BytesIO(response.content))
        elif args.path is not None:
            IMAGE_PATH=args.path
            faces = getFaceFromPath(IMAGE_PATH)
            img = Image.open(IMAGE_PATH)
        
        draw = ImageDraw.Draw(img)

        if faces is not None:
            for face in faces:
                draw.rectangle(getRectangle(face), outline='red')
            img.save('result.jpg')
    except Exception, e:
        logging.error('Something is wrong!!! ):')
        logging.error(' Detail:'+str(e))

if __name__ == '__main__':
    main()

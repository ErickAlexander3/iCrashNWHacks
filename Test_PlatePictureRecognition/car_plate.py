#!/usr/bin/python

import requests
import base64
import json

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
IMAGE_PATH = '/Users/bolinwang/Downloads/car_plate_testing(5).jpg'
SECRET_KEY = 'sk_4170e41fafb3b3478a83269f'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

#print(json.dumps(r.json(), indent=1))

returned_json = json.loads(json.dumps(r.json()))
print(returned_json["results"][0]["plate"])


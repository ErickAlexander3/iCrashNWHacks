import RPi.GPIO as GPIO
import time
import subprocess
import requests
import base64
import json
import os

dirname = os.path.dirname(__file__)

SECRET_KEY = 'sk_4170e41fafb3b3478a83269f'
IMAGE_PATH = os.path.join(dirname, 'image.jpg')
URL = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 60:
                subprocess.call(['./take_photo.sh'])
                
                with open(IMAGE_PATH, 'rb') as image_file:
                    img_base64 = base64.b64encode(image_file.read())
                
                """
                r = requests.post(URL, data = img_base64)
                
                returned_json = json.loads(json.dumps(r.json()))
                if len(returned_json["results"]) > 0:
                    print(returned_json["results"][0]["plate"])
                else:
                    print("No plate recognized")
                """
                
            time.sleep(0.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
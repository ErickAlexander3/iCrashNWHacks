import RPi.GPIO as GPIO
import time
import subprocess
import requests
import base64
import json
import os
from collections import deque
from threading import Thread
import queue
from Bluetin_Echo import Echo

dirname = os.path.dirname(__file__)

SECRET_KEY = 'sk_4170e41fafb3b3478a83269f'
URL = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

pic_requests_queue = queue.Queue()
plate_requests_queue = queue.Queue()
session_queue = deque(maxlen=12)
parked_queue = deque(maxlen=12)
time_of_last_detection = None
distances = deque(maxlen=6)
license_plate = None

def plate_detection():
    global license_plate
    
    while True:
        plate_request = plate_requests_queue.get()
        if plate_request is not None:
            print("detecting plate in image " + plate_request)
        
            image_path = os.path.join(dirname, plate_request)

            with open(image_path, 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())
            
            r = requests.post(URL, data = img_base64)
            
            returned_json = json.loads(json.dumps(r.json()))
            if len(returned_json["results"]) > 0:
                license_plate = returned_json["results"][0]["plate"]
                print("plate is " + license_plate)
                #TODO: make request setting the plate on the current session
                with plate_requests_queue.mutex:
                    plate_requests_queue.queue.clear()
            else:
                print("No plate recognized")
                
            os.remove(plate_request)
            plate_requests_queue.task_done()

        time.sleep(0.5)
        
def distance_detector():
    
    global time_of_last_detection
    global license_plate
    
    while True:
        dist = distance() 
        #print ("Measured Distance = %.1f cm" % dist)
        if not license_plate:
            if dist < 160:
                if time_of_last_detection is None:
                    print("session started")
                    #TODO: make request starting session here
                    time_of_last_detection = time.time()
                distances.append(dist)
                #print(list(distances))
                if license_plate is None and len(distances) == 6:
                    items = list(distances)
                    max_val = max(items)
                    min_val = min(items)
                    #print("difference is " + str(max_val - min_val))
                    if max_val - min_val < 30 and plate_requests_queue.qsize() < 1:
                        pic_requests_queue.put(".")
                        time.sleep(2)
            elif dist < 300:
                    print("session cleared")
                    #TODO: request telling the server to end session
                    distances.clear()
                    session_queue.clear()
                    time_of_last_detection = None
                    
            session_queue.append(dist)
            if time_of_last_detection is not None and min(session_queue) > 300:
                print("session without plate ended due to inactivity")
                #TODO: request telling server to end session
                distances.clear()
                session_queue.clear()
                time_of_last_detection = None
        else:
            parked_queue.append(dist)
            if len(parked_queue) == 12:
                items = list(parked_queue)
                #print(items)
                min_val = min(items)
                if min_val > 300:
                    print("license plate cleared, session ended")
                    #TODO: request telling server to end session
                    distances.clear()
                    parked_queue.clear()
                    license_plate = None
                    time_of_last_detection = None
            
            
        time.sleep(0.25)
        
def pic_taker():
    while True:
        pic_request = pic_requests_queue.get()
        if pic_request is not None:
            file_name = 'image_' + str(time.time()) + '.jpg'
            print(file_name)
            
            subprocess.call("fswebcam -r 1920x1080 " + file_name + " -S 1 --no-banner", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
            plate_requests_queue.put(file_name)
            pic_requests_queue.task_done()

        time.sleep(1)

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
    """
    speed_of_sound = 315
    echo = Echo(GPIO_TRIGGER, GPIO_ECHO, speed_of_sound)
    
    samples = 5
    result = echo.read('cm',  samples)
    return result
    """
    
if __name__ == '__main__':
    try:
        distance_detector_thread = Thread(target=distance_detector)
        pic_taker_thread = Thread(target=pic_taker)
        plate_detection_thread = Thread(target=plate_detection)

        distance_detector_thread.start()
        pic_taker_thread.start()
        plate_detection_thread.start()

 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        echo.stop()
        GPIO.cleanup()
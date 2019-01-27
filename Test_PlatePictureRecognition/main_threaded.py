import time
from threading import Thread
from random import randint
import queue
import os
import requests

dirname = os.path.dirname(__file__)

SECRET_KEY = 'sk_4170e41fafb3b3478a83269f'
IMAGE_PATH = os.path.join(dirname, 'image.jpg')
URL = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)


pic_requests_queue = queue.Queue()
plate_requests_queue = queue.Queue()
time_of_last_detection = None

def plate_detection():
    while True:
        plate_request = plate_requests_queue.get()
        if plate_request is not None:
            print("detecting plate in image " + plate_request)
            os.remove(plate_request)
            plate_requests_queue.task_done()

        time.sleep(0.25)


def distance_detector():
    while True:
        val = randint(0, 1000)
        if val % 20 == 0:
            print("something detected, please take pic (twice)")
            pic_requests_queue.put("do something!")
            pic_requests_queue.put("do something!")
        time.sleep(0.25)


def pic_taker():
    while True:
        pic_request = pic_requests_queue.get()
        if pic_request is not None:
            file_name = f'image_{time.time()}.jpg'
            file = open(file_name, 'w+')
            file.close()
            print(f"created file {file_name}")
            plate_requests_queue.put(file_name)
            pic_requests_queue.task_done()

        time.sleep(0.25)

if __name__ == '__main__':
    try:
        distance_detector_thread = Thread(target=distance_detector)
        pic_taker_thread = Thread(target=pic_taker)
        plate_detection_thread = Thread(target=plate_detection)

        distance_detector_thread.start()
        pic_taker_thread.start()
        plate_detection_thread.start()

    except KeyboardInterrupt:
        print("Program stopped")
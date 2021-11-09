import time
import sys
import cv2
import os
import base64

from kafka import KafkaProducer
from kafka.errors import KafkaError

cpath = os.path.dirname(os.path.abspath(__file__))

producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'video'


def emit_video(path_to_video):
    print('start')

    video = cv2.VideoCapture(path_to_video)

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        frame = cv2.resize(frame, (1600, 900))

        img = cv2.imencode('.jpeg', frame)[1].tobytes()

        future = producer.send(topic, img)

        try:
            future.get(timeout=10)
        except KafkaError as e:
            print(e)
            break


emit_video(os.path.join(cpath, '1.mp4'))

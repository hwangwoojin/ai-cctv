import torch
import os
import cv2
import base64
import numpy as np
import json

from kafka import KafkaConsumer

topic = 'video'

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer(topic,
                         bootstrap_servers=['localhost:9092'])


model = torch.hub.load('ultralytics/yolov5',
                       'yolov5n6',
                       verbose=False)

for message in consumer:
    data = np.frombuffer(message.value, np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cpath = os.path.dirname(os.path.abspath(__file__))

    result = model(img)

    res = result.crop(save_dir='./')

import tqdm
import os
import cv2
import torch
import numpy as np
import pandas as pd
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose
from fastapi import FastAPI
from fastapi_socketio import SocketManager
from model import bootstrap, get_pose, get_yolo

app = FastAPI()
socket_manager = SocketManager(app=app, cors_allowed_origins=[
                               "http://localhost:3000"], mount_location='/')


@ app.get("/")
def read_root():
    return {"Hello": "World"}


@ socket_manager.on('start')
async def handle_socket(sid, *args, **kwargs):
    # Open the video.
    video_cap = cv2.VideoCapture("../videos/c.mp4")
    video_n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_fps = video_cap.get(cv2.CAP_PROP_FPS)
    video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # do bootstrap
    # bootstrap()
    pose_tracker, pose_embedder, pose_classifier = get_pose()
    model = get_yolo()

    # Run classification on a video.
    frame_idx = 0
    least_send_frame = 0
    output_frame = None
    results = {}
    with tqdm.tqdm(total=video_n_frames, position=0, leave=True) as pbar:
        while True:
            success, input_frame = video_cap.read()
            if not success:
                break
            if frame_idx - least_send_frame < 10:
                frame_idx += 1
                continue
            frames = model(input_frame)
            frames = frames.pandas().xyxy[0]
            for frame_index in range(len(frames)):
                xmin, ymin, xmax, ymax, _, _, _ = frames.values[frame_index]
                xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
                _input_frame = input_frame[ymin: ymax, xmin: xmax]
                _input_frame = cv2.cvtColor(_input_frame, cv2.COLOR_BGR2RGB)
                result = pose_tracker.process(image=_input_frame)
                pose_landmarks = result.pose_landmarks
                output_frame = _input_frame.copy()
                if pose_landmarks is not None:
                    mp_drawing.draw_landmarks(
                        image=output_frame,
                        landmark_list=pose_landmarks,
                        connections=mp_pose.POSE_CONNECTIONS)
                if pose_landmarks is not None:
                    frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
                    pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                                              for lmk in pose_landmarks.landmark], dtype=np.float32)
                    assert pose_landmarks.shape == (
                        33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)
                    pose_classification = pose_classifier(pose_landmarks)

                    for _pose in pose_classification:
                        if pose_classification[_pose] >= 9 and _pose != 'two' and _pose != 'standing' and _pose != 'sitting':
                            _image = cv2.imencode('.jpeg', output_frame)[
                                1].tobytes()
                            await socket_manager.emit('data', {'action': _pose, 'image': _image, 'key': frame_idx})
                            least_send_frame = frame_idx
                            break
                else:
                    pose_classification = None
            frame_idx += 1
            pbar.update()
    pose_tracker.close()

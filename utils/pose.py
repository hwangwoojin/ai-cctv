import os
import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def parse(e):
    result = []
    for l in e:
        result.extend([l.x, l.y, l.z])
    return result


def mediapipe(path):
    image = cv2.imread(path)
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if (results.pose_world_landmarks):
            return parse(results.pose_world_landmarks.landmark)
        else:
            return None


path = '../images'

pose_list = []
for action in os.listdir(path):
    subdir = os.path.join(path, action)
    for i, image in enumerate(os.listdir(subdir)):
        print(f'{i}/{len(os.listdir(subdir))}')
        imagename = os.path.join(subdir, image)
        pose = mediapipe(imagename)

        if (pose is not None):
            pose_list.append(pose)

    filename = f'./{action}.csv'
    with open(filename, 'w') as f:
        for pose in pose_list:
            f.write(','.join(map(str, pose)))
            f.write('\n')
    break

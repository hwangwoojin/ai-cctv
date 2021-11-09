import os
import cv2
import shutil

INPUT_PATH = '../videos/1.mp4'
OUTPUT_PATH = '../images'
META_PATH = '../videos/1.txt'

metas = {}
with open(META_PATH, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        frame, id, left, top, right, bottom, _, _, _, _ = line.split()
        if frame in metas:
            metas[frame].append([id, left, top, right, bottom])
        else:
            metas[frame] = [[id, left, top, right, bottom]]

metas2 = {}
for meta in metas:
    if len(metas[meta]) == 2:
        metas2[meta] = metas[meta]

cap = cv2.VideoCapture(INPUT_PATH)

index = 0
success = True

actions = {'punching': [['1587', '1630'], ['2402', '2471'], ['3122', '3433'], ['3886', '3926'], ['4407', '4524'], ['4846', '4911'], ['4936', '4998'], ['5441', '5543'], ['5928', '6120'], ['6511', '6569'], ['6640', '6781'], ['7065', '7122'], ['7694', '7889'], ['8036', '8107'], ['8543', '8595']], 'pulling': [['1977', '2072'], ['3834', '3926'], ['4407', '4524'], ['4818', '4911'], [
    '5151', '5483'], ['5549', '6777']], 'pushing': [['3710', '3750'], ['4523', '4582']], 'threaten': [['4247', '4298']], 'kicking': [['5668', '5707'], ['6264', '6350'], ['6366', '6416'], ['6774', '6865'], ['6977', '7056'], ['7187', '7470'], ['7974', '8018'], ['8253', '8294'], ['8371', '8420'], ['8461', '8514'], ['8876', '8971'], ['6124', '6224']], 'throwing': [['8723', '8807']]}

if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)
for action in actions:
    os.mkdir(os.path.join(OUTPUT_PATH, action))
os.mkdir(os.path.join(OUTPUT_PATH, 'others'))

action_times = []
for action in actions:
    action_times.extend(actions[action])
action_times.sort(key=lambda x: int(x[0]))

while success:
    if cv2.waitKey(10) == 27:
        break

    success, image = cap.read()
    index += 1

    if str(index) not in metas2:
        print(f'not saved for index: {index}')
        continue

    meta1, meta2 = metas[str(index)]
    id1, left1, top1, width1, height1 = map(int, meta1)
    id2, left2, top2, width2, height2 = map(int, meta2)

    image1 = image[top1: top1+height1, left1: left1+width1]
    image2 = image[top2: top2+height2, left2: left2+width2]

    for action_time in action_times:
        if index < int(action_time[0]):
            path1 = os.path.join(OUTPUT_PATH, f'others/{index}_{id1}.jpg')
            path2 = os.path.join(OUTPUT_PATH, f'others/{index}_{id2}.jpg')
            cv2.imwrite(path1, image1)
            cv2.imwrite(path2, image2)
            break

        if index < int(action_time[1]):
            action_name = ''
            for action in actions:
                if action_time in actions[action]:
                    action_name = action
                    break

            path1 = os.path.join(
                OUTPUT_PATH, f'{action_name}/{index}-{id1}.jpg')
            path2 = os.path.join(
                OUTPUT_PATH, f'{action_name}/{index}-{id2}.jpg')
            cv2.imwrite(path1, image1)
            cv2.imwrite(path2, image2)
            break

    print(f'saved image at {path1}, {path2}')

import os
import cv2
import shutil
import argparse

parser = argparse.ArgumentParser(description='XML Parser')
parser.add_argument('video', type=str, help='video path')
parser.add_argument('inference', type=str,
                    help='inference txt file (Yolov5 DeepSort)')
parser.add_argument('output', type=str, help='output path')
args = parser.parse_args()

# set id for unique video source
videoid = "1"
# get actions using xml_parser.py
actions = {'pushing': [['4382', '4418'], ['4483', '4506'], ['4546', '4592'], ['4727', '4753'], ['4792', '4820'], ['5620', '5662'], ['5734', '5765'], ['5784', '5830'], ['6201', '6251'], ['7094', '7195'], ['7729', '7770'], ['7966', '8006'], ['8541', '8579']], 'kicking': [['5359', '5393'], ['5555', '5600'], ['5842', '6032'], [
    '6058', '6161'], ['8034', '8072']], 'pulling': [['6250', '6411'], ['6662', '6731'], ['7222', '7269'], ['8093', '8153']], 'punching': [['7312', '7350'], ['7804', '7834'], ['8215', '8247']], 'falldown': [['5366', '5425'], ['5569', '5629'], ['5734', '5765'], ['7172', '7226'], ['7982', '8044'], ['8541', '8582']]}

if __name__ == '__main__':
    metas = {}
    with open(args.inference, 'r') as f:
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

    cap = cv2.VideoCapture(args.video)

    index = 0
    success = True

    if os.path.exists(args.output):
        shutil.rmtree(args.output)
    os.mkdir(args.output)
    for action in actions:
        os.mkdir(os.path.join(args.output, action))

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
            continue

        meta1, meta2 = metas[str(index)]
        id1, left1, top1, width1, height1 = map(int, meta1)
        id2, left2, top2, width2, height2 = map(int, meta2)

        image1 = image[top1: top1+height1, left1: left1+width1]
        image2 = image[top2: top2+height2, left2: left2+width2]

        for action_time in action_times:
            if index < int(action_time[0]):
                break

            if index < int(action_time[1]):
                action_name = ''
                for action in actions:
                    if action_time in actions[action]:
                        action_name = action
                        break

                path1 = os.path.join(
                    args.output, f'{action_name}/{videoid}-{index}-{id1}.jpg')
                path2 = os.path.join(
                    args.output, f'{action_name}/{videoid}-{index}-{id2}.jpg')
                cv2.imwrite(path1, image1)
                cv2.imwrite(path2, image2)
                print(f'saved image at {path1}, {path2}')
                break

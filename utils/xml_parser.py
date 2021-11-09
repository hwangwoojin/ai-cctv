import xml.etree.ElementTree as ET

FILENAME = '../videos/2.xml'

doc = ET.parse(FILENAME)

root = doc.getroot()

objects = root.findall('object')

for person in objects:
    objectname = person.findtext('objectname')

    position = person.find('position')
    keyframe = position.findtext('keyframe')
    keypoint_x = position.find('keypoint').findtext('x')
    keypoint_y = position.find('keypoint').findtext('y')

    actions = person.findall('action')
    action_list = {}
    for action in actions:
        action_name = action.findtext('actionname')
        action_list[action_name] = []

        action_frames = action.findall('frame')
        for action_frame in action_frames:
            start = action_frame.findtext('start')
            end = action_frame.findtext('end')
            action_list[action_name].append([start, end])

    print(f'objectname: {objectname}')
    print(f'keyframe: {keyframe}')
    print(f'keypoint_x: {keypoint_x}')
    print(f'keypoint_y: {keypoint_y}')
    print(f'action: \n{action_list}')
    print()

# ai-cctv

Real-time abnormal behavior classification using AI-based CCTV

## Getting Started

Clone the repository recursively.

```
$ git clone --recurse-submodules https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch.git
```

Install dependencies for `ai-cctv`.

```
pip install -r requirements.txt
pip install -r Yolov5_DeepSort_Pytorch/requirements.txt
pip install -r Yolov5_DeepSort_Pytorch/yolov5/requirements.txt
```

## Track the person and save as text file using DeepSort.

```
cd Yolov5_DeepSort_Pytorch
python3 track.py --source <Path for the video file> --yolo_weights yolov5n6.pt --classes 0 --save-txt
```

or using script file.

```
./scripts/track.sh
```

output text file will be generated at `Yolov5_DeepSort_Pytorch/inference/output`.

## Parse XML meta data

About XML Meta data format: [here](https://aihub.or.kr/aidata/139)

Parse XML file.

```
python3 utils/xml_parser.py <filename>
```

## Get only Images with abnormal action

use `image_getter.py` to get only images with abnormal action by using XML meta data.

```
python3 utils/image_getter.py <video name> Yolov5_DeepSort_Pytorch/inference/output/<result name> <output name>
```

with some restrictions,

1. at abnormal actions.
2. detect 2 people. (not 1 or 3)

## reference

[AI Hub](https://aihub.or.kr/)

[yolov5](https://github.com/ultralytics/yolov5)

[Yolov5_DeepSort_Pytorch](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)

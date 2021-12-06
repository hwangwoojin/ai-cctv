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

## reference

[yolov5](https://github.com/ultralytics/yolov5)

[Yolov5_DeepSort_Pytorch](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)

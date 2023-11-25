from ultralytics import YOLO
from os import path

curdir = path.dirname(__file__)

# sample global model
model = YOLO(path.join(curdir, 'data', 'model','yolov8n.pt'))

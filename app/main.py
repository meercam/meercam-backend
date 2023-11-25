import cv2
from dataclasses import dataclass
from ultralytics import YOLO
from flask import Flask, Response, request
import torch
from os import path
from PIL import Image
import io 
from controller import bot_controller, cctv_controller

app = Flask(__name__)
curdir = path.dirname(__file__)


app.register_blueprint(bot_b)

@app.route('/')
def webcam():
    source = request.args.get('source')
    if source == None:
        source = 0
    print("source: ", source)
    return Response(read_cam_data(source), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/add-cctv')
def add_cctv():
    # todo : cctv 데이터를 더합니다 
    return 

@app.route('/model-test')
def model_test():
    model = YOLO(path.join(curdir, 'data', 'model','od.pt'))
    results = model.predict(path.join(curdir, 'data', 'datasets'))

    sum_bbox = []
    for result in results:
        print(type(result))
        # Detection
        print(result.boxes.xyxy)   # box with xyxy format, (N, 4)
        print(result.boxes.xywh)   # box with xywh format, (N, 4)
        print(result.boxes.xyxyn)  # box with xyxy format but normalized, (N, 4)
        print(result.boxes.xywhn)  # box with xywh format but normalized, (N, 4)
        print(result.boxes.conf)   # confidence score, (N, 1)
        print(result.boxes.cls)    # cls, (N, 1)

        # Classification
        print(result.probs)     # cls prob, (num_class, )

        # names 및 boxes 데이터를 문자열로 변환하고 \n을 실제 줄바꿈으로 변환
        if hasattr(result, 'names'):
            formatted_names = str(result.names).replace('\\n', '\n')
            sum_bbox.append(formatted_names)

        formatted_boxes = str(result.boxes).replace('\\n', '\n')
        sum_bbox.append(formatted_boxes)


    for item in sum_bbox:
        print(item)
        print("-----------------------------------")  # 각 항목 사이에 구분선 추가


    
    return sum_bbox

@dataclass
class data:
    x: float
    y: float
    w: float
    w: float
    color: tuple
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
    def __iter__(self):
        return iter((self.x, self.y, self.w, self.h, self.color))
    
def read_cam_data(source):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        yield(None)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        bounding_boxes = [
            data(x=0, y=0, w=20, h=30, color=(0, 255, 0)),
            data(40, 80, 120, 60, (0, 0, 255)),
        ]
        for (x, y, w, h, color) in bounding_boxes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    yield(None)


app.register_blueprint(cctv_controller.bp, url_prefix='/api/v1/cctv')
app.register_blueprint(bot_controller.bp, url_prefix='/api/v1/bot')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

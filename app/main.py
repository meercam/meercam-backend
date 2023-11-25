import cv2
from ultralytics import YOLO
from flask import Flask, Response, request, send_file
from os import path
from PIL import Image
from controller import bot_controller, cctv_controller
from bounding_box import BoundingBox
from inference import inference
from flask_cors import CORS
import numbers

app = Flask(__name__)
CORS(app)
curdir = path.dirname(__file__)

@app.route('/')
def webcam():
    source = request.args.get('source')
    if source == None:
        source = 0
    if isinstance(source, str) and ( source.endswith('.jpg') or source.endswith('.png') or source.endswith('.jpeg')):
        return send_file(source)    
    return Response(read_cam_data(source), mimetype='multipart/x-mixed-replace; boundary=frame')


# sample global model
model = YOLO(path.join(curdir, 'data', 'model','yolov8n.pt'))

update_frame = True
last_left_top = [] 
last_right_bottom = []
last_color = []
last_label = []

captures = {} 
captures_ret = {}
captures_buf = {}

def read_cam_data(source): 
    global update_frame
    global last_left_top
    global last_right_bottom
    global last_color
    global last_label

    cap = cv2.VideoCapture(source)
    

    if not cap.isOpened():
        yield(None)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if update_frame:
            last_left_top = []
            last_right_bottom = []
            last_color = []
            last_label = []
            update_frame = False

            bboxes = inference(frame, model)
            for bbox in bboxes:
                last_left_top.append((bbox.x, bbox.y))
                last_right_bottom.append((bbox.x+bbox.w, bbox.y+bbox.h))
                last_color.append(bbox.color)
                last_label.append(bbox.label)

        if not update_frame:
            update_frame = True
        
        print(f"draw{ len(last_left_top)}")
        for left_top, right_bottom, color, label in zip(last_left_top, last_right_bottom, last_color, last_label):
            cv2.putText(frame, label, left_top, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.rectangle(frame, left_top, right_bottom, color, 2)
                
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    yield(None)


app.register_blueprint(cctv_controller.bp, url_prefix='/api/v1/cctv')
app.register_blueprint(bot_controller.bp, url_prefix='/api/v1/bot')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

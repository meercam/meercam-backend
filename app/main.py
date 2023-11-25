import cv2
from ultralytics import YOLO
from flask import Flask, Response, request
from os import path
from PIL import Image
from controller import bot_controller, cctv_controller
from bounding_box import BoundingBox
from inference import inference

app = Flask(__name__)
curdir = path.dirname(__file__)

@app.route('/')
def webcam():
    source = request.args.get('source')
    if source == None:
        source = 0
    print("source: ", source)
    return Response(read_cam_data(source), mimetype='multipart/x-mixed-replace; boundary=frame')


# sample global model
model = YOLO(path.join(curdir, 'data', 'model','od.pt'))

update_frame = True
last_left_top = [] 
last_right_bottom = []
last_color = []
last_label = []

captures = {} 
captures_ret = {}
captures_buf = {}

def get_capture(source):
    global captures 
    if source not in captures:
        captures[source] = cv2.VideoCapture(source)
    return captures[source] 

def release_capture(source):
    global captures
    if source in captures and captures[source] is not None:
        captures[source].release()
        captures[source] = None

def read_capture(cap):
    global captures_ret
    global captures_buf

    ret, frame = cap.read()
    if ret:
        captures_ret[cap] = ret
        captures_buf[cap] = frame
    else:
        captures_ret[cap] = False
        captures_buf[cap] = None
    return ret, frame

def read_cam_data(source):
    global update_frame
    global last_left_top
    global last_right_bottom
    global last_color

    cap = get_capture(source)
    

    if not cap.isOpened():
        print("Error: Could not open camera.")
        yield(None)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
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
        
        for left_top, right_bottom, color, label in zip(last_left_top, last_right_bottom, last_color, last_label):
            cv2.putText(frame, label, left_top, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.rectangle(frame, left_top, right_bottom, color, 2)
                
# draw images
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        # bboxes  = inference(buffer, model)
        # frame = buffer.tobytes()

        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    release_capture(source)
    yield(None)


app.register_blueprint(cctv_controller.bp, url_prefix='/api/v1/cctv')
app.register_blueprint(bot_controller.bp, url_prefix='/api/v1/bot')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import cv2
from flask import Blueprint, Response, request, abort
from inference import inference
from ai_model import model
import base64
bp = Blueprint('streaming', __name__)

update_frame = True
last_left_top = [] 
last_right_bottom = []
last_color = []
last_label = []
capture = {} 
last = {} 


@bp.route('/')
def webcam():
    source = request.args.get('source')
    # if source == None:
    #     source = 0
    is_static_file = isinstance(source, str) and (source.endswith('jpg') or source.endswith('png') or source.endswith('jpeg'))

    data = None
    if isinstance(source, str) and source.startswith('data:image'):
        b64 = source.split(',')[1]
        decoded = base64.decode(b64)
        data = read_cam_data(decoded, is_static_file)
    else:    
        data = read_cam_data(source, is_static_file)
    if data == None: return abort(404)
    return Response(data, mimetype='multipart/x-mixed-replace; boundary=frame')

def data_uri(b64):
    frame = base64.b64decode(b64)
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/', methods=['POST'])
def register(): 
    data = request.body.split(',')[1]
    return Response(data_uri(data), mimetype='multipart/x-mixed-replace; boundary=frame')



def get_capture(source):
    global capture
    if source not in capture:
        capture[source] = cv2.VideoCapture(source)
    return capture[source]


def get_data(source, is_static):
    global last
    cap = get_capture(source)
    if is_static:
        if source not in last:
            ret, frame = cap.read()
            if ret:
                last[source] = frame
        return last[source]
    else:
        ret, frame = cap.read() 
        return frame


def read_cam_data(source, is_static : bool): 
    global update_frame
    global last_left_top
    global last_right_bottom
    global last_color
    global last_label

    while True:
        frame = get_data(source, is_static)
        if frame is None: 
            abort(404)
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
                
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

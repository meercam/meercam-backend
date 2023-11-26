from flask import Flask, abort, jsonify, request, Response
from os import path
from flask_cors import CORS
from flask_socketio import SocketIO
from repository.cctv_repository import repository
from ai_model import model
from inference import inference
import cv2
import base64
from PIL import Image
import io
import numpy as np

from entity.cctv_entity import CCTVEntity

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('alert')
def cast_alert(msg):
    socketio.emit('alert_listener', msg)

def convert_image(data):
    # Base64 데이터를 이미지로 변환
    encoded_data = data.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def encode_frame(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='JPEG')
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img  

def video_stream(frame):
    # inference 
    list = inference(frame, model)
    socketio.emit('send_streaming', {'data': encode_frame(frame)})
    socketio.sleep(0)  # 너무 빠른 스트리밍 방지

@socketio.on('streaming')
def handle_streaming(data):
    frame = convert_image(data)
    video_stream(frame)

@app.route('/test/<msg>')
def trigger_alert(msg):
    socketio.emit('alert_listener', msg)
    return "sent"


@app.route('/', methods=['GET'])
def get_all_cctv():
    print("안찍혀")
    return jsonify([data.__dict__ for data in repository.find_all()])

@app.route('/<id>', methods=['GET'])
def get_cctv(id):
    return jsonify(repository.find_by_id(id).__dict__)

@app.route('/<id>/stream_url', methods=['GET'])
def get_stream_url(id):
    cctv = repository.find_by_id(id)
    if cctv is None: abort(404)
    return jsonify(cctv.get_connection_string())

@app.route('/', methods=['POST'])
def add_cctv():
    json_data = request.json
    cctv = CCTVEntity(
        repository.next_id(), 
        json_data['name'], 
        json_data['scheme'], 
        json_data['ip'], 
        json_data['port'], 
        json_data['username'], 
        json_data['password']
    )
    add_cctv(cctv)
    return "ok"

@app.route('/<id>', methods=['PUT'])
def modify_cctv(id):
    json_data = request.json 
    cctv = CCTVEntity(
        id, 
        json_data['name'], 
        json_data['scheme'], 
        json_data['ip'], 
        json_data['port'], 
        json_data['username'], 
        json_data['password']
    )
    return jsonify(modify_cctv(id).__dict__)

@app.route('/<id>', methods=['DELETE'])
def delete_cctv(id):
    return f"delete cctv {id}"

@app.route('/')
def webcam():
    source = request.args.get('source')
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

@app.route('/', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, abort, jsonify, request, Response
from os import path
from flask_cors import CORS
from flask_socketio import SocketIO
from repository import cctv_repository
from ai_model import model
from inference import inference
import cv2
import base64
from PIL import Image

capture = {}
update_frame = False

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('alert')
def cast_alert(msg):
    socketio.emit('alert_listener', msg)

@app.route('/api/v1/cctv', methods=['GET'])
def get_all_cctv():
    return jsonify([data.__dict__ for data in cctv_repository.find_all()])

@app.route('/api/v1/cctv/<id>', methods=['GET'])
def get_cctv(id):
    return jsonify(cctv_repository.find_by_id(id).__dict__)

@app.route('/api/v1/cctv/<id>/stream_url', methods=['GET'])
def get_stream_url(id):
    cctv = cctv_repository.find_by_id(id)
    if cctv is None: abort(404)
    return jsonify(cctv.get_connection_string())

@app.route('/api/v1/streaming')
def webcam():
    source = request.args.get('source')
    print(source)
    print(source)
    data = None 
    data = read_cam_data(source, False)
    if data == None: return abort(404)
    return Response(data, mimetype='multipart/x-mixed-replace; boundary=frame')

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
    while True:
        frame = get_data(source, is_static)
        if frame is None: 
            abort(404)
        if update_frame:
            update_frame = False
            bboxes = inference(frame, model)
            
            for bbox in bboxes:
                left_top = (bbox.x, bbox.y)
                right_bottom = (bbox.x + bbox.w, bbox.y + bbox.h)
                label = bbox.label
                color = bbox.color
                cv2.putText(frame, label, left_top, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.rectangle(frame, left_top, right_bottom, color, 2)
        if not update_frame:
            update_frame = True
                
        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

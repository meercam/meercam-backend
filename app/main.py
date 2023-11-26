from flask import Flask
from os import path
from controller import bot_controller, cctv_controller, streaming_controller
from flask_cors import CORS
from flask_socketio import SocketIO

from ai_model import model
from inference import inference
import cv2
import base64
from PIL import Image
import io
import numpy as np
from flask import Blueprint


last_left_top = []
last_right_bottom = []
last_color = []
last_label = []
update_frame = False


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('alert')
def cast_alert(msg):
    socketio.emit('alert_listener', msg)

# app.register_blueprint(websocket_controller.bp, url_prefix='/api/v1/websocket')
app.register_blueprint(streaming_controller.bp, url_prefix='/api/v1/streaming')
app.register_blueprint(cctv_controller.bp, url_prefix='/api/v1/cctv')
app.register_blueprint(bot_controller.bp, url_prefix='/api/v1/bot')



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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

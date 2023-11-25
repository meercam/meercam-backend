from main import socketio
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
    bboxes = inference(frame, model)

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
    socketio.emit('send_streaming', {'data': encode_frame(frame)})
    socketio.sleep(0)  # 너무 빠른 스트리밍 방지

@socketio.on('streaming')
def handle_streaming(data):
    frame = convert_image(data)
    video_stream(frame)

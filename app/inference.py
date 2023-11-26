from bounding_box import BoundingBox
from ultralytics.engine.results import Boxes, Results
import numpy as np
import math

def inference(img, model): 
    colors = [
        (0x00, 0x00, 0xff),
        (0x00, 0x80, 0xff), 
        (0x00, 0xff, 0xff),
        (0x00, 0xff, 0x80), 
        (0x00, 0xff, 0x00),
        (0x80, 0xff, 0x00),
        (0xff, 0x0f, 0x00),
        (0xff, 0x80, 0x00),
        (0xff, 0x00, 0x00),
        (0xff, 0x00, 0x80),
        (0xff, 0x00, 0xff),
        (0x80, 0x00, 0xff),
    ]
    results = model.predict(img)
    ret = [] 
    for r in results:
        if isinstance(r, Results):
            if hasattr(r, 'boxes') and isinstance(r.boxes, Boxes):
                for box in r.boxes: 
                    confidence = math.ceil((box.conf[0]*100))/100
                    if confidence >= 0.45: 
                        x_center, y_center, width, height = box.xywh[0].tolist()
                        x = np.round((x_center - width / 2)).astype("int")
                        y = np.round((y_center - height / 2)).astype("int")
                        w = np.round(width).astype("int")
                        h = np.round(height).astype("int")
                        ret.append(BoundingBox(x, y, w, h, colors[int(box.cls[0]) % 12], model.names[int(box.cls[0])]))
    return ret


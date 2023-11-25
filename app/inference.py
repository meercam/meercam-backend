from bounding_box import BoundingBox
from ultralytics.engine.results import Boxes, Results

import numpy as np

"""
model.predict()

Perform prediction using the YOLO model.
Args:
    source (str | int | PIL | np.ndarray): The source of the image to make predictions on.
        Accepts all source types accepted by the YOLO model.
    stream (bool): Whether to stream the predictions or not. Defaults to False.
    predictor (BasePredictor): Customized predictor.
    **kwargs : Additional keyword arguments passed to the predictor.

"""
def inference(img, model): 
    results = model.predict(img)
    # print("xywh", results[0].boxes.xywh)
    ret = [] 
    for r in results:
        if isinstance(r, Results):
            if hasattr(r, 'boxes') and isinstance(r.boxes, Boxes):
                print("yeap")
                if hasattr(r.boxes, 'xywh') and len(r.boxes.xywh) > 0:
                    print(type(r.boxes.xywh))
                    x = np.round( r.boxes.xywh[0][0].item() ).astype("int")
                    y = np.round( r.boxes.xywh[0][1].item() ).astype("int")
                    w = np.round( r.boxes.xywh[0][2].item() ).astype("int")
                    h = np.round( r.boxes.xywh[0][3].item() ).astype("int")
                    ret.append(BoundingBox(x, y, w, h, (0, 255, 0), model.names[int(r.boxes.cls[0])] ))
    return ret
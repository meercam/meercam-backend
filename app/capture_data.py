from time import time
class CaptureData:
    def __init__(self, cv_result: bool, buf, infer: bool):
        self.cv_result = cv_result
        self.buf = buf 
        self.infer = infer 
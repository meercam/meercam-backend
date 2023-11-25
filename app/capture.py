import cv2

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
    capture = get_capture(cap)

    if not capture.isOpened():
        print("Error: Could not open camera.")
        return False, None
    ret, frame = cap.read()
    
    if ret:
        captures_ret[cap] = ret
        captures_buf[cap] = frame
    else:
        captures_ret[cap] = False
        captures_buf[cap] = None
    return ret, frame

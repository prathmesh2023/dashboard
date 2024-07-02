from django.shortcuts import render

# Create your views here.
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

from datetime import datetime
import pandas as pd
import winsound



def index(request):
    
    return render(request, "index.html")

def cctv(request):

    return render(request, "cctv.html")

def action_chart(request):
    return render(request, "action_chart.html")

def object_detection(request):
    return render(request, "object_detection.html")
    

static_back = None
motion_list = [None, None]
time = []
df = pd.DataFrame(columns=["Start", "End"])

class VideoCamera(object):
    def __init__(self):
        
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        
        global static_back , motion_list 
        
        success, image = self.video.read()
        
        if not success:
        # Log the error or handle it as needed
            print("Failed to capture frame from the camera.")
            return b''
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if static_back is None:
            static_back = gray
            return b''
        
        
        diff_frame = cv2.absdiff(static_back, gray)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion = 0 
        
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            motion = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

        motion_list.append(motion)
        motion_list = motion_list[-2:]
        
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now())
            print("detected")  # Beep when motion is detected
            winsound.Beep(1000, 1000)  # 
            

        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now())
            
       
    


        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

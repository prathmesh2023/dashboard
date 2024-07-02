from django.shortcuts import render,HttpResponse

# Create your views here.
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

from datetime import datetime
import pandas as pd
import winsound


import cv2
import numpy as np
from .simple_facerec import SimpleFacerec
import cvlib as cv
from cvlib.object_detection import draw_bbox
from datetime import datetime

import requests as req

from django.templatetags.static import static


def index(request):
    
    return render(request, "index.html")

def cctv(request):

    return render(request, "cctv.html")

def action_chart(request):
    return render(request, "action_chart.html")

def obj_detection(request):
    return render(request, "object_detection.html")

def obj_tracking(request):
    return render(request, "object_tracking.html")

def ai_bot(request):
    return render(request, "ai_bot.html")

def obj_testing(request):
    return HttpResponse("test")
    




def create_alert(alert_type):
    host = "http://localhost:8000/api/"
    parameters = {
        "alert_type": alert_type,
        "camera_id": 1
    }
    resp = req.post(host + "camera_alerts", json=parameters)
    print(resp.status_code)
    if resp.status_code == 201:
        return True
    else:
        return False

class VideoCamera(object):
    
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        # url = static('static/face/images/')
        self.last_mean = 0
        self.detected_motion = False
        self.detected_person = False
        self.suspicious_activity = False
        self.detected_health = False
        self.detected_face = False
        self.detected_bad = False
        self.sfr = SimpleFacerec()
        # self.sfr.load_encoding_images(url) 
        self.motion_detection = True
        self.object_detection = True
        self.animal_detection = True
        self.person_detection = True
        self.face_detection = True
        self.bad_activity_detection = True
        self.health_activity_detection = True
        self.camera_id = 1
        self.host = "http://localhost:8000/api/"
        
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = np.abs(np.mean(gray) - self.last_mean)
        self.last_mean = np.mean(gray)

        # if result > 1 and self.motion_detection:  # Assuming motion_detection is a global variable
        #     create_alert(2)
        
        if result > 1 and self.motion_detection:
            print("Motion detected!")
            # print("Started recording.")
            detected_motion = True
            # api code to get previous alert time
            # if not alerted then create new alert
            res = req.get(self.host+"camera_alert_flag/alert_type_id=2&camera_id="+str(self.camera_id)).json()
            if res['alert_flag']==True:
                # print("flag"res)
                create_alert(2)
        else:
            detected_motion = False
        
        if self.detected_motion or self.object_detection:
            bbox, label, conf = cv.detect_common_objects(frame)
            output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)
            frame = output_image
            if "person" in label:
                self.detected_person = True
        
        if self.person_detection and self.face_detection:
            if self.detected_person:
                face_locations, face_names = self.sfr.detect_known_faces(frame)
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    if name == "unknown":
                        self.suspicious_activity = True
                        self.detected_face = False
                    else:
                        self.detected_face = True
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
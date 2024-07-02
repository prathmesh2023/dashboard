import cv2 
import numpy as np
import requests as req
import threading
from django.http import StreamingHttpResponse
from django.shortcuts import render
from cvlib.object_detection import draw_bbox
from .facerec import SimpleFacerec  # Ensure this module exists
import cvlib as cv

# Function to create alerts
def create_alert(alert_type):
    host = "http://localhost:8000/api/"
    parameters = {
        "alert_type": alert_type,
        "camera_id": 1
    }
    resp = req.post(host + "camera_alerts", json=parameters)
    print(resp.status_code)
    return resp.status_code == 201

# VideoCamera class for capturing and processing video frames
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.last_mean = 0
        self.detected_motion = False
        self.detected_person = False
        self.sfr = SimpleFacerec()
        # self.sfr.load_encoding_images()  # Path to face images
        self.motion_detection = True
        self.object_detection = True
        self.person_detection = True
        self.face_detection = True
        self.camera_id = 1
        self.host = "http://localhost:8000/api/"
        start_all_surveillance()
        
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = np.abs(np.mean(gray) - self.last_mean)
        self.last_mean = np.mean(gray)

        if result > 1 and self.motion_detection:
            print("Motion detected!")
            self.detected_motion = True
            res = req.get(f"{self.host}camera_alert_flag/alert_type_id=2&camera_id={self.camera_id}").json()
            if res['alert_flag']:
                create_alert(2)
        else:
            self.detected_motion = False
        
        if self.detected_motion or self.object_detection:
            bbox, label, conf = cv.detect_common_objects(frame)
            frame = draw_bbox(frame, bbox, label, conf, write_conf=True)
            if "person" in label:
                self.detected_person = True
        
        if self.person_detection and self.face_detection and self.detected_person:
            face_locations, face_names = self.sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

# Generator function for video feed
def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# View to handle the video feed
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

# Function to start surveillance for a specific camera link
def start_surveillance(cam_link, win_name):
    last_mean = 0
    motion_detection = True
    object_detection = True
    person_detection = True
    face_detection = True
    detected_person = False
    detected_motion = False

    cap = cv2.VideoCapture(cam_link)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = np.abs(np.mean(gray) - last_mean)
        last_mean = np.mean(gray)
        
        if 1 < result < 100:
            detected_motion = True
            if motion_detection:
                res = req.get(f"{host}camera_alert_flag/alert_type_id=2&camera_id={camera_id}").json()
                if res['alert_flag']:
                    create_alert(2)
        else:
            detected_motion = False

        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)

        if "person" in label:
            detected_person = True
            res = req.get(f"{host}camera_alert_flag/alert_type_id=4&camera_id={camera_id}").json()
            if res['alert_flag']:
                create_alert(4)

        cv2.imshow(win_name, output_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to start all surveillance threads
def start_all_surveillance():
    available_cameras = ["http://103.151.177.124:91/mjpg/video.mjpg"]
    window_name = ['Feed1']

    threads = []
    for i, camera in enumerate(available_cameras):
        thread = threading.Thread(target=start_surveillance, args=(camera, window_name[i]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Start surveillance when the server starts
start_all_surveillance()

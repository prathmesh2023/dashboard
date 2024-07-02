# views.py

import cv2
import numpy as np
import requests as req
import threading
from django.http import StreamingHttpResponse
from cvlib.object_detection import draw_bbox
import cvlib as cv

host = "http://localhost:8000/api/"  # Replace with your API endpoint
camera_id = 1

# Define cascade classifier for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Function to check alert flag for a specific alert type
def check_alert_flag(alert_type):
    try:
        res = req.get(f"{host}camera_alert_flag/alert_type_id={alert_type}&camera_id={camera_id}")
        if res.status_code == 200:
            return res.json().get("alert_flag", False)
        else:
            print(f"Error checking alert flag: {res.status_code}")
            return False
    except req.RequestException as e:
        print(f"Request failed: {e}")
        return False

# Function to create alerts
def create_alert(alert_type):
    parameters = {
        "alert_type": alert_type,
        "camera_id": camera_id
    }

    # Check alert flag
    flag = check_alert_flag(alert_type)

    # If flag is true, make a post request to create an alert
    if flag:
        try:
            resp = req.post(host + "camera_alerts", json=parameters)
            print(resp.status_code)
            if resp.status_code == 201:
                print("Alert posted successfully")
            else:
                print("Failed to post alert")
        except req.RequestException as e:
            print(f"Request failed: {e}")
    else:
        print("Alert flag is False, no alert will be posted")

# Function to detect motion
def detect_motion(fr):
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    result = np.abs(np.mean(gray))
    return result

# Function to start surveillance process
def start_surveillance(cam_link):
    last_mean = 0

    # Features list and settings
    # Set to True if the feature is ON, False if it's OFF
    motion_detection = True
    object_detection = True
    person_detection = True
    face_detection = True

    detected_person = False

    cap = cv2.VideoCapture(cam_link)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Motion detection
        result = detect_motion(frame)
        
        if 1 < result < 100:
            print("Motion detected!")
            detected_motion = True
            if motion_detection:
                if check_alert_flag(1):  # Check alert flag for motion detection
                    create_alert(1)  # Create alert for motion detection
        else:
            detected_motion = False
        
        # Object detection
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)

        if "person" in label:
            detected_person = True
        
        # Encode frame for streaming
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()

# Django view to serve the video feed
def video_feed(request):
    available_cameras = ["http://103.151.177.124:91/mjpg/video.mjpg"]  # Replace with your camera URLs
    
    # Use streaming HTTP response for continuous video streaming
    return StreamingHttpResponse(start_surveillance(available_cameras[0]), content_type='multipart/x-mixed-replace; boundary=frame')

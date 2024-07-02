from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import threading
import numpy as np
from .simple_facerec import SimpleFacerec
import datetime
import time as t
import requests as req
from cvlib.object_detection import draw_bbox
import cvlib as cv  # Import cvlib

import os 



# Initialize face recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Set API host and camera ID
host = "http://localhost/php_api/api.php?"


module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'action_recognition_kinetics_all.txt')
# Load class labels for human activity recognition
CLASSES = open(file_path).read().strip().split("\n")
SAMPLE_DURATION = 16
SAMPLE_SIZE = 112
custom_labels = ["smoking", "smoking hookah", "drinking", "drinking beer", "drinking shots", "tasting beer"]

# Load the human activity recognition model
print("[INFO] Loading the human activity recognition model...")

module_dir2 = os.path.dirname(__file__)  # get current directory
file_path2 = os.path.join(module_dir2, 'resnet-34_kinetics.onnx')
net = cv2.dnn.readNet(file_path2)

# Load face detection model
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# List of animals for detection
animals = ["bird", "cat", "dog", "horse", "sheep", "cow"]

# Initialize detection flags
motion_detection = False
object_detection = False
animal_detection = False
person_detection = False
child_detection = False
face_detection = False
smoking_detection = False
drinking_detection = False
health_activity_detection = False
fire_detection = False
increase_speed = False
terminate = False


camera_id = 0

def get_file_name():
    """Generate a unique file name based on the current date and time."""
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return date

def create_alert(alert_type):
    """Send a request to create an alert of the specified type."""
    res = req.get(host + "action=create_alert&alert_type_id=" + str(alert_type) + "&camera_id=" + str(camera_id)).json()
    return res['status'] == "success"

def detect_fire(fr):
    """Detect fire in the given frame."""
    fr = cv2.resize(fr, (960, 540))
    blur = cv2.GaussianBlur(fr, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower = np.array([18, 50, 50], dtype="uint8")
    upper = np.array([35, 255, 255], dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
    no_red = cv2.countNonZero(mask)
    return no_red

def detect_motion(fr):
    """Detect motion in the given frame."""
    last_mean = 0
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    result = np.abs(np.mean(gray) - last_mean)
    last_mean = np.mean(gray)
    return result

def detect_objects(fr):
    """Detect common objects in the given frame."""
    new_width = int(fr.shape[1] * 0.8)
    new_height = int(fr.shape[0] * 0.8)
    resized_image = cv2.resize(fr, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    bbox, label, conf = cv.detect_common_objects(resized_image, model='yolov4-tiny')
    output_image = draw_bbox(resized_image, bbox, label, conf, write_conf=True)
    return output_image, bbox, label, conf

def check_features():
    global camera_id
    """Periodically check which detection features are enabled."""
    while True:
        global terminate
        if terminate:
            break
        global motion_detection, object_detection, animal_detection, person_detection, child_detection
        global face_detection, smoking_detection, drinking_detection, health_activity_detection, fire_detection

        res = req.get(host + "action=get_features&camera_id=" + str(camera_id)).json()
        print("cf",host + "action=get_features&camera_id=" + str(camera_id))
        if res['feature_list'] == "success":
            for feature in res['feature_list']:
                if feature["alert_type_id"] == 1:
                    motion_detection = True
                elif feature["alert_type_id"] == 2:
                    person_detection = True
                    face_detection = True
                elif feature["alert_type_id"] == 5:
                    animal_detection = True
                elif feature["alert_type_id"] == 6:
                    fire_detection = True
                elif feature["alert_type_id"] in [7, 8]:
                    smoking_detection = True
                    drinking_detection = True
        else:
            motion_detection = False
            person_detection = False
            face_detection = True
        t.sleep(3)  # Check for features ON/OFF every 3 seconds

def generate_frames(cam_link):
    global camera_id
    """Generate frames from the video feed."""

    global terminate
    last_mean = 0

    # Start a thread to check features
   
    check = threading.Thread(target=check_features)
    check.start()

    detected_motion = detected_person = detected_unknown = detected_suspect = False
    detected_fire = detected_animal = detected_face = detected_child = False
    detected_smoking = detected_drinking = False

    bbox_out = []
    label_out = []
    conf_out = []
    face_names = []
    face_locations = []
    original_frames = []
    compressed_frames = []
    activity_label = ""

    cap = cv2.VideoCapture(cam_link)
    fps = cap.get(cv2.CAP_PROP_FPS)
    writer = None
    skip_count = 3 if fps >= 30 else 2 if 21 <= fps < 30 else 1 if 11 < fps <= 20 else 0
    skip_frames = skip_count
    frame_count = 0
    frame_number = 0

    while True:
        # camera_id=1
        
        
        ret, frame = cap.read()
        if not ret:
            terminate = True
            break
        frame_number += 1

        # Skip frames based on the condition (skip_count)
        if skip_frames == 0:
            result = detect_motion(frame)
            if 1 < result and frame_number > 2:
                detected_motion = True
                if motion_detection:
                    res = req.get(host + "action=get_last_detected&alert_type_id=1&camera_id=" + str(camera_id)).json()
                    if res['status'] != 1:
                        create_alert(1)
            else:
                detected_motion = False

            frame, bbox_out, label_out, conf_out = detect_objects(frame)

            if "person" in label_out:
                detected_person = True
                res = req.get(host + "action=get_last_detected&alert_type_id=2&camera_id=" + str(camera_id)).json()
                if res['status'] != 1:
                    create_alert(2)
            for name in label_out:
                if name in animals:
                    detected_animal = True
            if animal_detection and detected_animal:
                res = req.get(host + "action=get_last_detected&alert_type_id=5&camera_id=" + str(camera_id)).json()
                if res['status'] != 1:
                    create_alert(5)
            if person_detection and face_detection:
                if detected_person:
                    face_locations, face_names = sfr.detect_known_faces(frame)
                    for face_loc, name in zip(face_locations, face_names):
                        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
                        if name.lower() == "unknown":
                            suspicious_activity = True
                            detected_face = False
                            res = req.get(host + "action=get_last_detected&alert_type_id=3&camera_id=" + str(camera_id)).json()
                            if res['status'] != 1:
                                create_alert(3)
                        elif "suspect" in name.lower():
                            suspicious_activity = True
                            detected_face = True
                            res = req.get(host + "action=get_last_detected&alert_type_id=4&camera_id=" + str(camera_id)).json()
                            if res['status'] != 1:
                                create_alert(4)
                        else:
                            detected_face = True
                            res = req.get(host + "action=get_last_detected&alert_type_id=2&camera_id=" + str(camera_id)).json()
                            if res['status'] != 1:
                                create_alert(2)

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            if smoking_detection or drinking_detection:
                frame_count += 1
                if frame_count <= 15:
                    original_frames.append(frame)
                    resized_frame = imutils.resize(frame, width=400)
                    compressed_frames.append(resized_frame)
                if frame_count >= 16:
                    frame_count = 0
                    blob = cv2.dnn.blobFromImages(compressed_frames, 1.0, (SAMPLE_SIZE, SAMPLE_SIZE),
                                                  (114.7748, 107.7354, 99.4750), swapRB=True, crop=True)
                    blob = np.transpose(blob, (1, 0, 2, 3))
                    blob = np.expand_dims(blob, axis=0)
                    net.setInput(blob)
                    outputs = net.forward()
                    activity_label = CLASSES[np.argmax(outputs)]
                    original_frames = []
                    compressed_frames = []

                if activity_label in custom_labels:
                    if "smoking" in activity_label.lower():
                        res = req.get(host + "action=get_last_detected&alert_type_id=8&camera_id=" + str(camera_id)).json()
                        if res['status'] != 1:
                            create_alert(8)
                    else:
                        res = req.get(host + "action=get_last_detected&alert_type_id=9&camera_id=" + str(camera_id)).json()
                        if res['status'] != 1:
                            create_alert(9)
                    cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), -1)
                    cv2.putText(frame, activity_label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            skip_frames = skip_count
        else:
            skip_frames -= 1

    cap.release()
    cv2.destroyAllWindows()

def video_feed(request,id):
    """Video feed view."""
    global camera_id
    from app1.models import camera
    obj= camera.objects.filter(id=id).first()
    local_camera_id = obj.id
    camera_id = local_camera_id
    ip = obj.ip_address
    rances = "0","1","2"
    if ip in rances:
        ip = int(ip)
    
    
    
    return StreamingHttpResponse(generate_frames(ip),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


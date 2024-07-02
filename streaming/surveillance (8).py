import cv2  # Always load this library
import numpy as np
import cvlib as cv
import time as t
from cvlib.object_detection import draw_bbox
import requests as req
import threading
from simple_facerec import SimpleFacerec
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
host = "http://localhost/php_api/api.php?"
camera_id = 1

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

animals = ["bird","cat","dog","horse","sheep","cow"]

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


def create_alert(alert_type):  # function to create alerts

    res = req.get(host + "action=create_alert&alert_type_id="+str(alert_type)+"&camera_id=" + str(camera_id)).json()
    if res['status'] == "success":
        return True
    else:
        return False


def detect_fire(fr):
    Fire_Reported = 0

    fr = cv2.resize(fr, (960, 540))

    blur = cv2.GaussianBlur(fr, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)

    # output = cv2.bitwise_and(fr, hsv, mask=mask)

    no_red = cv2.countNonZero(mask)
    return no_red


def detect_motion(fr):  # motion detection function
    last_mean = 0
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    result = np.abs(np.mean(gray) - last_mean)
    print(result)
    last_mean = np.mean(gray)
    return result


def detect_objects(fr):  # object detection n tracking
    # Reduce image size by 20% i.e. * 0.8 (experiment with different scales)
    new_width = int(fr.shape[1] * 0.8)
    new_height = int(fr.shape[0] * 0.8)
    resized_image = cv2.resize(fr, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    bbox, label, conf = cv.detect_common_objects(resized_image, model='yolov4-tiny')
    # bbox, label, conf = cv.detect_gender(frame)
    output_image = draw_bbox(resized_image, bbox, label, conf, write_conf=True)
    return output_image, label


def check_features():
    while True:
        global motion_detection,object_detection,animal_detection,person_detection,child_detection
        global face_detection,smoking_detection,drinking_detection,health_activity_detection,fire_detection
        # features list and settings
        # True means feature is ON, False = OFF
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
        res = req.get(host + "action=get_features&camera_id=" + str(camera_id)).json()
        print(res["feature_list"])
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
                elif feature["alert_type_id"] == 7 or feature["alert_type_id"] == 8:
                    smoking_detection = True
                    drinking_detection = True
        else:
            person_detection = True
            face_detection = True
        t.sleep(5)


def start_surveillance(cam_link, win_name):  # start thread to surveillance process
    import cv2  # Always load this library
    # import numpy as np
    # import cvlib as cv
    # from cvlib.object_detection import draw_bbox

    last_mean = 0

    check_features()  # looping the function every 5 seconds to check for Turned ON features
    check = threading.Thread(target=check_features)
    check.start()
    detected_person = False
    detected_unknown = False
    detected_suspect = False
    detected_fire = False
    detected_animal = False
    detected_face = False
    detected_child = False
    detected_smoking = False
    detected_drinking = False

    cap = cv2.VideoCapture(cam_link)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        # Fire detection start
        # fire_score = detect_fire(frame)
        #
        # if int(fire_score) > 2000:
        #     detected_fire = True
        #     res = req.get(host + "action=get_last_detected&alert_type_id=6&camera_id=" + str(camera_id)).json()
        #     if res['status'] != 1:
        #         create_alert(6)
        # else:
        #     detected_fire = False

        # Fire detection end

        # motion detection code
        result = detect_motion(frame)
        # motion_res = detect_motion(frame)
        if 1 < result and frame_count > 5:
            print("Motion detected!")
            detected_motion = True
            if motion_detection:
                # api code to get previous alert time
                # if not alerted then create new alert
                res = req.get(host + "action=get_last_detected&alert_type_id=1&camera_id=" + str(camera_id)).json()
                if res['status'] != 1:
                    create_alert(1)
        else:
            detected_motion = False
        # Motion detection end
        # Object detection start
        # global detected_person

        frame, label = detect_objects(frame)

        if "person" in label:
            detected_person = True
            res = req.get(host + "action=get_last_detected&alert_type_id=2&camera_id=" + str(camera_id)).json()
            if res['status'] != 1:
                create_alert(2)
        for name in label:
            if name in animals:
                detected_animal = True
        if animal_detection and detected_animal:
            res = req.get(host + "action=get_last_detected&alert_type_id=5&camera_id=" + str(camera_id)).json()
            if res['status'] != 1:
                create_alert(5)
        if person_detection and face_detection:
            pass
            # Encode faces from a folder
            # if detected_person:
            #     face_locations, face_names = sfr.detect_known_faces(frame)
            #     for face_loc, name in zip(face_locations, face_names):
            #         y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            #         cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            #         print(name)
            #         if name == "unknown":
            #             suspicious_activity = True
            #             detected_face = False
            #             res = req.get(host + "action=get_last_detected&alert_type_id=3&camera_id=" + str(camera_id)).json()
            #             if res['status'] != 1:
            #                 create_alert(3)
            #         if "suspect" in name.lower():
            #             suspicious_activity = True
            #             detected_face = False
            #             res = req.get(host + "action=get_last_detected&alert_type_id=4&camera_id=" + str(camera_id)).json()
            #             if res['status'] != 1:
            #                 create_alert(4)
            #         else:
            #             detected_face = True
            #             res = req.get(host + "action=get_last_detected&alert_type_id=2&camera_id=" + str(camera_id)).json()
            #             if res['status'] != 1:
            #                 create_alert(2)
        print("Motion " + str(detected_motion))
        print("Person " + str(detected_person))
        print("Fire " + str(detected_fire))
        # cv2.imshow(win_name, output_image)
        cv2.imshow(win_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Get all cameras registered for the area

available_cameras = ["1.mp4"]  # , "http://103.151.177.124:91/mjpg/video.mjpg"]
# available_cameras = ["Wildlife.wmv"]  # , "http://103.151.177.124:91/mjpg/video.mjpg"]
started_thread = [1]
window_name = ['Feed1', 'Feed2']
# for i in range(2):
#     vid = cv2.VideoCapture("http://217.91.112.157/mjpg/video.mjpg")
#     if vid.isOpened():
#         available_cameras.append("http://217.91.112.157/mjpg/video.mjpg")
#         started_thread.append(i)
#         vid.release()
j=0
for camera in available_cameras:
    started_thread[j] = threading.Thread(target=start_surveillance, args=(camera, window_name[j]))
    started_thread[j].start()
    j += 1

print(available_cameras)
print(started_thread)


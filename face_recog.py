#Last modified: 2022-08-07
import os
import cv2
import face_recognition
import numpy as np
import winsound as sd
import mysql.connector as mariadb
import logging
import logging.handlers
mariadb_connect = mariadb.connect(host='127.0.0.1', port=3306,
                                  user='root', password='tom',
                                  database='seokwon')
logging.basicConfig(filename="log.txt", filemode="w", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def beepsound():
    frequency = 800
    duration = 1000
    times = 0
    while (times < 2):
        sd.Beep(frequency, duration)
        times += 1

def recognize():
    time = 0
    vid_cap = cv2.VideoCapture(0)
    recognized_names = []
    recognized_encodings = []

    directory_name = 'knowns'
    files = os.listdir(directory_name)

    for file_name in files:
        name, ext = os.path.splitext(file_name)
        if ext == '.jpg':
            recognized_names.append(name)
            path  = os.path.join(directory_name, file_name)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)[0]
            recognized_encodings.append(encoding)

    current_frame = True
    names = []
    locations = []
    encodings = []

    while True:
        ret, frame = vid_cap.read()
        if current_frame:
            resize_frame = cv2.resize(frame,None,fx=0.25,fy=0.25)
            bgr_to_rgb = resize_frame[:, :, ::-1]
            locations = face_recognition.face_locations(bgr_to_rgb)
            encodings = face_recognition.face_encodings(bgr_to_rgb, locations)
            names = []
            for face_encoding in encodings:
                compare_faces = face_recognition.compare_faces(recognized_encodings, face_encoding)
                name = "unknown"
                distance = face_recognition.face_distance(recognized_encodings, face_encoding)
                index = np.argmin(distance)
                if compare_faces[index]:
                    name = recognized_names[index]
                    logger = logging.getLogger(name)
                    logger.info("Found %s from camera", name)

                else:
                    beepsound()
                    logger = logging.getLogger(name)
                    logger.info("Found %s from camera", name)

                names.append(name)
        current_frame = not current_frame

        for (top, right, bottom, left), name in zip(locations, names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid_cap.release()
    cv2.destroyAllWindows()

import json
import threading
import time

import cv2
import os

import requests
from lib.data import Data, db



class Camera():
    def __init__(self, c_id, c_posi, class_id, c_time, camera_url, recive_url):
        self.c_id = c_id
        self.c_posi = c_posi
        self.class_id = class_id
        self.c_time = c_time
        self.camera_url = camera_url
        self.recive_url = recive_url
        self.cap = cv2.VideoCapture(self.camera_url)

        # if not self.cap.isOpened():
        #     print('摄像头初始化失败，请关闭摄像头后重新打开!')

    def save_img(self):
        # ret, frame = self.cap.read()
        ret, frame = cv2.VideoCapture(self.camera_url).read()
        if ret:
            cv2.imwrite(f"./images/cache/{self.c_id}.jpg", frame)
            return True
        else:
            return False


    def detect_img(self):
        upload_url = "http://127.0.0.1:5000/detect"
        # file = {"file": open(f"images/{self.c_id}.jpg", "rb"), "c_id": self.c_id, "c_posi": self.c_posi, "class_id": self.class_id, "c_time": self.c_time}
        file = {"file": open(f"images/cache/{self.c_id}.jpg", "rb")}
        data = {"c_id": self.c_id, "c_posi": self.c_posi, "class_id": self.class_id, "c_time": self.c_time, "recive_url": self.recive_url}
        upload_res = requests.post(url=upload_url, files=file, data=data)
        # print(f"{i}, {upload_res.content}")
        res = upload_res.content.decode('UTF-8')
        # print(json.loads(res))
        res = "fail"
        if upload_res.status_code == 200:
            res = "success"
        return res


class inferThread(threading.Thread):
    def __init__(self, cv_camera):
        threading.Thread.__init__(self)
        self.cv_camera = cv_camera

    def run(self):
        while 1:
            if Data.query.filter_by(id=1).first().camera_url == 'True' and self.cv_camera.save_img():
                self.cv_camera.detect_img()
            else:
                break

if __name__ == '__main__':
    threads = []

    data = Data.query.all()

    for i, e in enumerate(data[1:]):
        threads.append(inferThread(Camera(e.camera_url, f'img-{e.id}.jpg'), i))

    for e in threads:
        e.start()





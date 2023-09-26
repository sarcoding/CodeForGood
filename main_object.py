import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker
import websockets
import asyncio
import json
import time
from datetime import datetime
import pytz
import pickle
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8765  # The port used by the server

class ObjectTracker:
    def __init__(self, camera_name, video_path, cy1, cy2, offset):
        self.camera_name = camera_name
        self.video_path = video_path
        self.cy1 = cy1
        self.cy2 = cy2
        self.offset = offset
        self.model = YOLO('yolov8s.pt')
        self.tracker = Tracker()
        self.waiting_car = set()
        self.current_signal = 'red'
        self.red_thic = -1
        self.green_thic = 2
        self.penalty = []
        






    async def object_tracking(self):
        start_time = time.time()
        cap = cv2.VideoCapture(self.video_path)
        my_file = open("coco.txt", "r")
        data = my_file.read()
        class_list = data.split("\n")
        count = 0

        while True:
            current_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            if count % 3 != 0:
                continue
            frame = cv2.resize(frame, (1020, 500))

            results = self.model.predict(frame)
            a = results[0].boxes.data
            px = pd.DataFrame(a).astype("float")
            obj_list = []

            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                if 'car' in c:
                    obj_list.append([x1, y1, x2, y2])

            bbox_id = self.tracker.update(obj_list)
            for bbox in bbox_id:
                x3, y3, x4, y4, obj_id = bbox
                cx = int((x3 + x4) / 2)
                cy = int((y3 + y4) / 2)

                if self.cy1 - self.offset < cy < self.cy2 + self.offset and cx > 530:
                    self.waiting_car.add(obj_id)
                elif cy > self.cy2 + self.offset and cx > 530:
                    if obj_id in self.waiting_car:
                        if self.current_signal=="red":
                            self.penalty.append(obj_id)
                            _, penalty_frame = cap.read()
                            penalty_frame = cv2.resize(penalty_frame, (1020, 500))
                            cv2.line(penalty_frame, (143, self.cy2), (922, self.cy2), (0, 0, 255), 1)
                            cv2.putText(penalty_frame, str(obj_id), (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                            cv2.rectangle(penalty_frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                            cv2.putText(penalty_frame, datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y:- %H:%M:%S"), (60, 440), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                            cv2.imwrite(f"./cache/{obj_id}_redCross.jpg", penalty_frame)
                        self.waiting_car.remove(obj_id)

                if self.cy1 - self.offset <= cy <= self.cy2 + self.offset:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.putText(frame, str(obj_id), (x3, y3 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)


            cv2.rectangle(frame, (900, 35), (1000, 255), color=(0, 0, 0), thickness=-1)

            if current_time-start_time>=5:
                if self.current_signal == 'red':
                    self.current_signal ='green'
                    start_time = current_time

                elif self.current_signal=='green':
                    self.current_signal ='red'
                    start_time = current_time


            
            cv2.putText(frame, str("Vehicles in the waiting area: " + str(len(self.waiting_car) if len(self.waiting_car)!=None else 0)), (130, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, str(self.penalty), (500, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

            cv2.circle(frame, center=(950, 90), radius=50, color=(0, 0, 255), thickness=-1 if self.current_signal=='red' else 2)

            cv2.circle(frame, center=(950, 200), radius=50, color=(0, 255, 0), thickness=-1 if self.current_signal=='green' else 2)

            cv2.line(frame, (356, self.cy1), (715, self.cy1), (255, 255, 255), 1)
            cv2.putText(frame, str("Enter"), (382, 277), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

            cv2.line(frame, (143, self.cy2), (922, self.cy2), (255, 255, 255), 1)
            cv2.putText(frame, str("Exit"), (183, 369), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow("RGB", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    async def send_traffic_data(self, websocket, path):
        while True:
            request = await websocket.recv()
            if request == "get_traffic_data":
                with open("/vehical_count.txt", 'w') as file:
                    pickle.dump(f"{self.camera_name}: {len(self.waiting_car)}")

    async def start_websocket_server(self):
        server = await websockets.serve(self.send_traffic_data, "localhost", 8765)
        await server.wait_closed()

    async def main(self):
        await asyncio.gather(self.start_websocket_server(), self.object_tracking())

if __name__ == "__main__":
    tracker = ObjectTracker("camera2", 'veh1.mp4', 281, 374, 3)
    asyncio.run(tracker.main())
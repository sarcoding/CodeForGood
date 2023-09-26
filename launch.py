from main_object import ObjectTracker
from client import request_traffic_data
import asyncio

camera1 = ObjectTracker("camera1", "veh2.mp4", 281, 374, 3)
camera1.object_tracking()

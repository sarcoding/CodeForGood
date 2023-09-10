from main_object import ObjectTracker
import asyncio

camera1 = ObjectTracker("veh2.mp4", 281, 374, 3)

asyncio.run(camera1.main())
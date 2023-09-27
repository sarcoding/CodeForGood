import asyncio
import websockets
import json

import datetime

default_total_signal_time = 240
default_single_road_time = 60

vehicle_counts = {
    'road1': 10,
    'road2': 8,
    'road3': 5,
    'road4': 18 
}


def manage(vehicle_counts):
    total_vehicles_road1 = vehicle_counts['road1']
    total_vehicles_road2 = vehicle_counts['road2']
    total_vehicles_road3 = vehicle_counts['road3']
    total_vehicles_road4 = vehicle_counts['road4']

    signal_time_road1 = default_single_road_time * total_vehicles_road1 / (sum(vehicle_counts.values()))
    signal_time_road2 = default_single_road_time * total_vehicles_road2 / (sum(vehicle_counts.values()))
    signal_time_road3 = default_single_road_time * total_vehicles_road3 / (sum(vehicle_counts.values()))
    signal_time_road4 = default_single_road_time * total_vehicles_road4 / (sum(vehicle_counts.values()))

    actual_total_signal_time = signal_time_road1 + signal_time_road2 + signal_time_road3 + signal_time_road4

    adjustment = default_total_signal_time - actual_total_signal_time

    # Adjust signal times for both roads
    signal_time_road2 += adjustment / 4
    signal_time_road1 += adjustment / 4
    signal_time_road3 += adjustment / 4
    signal_time_road4 += adjustment / 4

    signal_time_road1 = max(10, min(120, signal_time_road1))
    signal_time_road2 = max(10, min(120, signal_time_road2))
    signal_time_road3 = max(10, min(120, signal_time_road3))
    signal_time_road4 = max(10, min(120, signal_time_road4))

    current_time = datetime.datetime.now()
    arr = []
    signal_times = [signal_time_road1, signal_time_road2, signal_time_road3, signal_time_road4]

    for signal_time in signal_times:
        arr.append(current_time.strftime("%H:%M:%S"))
        current_time += datetime.timedelta(seconds=signal_time)
        arr.append(current_time.strftime("%H:%M:%S"))

    print(f"Green signal for road 1: {signal_time_road1:.2f} seconds")
    print(f"Green signal for road 2: {signal_time_road2:.2f} seconds")
    print(f"Green signal for road 3: {signal_time_road3:.2f} seconds")
    print(f"Green signal for road 4: {signal_time_road4:.2f} seconds")

    
    return arr



# print(manage(vehicle_counts))

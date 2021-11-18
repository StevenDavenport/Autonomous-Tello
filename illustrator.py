import cv2
import time

class Illustrator:
    def __init__(self):
        self.fps = 0
        self.start_time = 0

    def start_clock(self):
        self.start_time = time.time()

    def calculate_fps(self):
        self.fps = 1.0 / (time.time() - self.start_time)

    def draw(self, object_data, frame, drone_velocity, battery_level):
        font = cv2.FONT_HERSHEY_SIMPLEX
        battery_string = 'BATTERY: ' + str(battery_level)
        cv2.putText(frame, battery_string, (750, 40), font, 1, (204, 0, 0), 2, cv2.LINE_AA)
        fps_string = 'FPS: ' + str(int(self.fps))
        cv2.putText(frame, fps_string, (800, 80), font, 1, (0, 102, 34), 2, cv2.LINE_AA)
        z_velocity_string = 'Z VELOCITY: ' + str(drone_velocity[1])
        cv2.putText(frame, z_velocity_string, (40, 40), font, 1, (0, 0, 153), 2, cv2.LINE_AA)
        yaw_velocity_string = 'YAW VELOCITY: ' + str(drone_velocity[2])
        cv2.putText(frame, yaw_velocity_string, (40, 80), font, 1, (0, 0, 153), 2, cv2.LINE_AA)

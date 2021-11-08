''''
User tracking module is used to detect and identify the user.
This module relies on an object detection system as well as a
tracking system.
'''

from userTracking.objectDetection.objectDetection import ObjectDetector
from userTracking.objectTracking.objectTracking import ObjectTracker

import cv2


class UserTracking:
    def __init__(self) -> None:
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()


    def track(self, frame):
        self.detector.predict(frame)
        #return self.tracker.predict(frame, detections)

    # Function that draws the bounding boxes on the frame
    def draw_bounding_boxes(self, frame, detections):
        for detection in detections:
            xmin = detection[0]
            ymin = detection[1]
            xmax = detection[2]
            ymax = detection[3]
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        return frame
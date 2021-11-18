from .objectDetection.yolo import YOLOv5
from .objectTracking.deepsort import DeepSORT

import cv2
import numpy as np


class ObjectTracker:
    def __init__(self) -> None:
        self.detector = YOLOv5('yolov5s')
        self.tracker = DeepSORT()

    def track(self, frame):
        detections = self.detector.predict(frame)
        tracked_detections = self.tracker.track(detections, frame)
        return tracked_detections, frame
        


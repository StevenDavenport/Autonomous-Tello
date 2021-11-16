from .objectDetection.yolo import YOLOv5
from .objectTracking.deepsort import DeepSORT

import cv2
import numpy as np


class ObjectTracker:
    def __init__(self) -> None:
        self.detector = YOLOv5('yolov5s')
        self.tracker = DeepSORT()
        self.label_colours = {}
        self.object_labels = []
        self.object_locations = []
        self.object_scores = []

    def track(self, frame):
        detections = self.detector.predict(frame)
        tracked_detections = self.tracker.track(detections, frame)
        return tracked_detections, self.draw_boxes(frame, tracked_detections)

    # Draws tracked detections on frame
    def draw_boxes(self, frame, tracked_detections):
        for detection in tracked_detections:
            frame = cv2.rectangle(frame, (detection['location'][0], detection['location'][1]), (detection['location'][2], detection['location'][3]), self.box_colour_picker(detection['class_label']), 2)
            label = '#{} - {}'.format(detection['object_identity'], detection['class_label'])
            frame = cv2.putText(frame, label, (detection['location'][0], detection['location'][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame

    # Function that randomly picks a colour for each label detected
    def box_colour_picker(self, label):
        if self.label_colours.get(label) is None:
            self.label_colours[label] = np.random.randint(0, 255, (3,)).tolist()
        return self.label_colours[label]
        


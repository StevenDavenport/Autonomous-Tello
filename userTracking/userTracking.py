''''
User tracking module is used to detect and identify the user.
This module relies on an object detection system as well as a
tracking system.
'''

from userTracking.objectDetection.objectDetection import ObjectDetector
from userTracking.objectTracking.objectTracking import ObjectTracker

import cv2
import numpy as np


class UserTracker:
    def __init__(self) -> None:
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.label_colours = {}

    def track(self, frame):
        detections = self.detector.predict(frame)
        self.draw_boxes(frame, detections)

    # Function that draws the bounding boxes, labels and scores on frame
    def draw_boxes(self, frame, detections):
        detections = detections.pandas().xyxy[0]
        labels, scores, xmins, ymins, xmaxs, ymaxs = detections.name, detections.confidence, detections.xmin, detections.ymin, detections.xmax, detections.ymax
        for label, score, xmin, ymin, xmax, ymax in zip(labels, scores, xmins, ymins, xmaxs, ymaxs):
            frame = cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), self.colour_picker(label), 3)
            label = '{}: {:.2f}'.format(label, score)
            frame = cv2.putText(frame, label, (int(xmin), int(ymin)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Function that randomly picks a colour for each label detected
    def colour_picker(self, label):
        if self.label_colours.get(label) is None:
            self.label_colours[label] = np.random.randint(0, 255, (3,)).tolist()
        return self.label_colours[label]


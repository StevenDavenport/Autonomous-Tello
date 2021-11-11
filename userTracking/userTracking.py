from userTracking.objectDetection.objectDetection import ObjectDetector
from userTracking.objectTracking.objectTracking import ObjectTracker

import cv2
import numpy as np


class UserTracker:
    def __init__(self) -> None:
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.label_colours = {}
        self.object_labels = []
        self.object_locations = []
        self.object_scores = []

    def track(self, frame):
        self.object_labels, self.object_scores, self.object_locations = self.detector.predict(frame)
        #tracked_detections = self.tracker.track(detections)
        self.draw_boxes_on_frame(frame)

    # Function that draws the bounding boxes, labels and scores on frame
    # Will need to be changed when object tracking is implemented
    def draw_boxes_on_frame(self, frame):
        for label, score, loc in zip(self.object_labels, self.object_scores, self.object_locations):
            frame = cv2.rectangle(frame, (loc[0], loc[1]), (loc[2], loc[3]), self.box_colour_picker(label), 2)
            label = '{}: {:.2f}'.format(label, score)
            frame = cv2.putText(frame, label, (loc[0], loc[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Function that randomly picks a colour for each label detected
    def box_colour_picker(self, label):
        if self.label_colours.get(label) is None:
            self.label_colours[label] = np.random.randint(0, 255, (3,)).tolist()
        return self.label_colours[label]
        


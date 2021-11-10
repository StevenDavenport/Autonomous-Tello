''''
User tracking module is used to detect and identify the user.
This module relies on an object detection system as well as a
tracking system.
'''

from userTracking.objectDetection.objectDetection import ObjectDetector
from userTracking.objectTracking.objectTracking import ObjectTracker

import cv2
import numpy as np

from userTracking.objectTracking.sort import detection


class UserTracker:
    def __init__(self) -> None:
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.label_colours = {}
        self.object_labels = []
        self.object_locations = []
        self.object_scores = []

    def track(self, frame):
        self.process_detections(self.detector.predict(frame))
        #self.inspect_detections()
        #tracked_detections = self.tracker.track(detections)
        self.draw_boxes(frame)

    # Function that draws the bounding boxes, labels and scores on frame
    def draw_boxes(self, frame):
        for label, score, loc in zip(self.object_labels, self.object_scores, self.object_locations):
            print(len(loc))
            frame = cv2.rectangle(frame, (loc[0], loc[1]), (loc[2], loc[3]), self.colour_picker(label), 2)
            label = '{}: {:.2f}'.format(label, score)
            frame = cv2.putText(frame, label, (loc[0], loc[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Function that randomly picks a colour for each label detected
    def colour_picker(self, label):
        if self.label_colours.get(label) is None:
            self.label_colours[label] = np.random.randint(0, 255, (3,)).tolist()
        return self.label_colours[label]

    def process_detections(self, detections):
        detections = detections.xyxy.to_(torch.device('cpu'))
        print(detections)
        
        self.object_labels = [label for detections.name in detections for label in detections.name]

        print(self.object_labels)

    def inspect_detections(self):
        print('Objects detected: {}'.format(self.object_labels))
        print('Object locations: {}'.format(self.object_locations))
        print('Object scores: {}'.format(self.object_scores))
        


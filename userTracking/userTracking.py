''''
User tracking module is used to detect and identify the user.
This module relies on an object detection system as well as a
tracking system.
'''

# Object detection module imports
from userTracking.objectDetection import ObjectDetection

# Object tracking module imports 
from userTracking.objectTracking import ObjectTracking



class UserTracking:
    def __init__(self) -> None:
        self.Detection = ObjectDetection()
        self.Tracking = ObjectTracking()


    def predict(self, frame):
        return self.Detection.predict(frame) 
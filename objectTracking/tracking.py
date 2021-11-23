from .objectDetection.yolo import YOLOv5
from .objectTracking.deepsort import DeepSORT

class ObjectTracker:
    '''
    This class controls and combines the object detection and tracking.
    '''
    def __init__(self) -> None:
        self.detector = YOLOv5('yolov5s') # Initialize the object detector
        self.tracker = DeepSORT()         # Initialize the object tracker

    def track(self, frame):
        '''
        Tracks the objects in the frame.
        Parameters:
            - frame: the frame to be tracked
        Returns:
            - tracked_objects: the objects tracked in the frame
            - frame: the frame with the tracked objects
        '''
        detections = self.detector.predict(frame)
        tracked_detections = self.tracker.track(detections, frame)
        return tracked_detections, frame 
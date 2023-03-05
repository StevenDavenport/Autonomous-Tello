import torch
from ultralytics import YOLO

class YOLO:
    '''
    This class uses YOLOv5 to detect objects in a frame.
    Other menthods in this class are helper functions.
    '''
    def __init__(self, model, version='yolov8') -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # Use GPU if available
        if version == 'yolov5':
            self.model = torch.hub.load('ultralytics/yolov5', model, pretrained=True).to(self.device).eval()
        elif version == 'yolov8':
            self.model = YOLO("yolov8n.pt")
        

    def predict(self, frame):
        '''
        This function uses YOLOv5 to detect objects in a frame.
        Parameters:
            - frame: a frame from a video stream
        Returns:
            - List of detected objects
                - Object labels
                - Confidence scores
                - Object locations
                (not ordered like this.)
        '''
        return self.model(frame)


    def format_detections(self, detections):
        '''
        Formats the detections, not used - kept for future use.
        '''
        detections = detections.pandas().xyxy[0]
        labels = [str(label) for label in detections.name]
        scores = [float(score) for score in detections.confidence]
        xmins = [int(xmin) for xmin in detections.xmin]
        ymins = [int(ymin) for ymin in detections.ymin]
        xmaxs = [int(xmax) for xmax in detections.xmax]
        ymaxs = [int(ymax) for ymax in detections.ymax]
        locations = [(xmin, ymin, xmax, ymax) for xmin, ymin, xmax, ymax in zip(xmins, ymins, xmaxs, ymaxs)]
        return labels, scores, locations


    def inspect_detections(self, object_labels, object_scores, object_locations, detections):
        '''
        Function is used to check what yolo is detecting.
        not really used but kept as utility.
        '''
        print(detections)
        print()
        print('Object labels: {}'.format(object_labels))
        print('Object confidence scores: {}'.format(object_scores))
        print('Object locations: {}'.format(object_locations))



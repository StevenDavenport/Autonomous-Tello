import torch

class ObjectDetector:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(self.device).eval()


    def predict(self, frame):
        detections = self.model(frame)
        return detections

    


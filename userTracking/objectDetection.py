import torch

class ObjectDetection:
    def __init__(self) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


    def predict(self, frame):
        return self.model(frame)

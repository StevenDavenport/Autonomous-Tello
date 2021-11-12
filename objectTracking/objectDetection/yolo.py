import torch

class YOLOv5:
    def __init__(self, model) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', model, pretrained=True).to(self.device).eval()

    def predict(self, frame):
        detections = self.model(frame)
        return self.format_detections(detections)

    def format_detections(self, detections):
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
        print(detections)
        print()
        print('Object labels: {}'.format(object_labels))
        print('Object confidence scores: {}'.format(object_scores))
        print('Object locations: {}'.format(object_locations))


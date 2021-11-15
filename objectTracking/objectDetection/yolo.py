import torch

class YOLOv5:
    def __init__(self, model) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load('ultralytics/yolov5', model, pretrained=True).to(self.device).eval()

    def predict(self, frame):
        detections = self.model(frame)
        return self.format_detections_for_deepsort(detections)

    def predict_raw(self, frame):
        return self.model(frame)

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

    def format_detections_for_deepsort(self, detections):
        '''
        Need below format
        List of detections, each in tuples of ( [left,top,w,h] , confidence, detection_class)
        left = xmin
        top = ymin
        w = xmax - xmin
        h = ymax - ymin
        confidence = confidence
        detection_class = name
        '''
        detections = detections.pandas().xyxy[0]
        xmins = [float(xmin) for xmin in detections.xmin]
        ymins = [float(ymin) for ymin in detections.ymin]
        xmaxs = [float(xmax) for xmax in detections.xmax]
        ymaxs = [float(ymax) for ymax in detections.ymax]
        ws = [xmax - xmin for xmax, xmin in zip(xmaxs, xmins)]
        hs = [ymax - ymin for ymax, ymin in zip(ymaxs, ymins)]
        detection_classes = [str(label) for label in detections.name]
        confidences = [float(score) for score in detections.confidence]
        detections = [([left, top, w, h], confidence, detection_class) for left, top, w, h, confidence, detection_class in zip(xmins, ymins, ws, hs, confidences, detection_classes)]
        return detections


    def inspect_detections(self, object_labels, object_scores, object_locations, detections):
        print(detections)
        print()
        print('Object labels: {}'.format(object_labels))
        print('Object confidence scores: {}'.format(object_scores))
        print('Object locations: {}'.format(object_locations))


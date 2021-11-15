from deep_sort_realtime.deepsort_tracker import DeepSort
from numpy.core.numeric import identity

class DeepSORT:
    def __init__(self):
        self.tracker = DeepSort(max_age=30, nn_budget=70, override_track_class=None)
        
    def track(self, detections, frame):
        processed_detections = self.preprocess_detections(detections)
        tracks = self.tracker.update_tracks(raw_detections=processed_detections, frame=frame)
        formatted_detections = self.format_detections(tracks, processed_detections)
        return formatted_detections

    def preprocess_detections(self, detections):
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

    def format_detections(self, tracks, detections):
        tracked_detections = list()
        for detection, track in zip(detections, tracks):
            tloc = track.to_ltrb()
            tracked_detections.append(dict(
                class_label=detection[2],
                confidence_score=detection[1],
                object_identity=track.track_id,
                location=[int(tloc[0]), int(tloc[1]), int(tloc[2]), int(tloc[3])]
            ))
        return tracked_detections
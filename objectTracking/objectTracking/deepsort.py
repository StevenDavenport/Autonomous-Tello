from deep_sort_realtime.deepsort_tracker import DeepSort
from numpy.core.numeric import identity

class DeepSORT:
    def __init__(self):
        self.tracker = DeepSort(max_age=30, nn_budget=70, override_track_class=None)
        
    def track(self, detections, frame):
        tracks = self.tracker.update_tracks(raw_detections=detections, frame=frame)
        return self.format_detections(tracks, detections)

    def format_detections(self, tracks, detections):
        tracked_detections = list()
        for detection, track in zip(detections, tracks):
            tracked_detections.append(dict(
                class_label=detection[2],
                confidence_score=detection[1],
                object_identity=track.track_id,
                location=[track.mean[0], track.mean[1], track.mean[2], track.mean[3]]
            ))
        return tracked_detections


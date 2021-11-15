from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSORT:
    def __init__(self):
        self.tracker = DeepSort(max_age=30, nn_budget=70, override_track_class=None)
        
    def track(self, detections, frame):
        detections = self.tracker.update_tracks(raw_detections=detections, frame=frame)
        return detections


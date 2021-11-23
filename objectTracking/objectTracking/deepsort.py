from deep_sort_realtime.deepsort_tracker import DeepSort

class DeepSORT:
    '''
    Simultanious Online Real-time Tracking.
    + Helper functions and preprocessing.
    '''
    def __init__(self):
        self.tracker = DeepSort(max_age=30, nn_budget=70, override_track_class=None) # Deepsort Tracker
        
    def track(self, detections, frame, only_people=True):
        '''
        Tracks objects in frame.
        Parameters:
            - detections: list of detections from Object Detection
            - frame: frame to be tracked
            - only_people: if True, only tracks people (default: True)
        Returns:
            - tracks: list of tracks (in a dictionary format)
        '''
        processed_detections = self.preprocess_detections(detections)
        ready_detections = self.remove_unwanted_detections(processed_detections, only_people)
        tracks = self.tracker.update_tracks(raw_detections=ready_detections, frame=frame)
        formatted_detections = self.format_detections(tracks, ready_detections)
        return formatted_detections

    def remove_unwanted_detections(self, detections, only_people):  
        '''
        Removes the unwanted objects from the detections.
        Parameters:
            - detections: list of detections from Object Detection
            - only_people: if True, only tracks people (default: True)
        Returns:
            - ready_detections/detections: list of detections ready for DeepSort
        '''
        if only_people:
            ready_detections = [d for d in detections if d[2] == 'person']
            return ready_detections
        return detections
        
    def preprocess_detections(self, detections):
        '''
        Preprocesses the detections, ready for DeepSort.
        Parameters:
            - detections: list of detections from Object Detection
        Returns:
            - detections: ready for DeepSort
                - ( [left,top,w,h] , confidence, detection_class )
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
        '''
        Formats the detections and tracks into a dictionary format.
        Parameters:
            - tracks: list of tracks (raw format)
            - detections: list of detections
        Returns:
            - formatted_detections: list of detections & tracks in dictionary format
        '''
        tracked_detections = list()
        for detection, track in zip(detections, tracks):
            tloc = track.to_ltrb()
            tracked_detections.append(dict(
                class_label=detection[2],
                confidence_score=detection[1],
                tracking_id=track.track_id,
                location=[int(tloc[0]), int(tloc[1]), int(tloc[2]), int(tloc[3])]
            ))
        return tracked_detections
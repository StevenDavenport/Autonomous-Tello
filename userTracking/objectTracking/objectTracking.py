# Object tracker that uses SORT to multiple objects in a frame.
class ObjectTracker:
    def __init__(self,
                 maxObjects=20,
                 max_age=5,
                 min_hits=3,
                 iou_threshold=0.3,
                 score_threshold=0.3):
        # Initialize variables
        self.maxObjects = maxObjects
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.trackers = []
        self.frame_count = 0

    def track(self, objects, frame_number=1):
        # Update trackers
        self.frame_count += 1
        # For each new object
        for new_object in objects:
            # If new object is not already tracked
            if len(self.trackers) < self.maxObjects:
                # Add new tracker
                self.trackers.append(Tracker(new_object, self.frame_count))
            else:
                # Find tracker with highest iou
                highest_iou = 0
                highest_iou_index = 0
                for i, tracker in enumerate(self.trackers):
                    # Compute iou
                    iou = tracker.iou(new_object)
                    # Update tracker if iou is higher
                    if iou > highest_iou:
                        highest_iou = iou
                        highest_iou_index = i
                # If iou is high enough
                if highest_iou > self.iou_threshold:
                    # Update tracker
                    self.trackers[highest_iou_index].update(new_object, self.frame_count)
                # If iou is not high enough
                else:
                    # Add new tracker
                    self.trackers.append(Tracker(new_object, self.frame_count))
        # Remove old trackers
        for i, tracker in enumerate(self.trackers):
            # If tracker is old
            if tracker.age > self.max_age or tracker.hits < self.min_hits:
                # Remove tracker
                self.trackers.pop(i)
        # Return trackers
        return self.trackers

        

    
class Tracker:
    def __init__(self, object, frame_number):
        # Initialize variables
        self.object = object
        self.frame_number = frame_number
        self.age = 0
        self.hits = 0
        self.score = 0
        self.matched = False

    def update(self, object, frame_number):
        # Update variables
        self.object = object
        self.frame_number = frame_number
        self.age = 0
        self.hits += 1
        self.score = 0
        self.matched = False

    def iou(self, object):
        # Compute iou
        x1 = max(self.object.x, object.x)
        y1 = max(self.object.y, object.y)
        x2 = min(self.object.x + self.object.w, object.x + object.w)
        y2 = min(self.object.y + self.object.h, object.y + object.h)
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        union = self.object.w * self.object.h + object.w * object.h - intersection
        return intersection / union



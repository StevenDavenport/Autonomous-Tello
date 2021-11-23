import cv2
import time
import numpy as np

class Illustrator:
    '''
    This class handles all the on screen effects.
    Such as Showing the frame, FPS, Battery level, etc.
    '''
    def __init__(self):
        self.fps = 0            # Frames per second
        self.start_time = 0     # Time at which the clock started
        self.label_colours = {} # Dictionary of colours for each label

    def start_clock(self):
        '''
        Starts the clock.
        '''
        self.start_time = time.time()

    def calculate_fps(self):
        '''
        Calculates the FPS.
        '''
        self.fps = 1.0 / (time.time() - self.start_time)

    def draw(self, object_data, frame, drone_velocity, battery_level, braking=False):
        '''
        Draws Data on the frame.
        Parameters:
            - object_data: List of objects detected, with their data.
            - frame: Frame to draw on.
            - drone_velocity: Velocity of the drone.
            - battery_level: Battery level of the drone.
            - braking: Boolean to indicate if the drone is braking (default: False).
        Returns:
            - Nothing.
        '''
        self.draw_boxes(frame, object_data)
        font = cv2.FONT_HERSHEY_SIMPLEX
        battery_string = 'BATTERY: ' + str(battery_level)
        cv2.putText(frame, battery_string, (750, 40), font, 1, (204, 0, 0), 2, cv2.LINE_AA)
        fps_string = 'FPS: ' + str(int(self.fps))
        cv2.putText(frame, fps_string, (800, 80), font, 1, (0, 102, 34), 2, cv2.LINE_AA)
        z_velocity_string = 'Z VELOCITY: ' + str(drone_velocity[1])
        cv2.putText(frame, z_velocity_string, (40, 40), font, 1, (0, 0, 153), 2, cv2.LINE_AA)
        yaw_velocity_string = 'YAW VELOCITY: ' + str(drone_velocity[3])
        cv2.putText(frame, yaw_velocity_string, (40, 80), font, 1, (0, 0, 153), 2, cv2.LINE_AA)
        if braking:
            cv2.putText(frame, 'Braking', (40, 120), font, 3, (0, 0, 153), 2, cv2.LINE_AA)
        cv2.imshow('Drone Vision', frame)

    def draw_boxes(self, frame, tracked_detections):
        ''' 
        Draws the bounding boxes on the frame.
        Parameters:
            - frame: Frame to draw on.
            - tracked_detections: List of objects detected, with their data. (Dict)
        '''
        for detection in tracked_detections:
            frame = cv2.rectangle(frame, (detection['location'][0], detection['location'][1]), (detection['location'][2], detection['location'][3]), self.box_colour_picker(detection['class_label']), 2)
            label = '#{} - {}'.format(detection['tracking_id'], detection['class_label'])
            frame = cv2.putText(frame, label, (detection['location'][0], detection['location'][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        return frame

    def box_colour_picker(self, label):
        '''
        Picks a random colour for each label.
        Parameters:
            - label: Label of the object.
        Returns:
            - Colour of the label.
        '''
        if self.label_colours.get(label) is None:
            self.label_colours[label] = np.random.randint(0, 255, (3,)).tolist()
        return self.label_colours[label]

    def check_done(self):
        '''
        Checks if the OpenCV window is ready to close.
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        else:
            return False

    def close(self):
        '''
        Closes the OpenCV window.
        '''
        cv2.destroyAllWindows()
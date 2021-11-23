class AutoPilot:
    '''
    This class is the logic for adjusting the position of the drone
    autonomously. 
    '''
    def __init__(self) -> None:
        self.velocity = [0, 0, 0, 0]        # velocity of the drone [x, z, y, yaw]
        self.user_track_id = -1             # tracking id of the user
        self.forget_user_threshold = 100    # threshold for forgetting the user (in frames)
        self.speed = 30                     # speed of the drone
        self.standard_z_speed = self.speed  # speed of the drone along the z-axis
        self.fast_z_speed = int(self.speed * 4) # speed of the drone along the z-axis
        self.standard_yaw_speed = 40        # speed of the drone along the yaw-axis
        self.fast_yaw_speed = int(self.standard_yaw_speed * 2) # speed of the drone along the yaw-axis
        self.momentum = 0                   # momentum of the drone
        self.momentum_threshold = 30        # threshold for the momentum until braking required
        self.width = 960                    # width of the frame
        self.height = 720                   # height of the frame
 

    def navigate(self, tracking_data, frame):
        '''
        Calculates the required drone movement based on the
        tracking data and the frame.
        Allowing the drone to follow the user.
        Parameters:
            - tracking_data: List of dictionaries containing from the tracker
                - Dictionary with the following keys:
                    - 'class_label' : The class label of the object
                    - 'confidence_score' : The confidence score of the object
                    - 'tracking_id' : The tracking id of the object
                    - 'location' : The location of the object [xmin, ymin, xmax, ymax]
                - frame: The frame of the video
        Returns:
            - Velocity: The velocity of the drone [x, z, y, yaw]
            - Boolean: True if the drone should brake, False otherwise
        '''
        braking = False
        if len(tracking_data) == 0: # No user -> repeat last command
            return self.velocity, braking
        self.should_forget_user(tracking_data) # Forget user if old
        for track in tracking_data: # Find which object is the user
            if track['tracking_id'] == self.user_track_id or self.user_track_id == -1:
                braking = self.calculate_positional_adjustments(track['location'], frame)
                break
        return self.velocity, braking

    def calculate_positional_adjustments(self, user_location, frame):
        '''
        Calculates the adjustments to the drone position based on the
        user location and the frame.
        Parameters:
            - user_location: The location of the user [xmin, ymin, xmax, ymax]
            - frame: The frame of the video
        Returns:
            - Boolean: True if the drone should brake, False otherwise
        '''
        self.calculate_z_adjustment(user_location, frame)
        self.calculate_yaw_adjustment(user_location, frame)
        self.calculate_y_adjustment(user_location, frame)
        return self.calculate_braking()    

    def calculate_z_adjustment(self, user_location, frame):
        '''
        Calculates the adjustment to the z-axis based on the
        user location and the frame.
        Parameters:
            - user_location: The location of the user [xmin, ymin, xmax, ymax]
            - frame: The frame of the video
        Returns: Nothing - The self.velocity is updated
        '''
        bbox_area = abs(user_location[3]-user_location[1]) * abs(user_location[2]-user_location[0])
        frame_area = frame.shape[0] * frame.shape[1]
        if bbox_area < frame_area / 9:
            self.velocity[1] = self.fast_z_speed
            if self.momentum >= 0:
                self.momentum += 4
            else:
                self.momentum = 0
        elif bbox_area < frame_area / 5:
            self.velocity[1] = self.standard_z_speed
            if self.momentum >= 0:
                self.momentum += 1
            else:
                self.momentum = 0
        elif bbox_area > frame_area / 2:
            self.velocity[1] = -self.fast_z_speed / 2
            if self.momentum <= 0:
                self.momentum -= 1.5
            else:
                self.momentum = 0
        elif bbox_area > frame_area / 1.5:
            self.velocity[1] = -self.standard_z_speed
            if self.momentum <= 0:
                self.momentum -= 1
            else:
                self.momentum = 0
        else:
            self.velocity[1] = 0
        
    def calculate_braking(self):
        '''
        Calulates braking based on the momentum.
        Parameters: Nothing
        Returns:
            - Boolean: True if the drone should brake, False otherwise
        '''
        if self.velocity[1] == 0:
            if self.momentum > self.momentum_threshold \
                or self.momentum < -self.momentum_threshold:
                self.velocity[1] = -self.velocity[1]
                self.momentum = 0
                return True
        return False

    def calculate_yaw_adjustment(self, user_location, frame):
        '''
        Calculates the adjustment to the yaw-axis based on the
        user location and the frame.
        Parameters:
            - user_location: The location of the user [xmin, ymin, xmax, ymax]
            - frame: The frame of the video
        Returns: Nothing - The self.velocity is updated
        '''
        # Required variables
        x_vector = int(frame.shape[1] / 2) - (user_location[0] + ((user_location[2] - user_location[0]) / 2))
        turn_fast_threshold = 350
        turn_slow_threshold = 150
        # Turn right fast
        if x_vector > turn_fast_threshold:
            self.velocity[3] = -self.fast_yaw_speed
        #Turn right slow
        elif x_vector > turn_slow_threshold:
            self.velocity[3] = -self.standard_yaw_speed
        # Turn left fast
        elif x_vector < -turn_fast_threshold:
            self.velocity[3] = self.fast_yaw_speed
        # Turn left slow
        elif x_vector < -turn_slow_threshold:
            self.velocity[3] = self.standard_yaw_speed
        else:
            self.velocity[3] = 0

    def calculate_y_adjustment(self, user_location, frame):
        '''
        Make sure the top of the bounding box is in frame,
        but still above the half way mark of the frame.
        Parameters:
            - user_location: The location of the user [xmin, ymin, xmax, ymax]
            - frame: The frame of the video
        Returns: Nothing - The self.velocity is updated
        '''
        top_of_bbox = user_location[1]
        lower_y_threshold = self.height * 0.80
        upper_y_threshold = self.height * 0.05
        if top_of_bbox > lower_y_threshold:
            self.velocity[2] = self.speed / 2
        elif top_of_bbox < lower_y_threshold and top_of_bbox > upper_y_threshold:
            self.velocity[2] = 0
        elif top_of_bbox < upper_y_threshold:
            self.velocity[2] = -self.speed / 2

    def should_forget_user(self, tracking_data):
        '''
        Calculates whether the user should be forgotten based on the
        tracking data.
        Parameters:
            - tracking_data: List of dictionaries containing from the tracker
                - Dictionary with the following keys:
                    - 'class_label' : The class label of the object
                    - 'confidence_score' : The confidence score of the object
                    - 'tracking_id' : The tracking id of the object
                    - 'location' : The location of the object [xmin, ymin, xmax, ymax]
        Returns:
            - Nothing - The self.user_track_id is updated
        '''
        if len(tracking_data) == 0: # No user
            self.user_track_id = -1
            return
        for track in tracking_data: # Is user old?
            if track['tracking_id'] == self.user_track_id:
                if track['tracking_id'] > self.forget_user_threshold:
                    self.user_track_id = -1
                    return
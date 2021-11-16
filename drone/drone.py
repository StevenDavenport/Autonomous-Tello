# Python package that comminicates with the DJI tello drone
from djitellopy import Tello 
from threading import Thread
import os
import cv2
import time


class DroneController:
    def __init__(self) -> None:
        self.tello = Tello()
        self.frame_size = tuple()
        self.user_track_id = int()
        self.forget_user_threshold = 300
        self.velocity = [0, 0, 0, 0]
        self.standard_z_speed = 30
        self.fast_z_speed = 100
        self.standard_yaw_speed = 40
        self.fast_yaw_speed = 100
        self.momentum = 0
        self.momentum_threshold = 30
        self.video_thread = Thread(target=self.record_video)
        self.video_thread_flag = False

    # Connect the controller to physical tello - optional turn on stream
    def connect(self, streamon=True):
        self.tello.connect()
        if streamon:
            self.tello.streamoff()
            self.tello.streamon()    
        
    # Flight test for Tello
    def test_drone_movement(self):
        print(self.tello.get_battery())
        self.tello.takeoff()
        self.tello.rotate_clockwise(50)
        self.tello.land()

    # Returns the frame captured by tello
    def get_frame(self):
        return self.tello.get_frame_read().frame

    # Returns the battery level of tello
    def get_battery(self):
        return self.tello.get_battery()

    # Function that decides on how the drone will move
    # to follow the user
    def navigate(self, tracking_data, frame):
        # Should the user be forgotten?
        self.should_forget_user(tracking_data)
        # If there is a user, track them
        # If not, get a new user and track them
        for track in tracking_data:
            if track['tracking_id'] == self.user_track_id or self.user_track_id == -1:
                required_adjustments = self.calculate_positional_adjustments(track['location'])
                adjustments = self.adjust_position(required_adjustments)
                return adjustments

    # Function that calculates wehther the user should be forgotten
    def should_forget_user(self, tracking_data):
        # If there is no user, forget the user
        if len(tracking_data) == 0:
            self.user_track_id = -1
            return
        # If there is a user, check if it is old
        for track in tracking_data:
            if track['tracking_id'] == self.user_track_id:
                if track['tracking_id'] > self.forget_user_threshold:
                    self.user_track_id = -1
                    return


    # Function that adjusts the postion of the drone in relation to the user
    def calculate_positional_adjustments(self, user_location):
        self.calculate_z_adjustment(user_location)
        self.calculate_braking(user_location)
        self.calculate_yaw_adjustment(user_location)


    def calculate_z_adjustment(self, user_location, frame):
        '''
        Algorithm:
            -Calculate the area of the users bounding box.
            -Decide on the action required.
            -Calculate momentum of the action & previous actions.
            -The required Z velocity is stored in self.velocity 
        '''
        # Required variables
        bbox_area = abs(user_location[3]-user_location[1]) * abs(user_location[2]-user_location[0])
        frame_area = frame.shape[0] * frame.shape[1]
        # Move forward fast
        if bbox_area < frame_area / 9:
            self.velocity[1] = self.fast_z_speed
            if self.momentum >= 0:
                self.momentum += 4
            else:
                self.momentum = 0
        # Move forward slow
        elif bbox_area < frame_area / 5:
            self.velocity[1] = self.standard_z_speed
            if self.momentum >= 0:
                self.momentum += 1
            else:
                self.momentum = 0
        # Move backward fast
        elif bbox_area > frame_area / 2:
            self.velocity[1] = -self.fast_z_speed / 2
            if self.momentum <= 0:
                self.momentum -= 1.5
            else:
                self.momentum = 0
        # Move backward slow
        elif bbox_area > frame_area / 1.5:
            self.velocity[1] = -self.standard_z_speed
            if self.momentum <= 0:
                self.momentum -= 1
            else:
                self.momentum = 0
        
    def calculate_braking(self, user_location):
        '''
        Algotithm:
            -Breaking is calculated using self.momentum.
            -Which is calculated by self.calculate_z_adjustment().
            -The velocity is adjusted by self.momentum.
        '''
        if self.momentum > self.momentum_threshold:
            self.velocity[1] = -self.standard_z_speed
        elif self.momentum < -self.momentum_threshold:
            self.velocity[1] = self.standard_z_speed
        else:
            self.velocity[1] = 0
            self.momentum = 0

    def calculate_yaw_adjustment(self, user_location, frame):
        '''
        Algorithm:
            -X vector is the vector between the center of the users bounding box 
                and the center of the frame on the x axis.
            -The size of that vector is used to calculate required yaw adjustment. 
            -The required yaw adjustment is stored in self.velocity.
        '''
        # Required variables
        x_vector = int(frame.shape[1] / 2) - (user_location[0] + ((user_location[2] - user_location[0]) / 2))
        turn_fast_threshold = 350
        turn_slow_threshold = 150
        # Turn right fast
        if x_vector > turn_fast_threshold:
            self.velocity[3] = self.fast_yaw_speed
        #Turn right slow
        elif x_vector > turn_slow_threshold:
            self.velocity[3] = self.standard_yaw_speed
        # Turn left fast
        elif x_vector < -turn_fast_threshold:
            self.velocity[3] = -self.fast_yaw_speed
        # Turn left slow
        elif x_vector < -turn_slow_threshold:
            self.velocity[3] = -self.standard_yaw_speed
        else:
            self.velocity[3] = 0

    def adjust_position(self):
        '''
        Algorithm:
            -The calculated velocity adjustments is send as a command to the drone.
            -Velocity = [x, z, y, yaw]
        '''
        self.tello.send_rc_control(self.velocity[0], self.velocity[1], self.velocity[2], self.velocity[3])

    def takeoff(self):
        '''
        Sends the command to the drone to takeoff.
        '''
        self.tello.takeoff()

    def land(self):
        '''
        Sends the command to the drone to land.
        '''
        self.tello.land()

    def start_video_thread(self):
        '''
        Starts the thread which the video capture will use.
        '''
        if not self.video_thread_flag:
            self.video_thread.start()
            self.video_thread_flag= True

    def join_video_thread(self):
        '''
        Joins the video thread.
        '''
        if self.video_thread_flag:
            self.video_thread.join()
            self.video_thread_flag = False
    
    def record_video(self):
        file_id = 0
        directory = './videos/'
        file_type = '.avi'
        full_directory = ''
        height, width, _ = self.get_frame().shape

        # find a file name that has not been used
        while True:
            if os.path.isfile(directory + str(file_id) + file_type):
                file_id += 1
            else:
                full_directory = directory + str(file_id) + file_type
                break
        video = cv2.VideoWriter(full_directory, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

        # frame loop, get and save the frames
        while self.record == True: 
            video.write(self.get_frame())
            time.sleep(1 / 60)
        video.release()
from .autopilot import AutoPilot
from djitellopy import Tello 
from threading import Thread
import os
import cv2
import time
import datetime


class DroneController:
    '''
    This class is used to control the drone, 
    as well as get and set drone data. 
    '''
    def __init__(self) -> None:
        self.tello = Tello()                    # Create the Tello object -> communicates with the drone
        self.pilot = AutoPilot()                # Create the autopilot object -> decides the drone's movement
        self.frame_height = 720                 # Height of the frame
        self.frame_width = 960                  # Width of the frame
        self.video_thread = Thread(target=self.record_video)   # Thread for recording the video
        self.video_thread_flag = False          # Flag for the video thread

    def connect(self, streamon=True):
        '''
        Connects the controller to the tello drone.
        Parameters:
            -streamon: True if the stream should be turned on.
        Returns: Nothing
        '''
        self.tello.connect()
        if streamon:
            self.tello.streamoff()
            self.tello.streamon()    
        
    def get_frame(self):
        '''
        Parameters: None
        Returns: The frame captured by tello
        '''
        return self.tello.get_frame_read().frame

    def get_battery(self):
        '''
        Parameters: None
        Returns: The battery level of the drone.
        '''
        return self.tello.get_battery()
        
    def move(self, tracking_data, frame):
        '''
        Moves the drone according to the autopilot.
        Parameters:
            -tracking_data: The data from the tracking algorithm.
            -frame: The frame from the video capture.
        Returns: Nothing
        '''
        velocity, braking = self.pilot.navigate(tracking_data, frame)
        self.tello.send_rc_control(int(velocity[0]), int(velocity[1]), int(velocity[2]), int(velocity[3]))
        return velocity, braking

    def takeoff(self):
        '''
        Sends the command to the drone to takeoff.
        Parameters: None
        Returns: Nothing
        '''
        self.tello.takeoff()

    def land(self):
        '''
        Sends the command to the drone to land.
        Parameters: None
        Returns: Nothing
        '''
        self.tello.land()

    def shutdown(self):
        '''
        Sends the command to the drone to shutdown.
        Parameters: None
        Returns: Nothing
        '''
        self.tello.end()

    def start_recording(self):
        '''
        Starts the thread which the video capture will use.
        Parameters: None
        Returns: Nothing
        '''
        if not self.video_thread_flag:
            self.video_thread.start()
            self.video_thread_flag= True

    def stop_recording(self):
        '''
        Joins the video thread.
        Parameters: None
        Returns: Nothing
        '''
        if self.video_thread_flag:
            self.record = False
            #self.video_thread.join()
            #self.video_thread_flag = False
    
    def record_video(self):
        '''
        Records a video from the drones onboard camera.
        Saves the vido to './videos/' as a '.avi' file.
        Parameters: None
        Returns: Nothing
        '''
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        file_name = 'video_' + str(date) + '_#'
        file_id = 0
        directory = './videos/'
        file_type = '.avi'
        full_directory = ''
        while True: # find a file name that has not been used
            if os.path.isfile(directory + file_name + str(file_id) + file_type):
                file_id += 1
            else:
                full_directory = directory + file_name + str(file_id) + file_type
                break
        video = cv2.VideoWriter(full_directory, cv2.VideoWriter_fourcc(*'XVID'), 30, (self.frame_width, self.frame_height))
        while self.record == self. record == True: # record until told to stop
            frame = self.get_frame()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video.write(frame)
            time.sleep(1 / 60)
        video.release()

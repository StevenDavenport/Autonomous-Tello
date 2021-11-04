# Python package that comminicates with the DJI tello drone
from djitellopy import Tello 



class DroneController:
    def __init__(self) -> None:
        self.tello = Tello()


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
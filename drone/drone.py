# Python package that comminicates with the DJI tello drone
from djitellopy import Tello 


class DroneController:
    def __init__(self) -> None:
        self.tello = Tello()


    def connect(self, streamon=True):
        self.tello.connect()
        if streamon:
            self.tello.streamoff()
            self.tello.streamon()
        
        
    def test_drone_movement(self):
        print(self.tello.get_battery())
        self.tello.takeoff()
        self.tello.rotate_clockwise(50)
        self.tello.land()
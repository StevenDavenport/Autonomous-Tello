from drone.drone import DroneController
from keybaord import KeyboardController
from objectTracking.tracking import ObjectTracker
from illustrator import Illustrator

def main():
    illustrator = Illustrator()
    tracker = ObjectTracker()
    keyboard = KeyboardController()
    drone = DroneController()
    drone.connect()

    while True:
        illustrator.start_clock()
        key_press = keyboard.get_key_pressed()
        if key_press == 'enter':
            drone.takeoff()
        elif key_press == 'space':
            drone.land()
        elif key_press == 'esc':
            drone.shutdown()
            break

        frame = drone.get_frame()
        tracking_data, tracked_frame = tracker.track(frame)
        drone_velocity, braking = drone.navigate(tracking_data, tracked_frame) 
        battery_level = drone.get_battery() 
        illustrator.calculate_fps()
        illustrator.draw(tracking_data, tracked_frame, drone_velocity, battery_level, braking)
        if illustrator.check_done() == True:
            break

    keyboard.disconnect()
    illustrator.close()

if __name__ == '__main__':
    main()

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
    drone_takeoff = False
    recording = False

    while True:
        illustrator.start_clock()
        key_press = keyboard.get_key_pressed()
        if key_press == 'enter':
            drone.land() if drone_takeoff else drone.takeoff()
            drone_takeoff = not drone_takeoff
        elif key_press == 'space':
            drone.stop_recording() if recording else drone.start_recording()
            recording = not recording
        elif key_press == 'esc':
            drone.shutdown()
            break

        frame = drone.get_frame()
        tracking_data, tracked_frame = tracker.track(frame)
        drone_velocity, braking = drone.move(tracking_data, tracked_frame) 
        battery_level = drone.get_battery() 
        illustrator.calculate_fps()
        illustrator.draw(tracking_data, tracked_frame, drone_velocity, battery_level, braking)
        if illustrator.check_done() == True:
            break

    keyboard.disconnect()
    illustrator.close()

if __name__ == '__main__':
    main()

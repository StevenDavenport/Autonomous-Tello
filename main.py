from drone.drone import DroneController
from objectTracking.tracking import ObjectTracker
from illustrator import Illustrator

import cv2


# Main function which connects the modules and drives the program
def main():

    # Testing
    testing = False
    test_data_path = 'test_data/person.jpeg'

    # Create Illustrator object
    illustrator = Illustrator()


    # Create user tracking object
    tracker = ObjectTracker()

    # Create drone control object
    # Connect it to the physical drone
    drone = DroneController()
    if not testing:
        drone.connect()
        drone.takeoff()

    # Video loop
    while True:
        # FPS Calculations
        illustrator.start_clock()

        # Get the frame from tello or test image -> transform
        if testing:
            frame = cv2.imread(test_data_path)
            #frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
        else:
            frame = drone.get_frame()

        # Track the user
        tracking_data, tracked_frame = tracker.track(frame)

        # Move the drone in relation to the user
        drone_velocity = drone.navigate(tracking_data, tracked_frame)
        
        # FPS Calculations & Display
        illustrator.calculate_fps()
        battery_level = drone.get_battery() if not testing else 100
        illustrator.draw(tracking_data, tracked_frame, drone_velocity, battery_level)

        # Display Frame and wait for key press  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Close the viewing window
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

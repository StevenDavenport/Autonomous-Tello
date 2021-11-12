from drone.drone import DroneController
from objectTracking.tracking import ObjectTracker
import cv2
import time


# Main function which connects the modules and drives the program
def main():

    # Testing
    testing = True 
    test_data_path = 'test_data/test_image.jpg'

    # Create drone control object
    # Connect it to the physical drone
    if not testing:
        drone = DroneController()
        drone.connect()

    # Create user tracking object
    tracker = ObjectTracker()

    # Video loop
    while True:
        # FPS Calculations
        start_time = time.time()

        # Get the frame from tello or test image -> transform
        if testing:
            frame = cv2.imread(test_data_path)
            frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
        else:
            frame = drone.get_frame()

        # Object detection on the frame
        tracker.track(frame)
        
        # FPS Calculations & Display
        fps = 1.0 / (time.time() - start_time)
        fps_string = 'FPS: ' + str(int(fps))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, fps_string, (800, 80), font, 1, (0, 102, 34), 2, cv2.LINE_AA)

        # Display Frame 
        cv2.imshow('Drone Vision', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Close the viewing window
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

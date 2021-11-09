from drone.drone import DroneController
from userTracking.userTracking import UserTracker
import cv2
import time


# Main function which connects the modules and drives the program
def main():

    # Create drone control object
    # Connect it to the physical drone
    drone = DroneController()
    drone.connect()

    # Create user tracking object
    tracker = UserTracker()

    # Video loop
    while True:
        # FPS Calculations
        start_time = time.time()

        # Get the frame from tello -> transform
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

# Drone control module
from drone.drone import DroneController

# User tracking module
from userTracking.userTracking import UserTracking


# Main function which connects the modules and drives the program
def main():

    # Create drone control object
    drone = DroneController()

    # Connect the control module to physical drone
    drone.connect()

    # flight and vision test
    drone.test_drone_movement()


if __name__ == '__main__':
    main()

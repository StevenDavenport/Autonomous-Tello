from monodepth2 import monodepth2
import cv2

class DepthEstimator:
    def __init__(self):
        self.depth_estimator = monodepth2()

    def predict(self, frame):
        return self.depth_estimator.predict(frame)

def test():
    md = monodepth2()
    path = 'depthEstimation/person.jpeg'
    frame = cv2.imread(path)
    frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
    while True:
        cv2.imshow('Origonal Frame', frame)
        depth = md.eval(frame)
        cv2.imshow('Depth', depth)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    test()

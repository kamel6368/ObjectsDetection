import cv2
from threading import Thread


class VideoCapturingWorker(Thread):

    def __init__(self):
        self.exit = False
        self.video_capture = None
        self.wait = None
        Thread.__init__(self)

    def run(self):
        self.video_capture = cv2.VideoCapture(0)

        while not self.exit:
            if not self.wait:
                self.video_capture.grab()

        self.video_capture.release()

    def read(self):
        self.wait = True
        _, frame = self.video_capture.read()
        self.wait = False
        return frame

    def set_frame_rate(self, fps):
        self.wait = True
        self.video_capture.set(cv2.CAP_PROP_FPS, fps)
        self.wait = False

    def release(self):
        self.exit = True

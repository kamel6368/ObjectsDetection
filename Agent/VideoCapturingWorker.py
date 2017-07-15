import cv2
from threading import Thread


class VideoCapturingWorker(Thread):

    def __init__(self):
        self.exit = False
        self.video_capture = None
        self.getting_current_frame = None
        Thread.__init__(self)

    def run(self):
        self.video_capture = cv2.VideoCapture(0)

        while not self.exit:
            if not self.getting_current_frame:
                self.video_capture.grab()

        self.video_capture.release()

    def read(self):
        self.getting_current_frame = True
        _, frame = self.video_capture.read()
        self.getting_current_frame = False
        return frame

    def release(self):
        self.exit = True

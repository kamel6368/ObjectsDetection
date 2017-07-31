import tasks
from threading import Thread
from time import time
from Common.config import config


class VideoRecorder(Thread):

    def __init__(self, main, duration):
        self.main = main
        self.duration = duration
        self.time_started = None
        self.interrupted = False
        Thread.__init__(self)

    def setup(self):
        # Note: here is the place to set frame rate of video
        self.time_started = time()

    def run(self):
        self.setup()
        while time() - self.time_started <= self.duration and not self.interrupted:
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)
        if not self.interrupted:
            self.release()

    def release(self):
        self.main.video_recorder = None
        tasks.send_video_done_recording(self.main.tcp_client)

    def interrupt(self):
        self.interrupted = True
        self.main.video_recorder = None

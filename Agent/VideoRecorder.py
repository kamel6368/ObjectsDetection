import tasks
from threading import Thread
from time import time, sleep


class VideoRecorder(Thread):

    def __init__(self, main, duration):
        self.main = main
        self.duration = duration
        self.recorded_frames = 0
        self.interrupted = False
        self.ack_received = False
        Thread.__init__(self)

    def setup(self):
        # Note: here is the place to set frame rate of video
        self.recorded_frames = 0

    def run(self):
        self.setup()
        while self.recorded_frames < self.duration and not self.interrupted:
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)
            self.recorded_frames += 1
            while not self.ack_received:
                pass
        if not self.interrupted:
            self._release()

    def acknowledge_image_received(self):
        self.ack_received = True

    def _release(self):
        self.main.video_recorder = None
        sleep(1)  # this sleep is needed to ensure that last picture is send correctly
        tasks.send_video_done_recording(self.main.tcp_client)

    def interrupt(self):
        self.interrupted = True
        self.main.video_recorder = None

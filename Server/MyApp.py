import tasks
import configurable_objects_factory
from kivy.app import App
from kivy.lang.builder import Builder
from collections import deque
from MainLayout import MainLayout
from Common.Logger import Logger
from Common.TCPConnections import StreamMode


class MyApp(App):

    def __init__(self):
        self.exit = False
        self.main_layout = None
        self.tcp_server = None
        self.tcp_client = None
        self.is_agent_alive = False
        self.logger = None
        self.is_stream_on = False
        self.single_image_mode = False
        self.apply_quantization = False
        self.object_detector = None
        self.stream_mode = StreamMode.EACH_FRAME
        self.video_buffer = deque([])
        self.frames_buffer_size = 10
        self.frames_buffer = deque([], maxlen=self.frames_buffer_size)
        self.current_frame_index = -1
        self.objects_unificator = None
        App.__init__(self)

    def build(self):
        Builder.load_file('Layouts/main_layout.kv')
        self.main_layout = MainLayout(self)
        return self.main_layout

    def on_start(self):
        self.logger = Logger()

        self.tcp_client = configurable_objects_factory.create_tcp_client(self.logger)
        tasks.try_reconnect_to_alive_agents(self, self.tcp_client)
        self.tcp_server = configurable_objects_factory.create_tcp_server(self, self.logger)
        self.tcp_server.start()

        self.object_detector = configurable_objects_factory.create_object_detector()
        self.objects_unificator = configurable_objects_factory.create_objects_unificator()

    def on_stop(self):
        self.tcp_server.disconnect()
        self.tcp_client.disconnect()

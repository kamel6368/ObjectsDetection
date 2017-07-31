import tasks
import ImageProcessing.parameters_loader as parameters_loader
from kivy.app import App
from kivy.lang.builder import Builder
from collections import deque
from MainLayout import MainLayout
from Common.TCPConnections import TCPClient
from TCPServer import TCPServer
from Common.config import config
from Common.Logger import Logger
from ImageProcessing.ObjectDetector import ObjectDetector
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
        self.frames_buffer = deque([], maxlen=10)
        self.current_frame = -1
        App.__init__(self)

    def build(self):
        Builder.load_file('Layouts/main_layout.kv')
        self.main_layout = MainLayout(self)
        return self.main_layout

    def start_tcp_server(self):
        receive_address = config('TCPConnection/receive_address')
        receive_port = config('TCPConnection/receive_port')
        buffer_size = config('TCPConnection/buffer_size')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_server = TCPServer(receive_address, receive_port, buffer_size, socket_timeout, self.logger, self)
        self.tcp_server.start()

    def start_tcp_client(self):
        agent_address = config('TCPConnection/agent_address')
        agent_port = config('TCPConnection/agent_port')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_client = TCPClient(agent_address, agent_port, socket_timeout, self.logger)

    def on_start(self):
        self.logger = Logger()

        self.start_tcp_client()
        tasks.try_reconnect_to_alive_agents(self, self.tcp_client)
        self.start_tcp_server()

        self.object_detector = ObjectDetector()
        parameters_loader.load_all_from_file(self.object_detector)

    def on_stop(self):
        self.tcp_server.disconnect()
        self.tcp_client.disconnect()

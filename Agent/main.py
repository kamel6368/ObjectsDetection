import tasks
import database
import Common.configurable_objects_factory as configurable_objects_factory
from time import sleep
from TCPServer import TCPServer
from Common.config import config
from Common.TCPConnections import TCPClient
from Common.Logger import Logger
from VideoCapturingWorker import VideoCapturingWorker


class Main:

    def __init__(self):
        self.exit = False
        self.is_registered = False
        self.tcp_server = None
        self.tcp_client = None
        self.video_capture = None
        self.logger = None
        self.is_stream_on = False
        self.database_connection = None
        self.video_recorder = None

    def start_tcp_server(self):
        receive_address = config('TCPConnection/receive_address')
        receive_port = config('TCPConnection/receive_port')
        buffer_size = config('TCPConnection/buffer_size')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_server = TCPServer(receive_address, receive_port, buffer_size, socket_timeout, self.logger, self)
        self.tcp_server.start()

    def start_tcp_client(self):
        remote_server_address = config('TCPConnection/remote_server_address')
        remote_server_port = config('TCPConnection/remote_server_port')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_client = TCPClient(remote_server_address, remote_server_port, socket_timeout, self.logger)

    def run(self):
        self.logger = configurable_objects_factory.create_logger()

        self.video_capture = VideoCapturingWorker()
        self.video_capture.start()

        self.logger.print_msg('Agent started')
        self.start_tcp_client()
        tasks.register(self.tcp_client, self.logger)

        self.start_tcp_server()

        while not self.is_registered:
            sleep(1)
        self.logger.print_msg('Agent registered')

        while not self.exit:
            # here is the place to integrate this subsystem with main decision loop
            sleep(1)
        self.logger.print_msg('Agent stopped')
        self.logger.print_msg('BYE!')



import cv2
import tasks
from time import sleep
from TCPServer import TCPServer
from Common.config import config
from Common.TCPConnections import TCPClient
from Common.Logger import Logger


class Main:

    def __init__(self):
        self.exit = False
        self.is_registered = False
        self.tcp_server = None
        self.tcp_client = None
        self.video_capture = None
        self.logger = None

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
        self.logger = Logger()

        self.logger.print_msg('Agent started')
        self.start_tcp_client()
        tasks.register(self.tcp_client)
        self.start_tcp_server()
        #self.tcp_server.start()

        while not self.is_registered:
            sleep(1)
        self.logger.print_msg('Agent registered')

        self.video_capture = cv2.VideoCapture(0)

        image = tasks.take_picture(self.video_capture)
        tasks.send_image_to_remote_server(self.tcp_client, image)

        while not self.exit:
            sleep(1)
        self.logger.print_msg('Agent stopped')
        self.logger.print_msg('BYE!')



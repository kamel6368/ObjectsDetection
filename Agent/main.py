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

    def run(self):
        logger = Logger()

        logger.print_msg('Agent started')

        receive_address = config('TCPConnection/receive_address')
        receive_port = config('TCPConnection/receive_port')
        buffer_size = config('TCPConnection/buffer_size')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_server = TCPServer(receive_address, receive_port, buffer_size, socket_timeout, logger, self)

        remote_server_address = config('TCPConnection/remote_server_address')
        remote_server_port = config('TCPConnection/remote_server_port')
        self.tcp_client = TCPClient(remote_server_address, remote_server_port, socket_timeout, logger)

        tasks.register(self.tcp_client)

        self.tcp_server.start()

        while not self.is_registered:
            sleep(1)
        logger.print_msg('Agent registered')

        self.video_capture = cv2.VideoCapture(0)

        image = tasks.take_picture(self.video_capture)
        tasks.send_image_to_remote_server(self.tcp_client, image)

        while not self.exit:
            sleep(1)
        logger.print_msg('Agent stopped')
        logger.print_msg('BYE!')



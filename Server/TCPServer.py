import cv2
import Common.image_serialization as im_ser
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main_app):
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)
        self.main_app = main_app

    def handle_message(self, command, content):
        if command == TCPCommands.IMAGE:
            image = im_ser.image_from_string(content)
        elif command == 'VIDEO':
            pass
        elif command == 'STREAM_ON_ACK':
            pass
        elif command == 'STREAM_OF_ACK':
            pass
        elif command == TCPCommands.REGISTER:
            if not self.main_app.is_connected_to_agent:
                self.main_app.tcp_client.connect()
            self.main_app.tcp_client.send(TCPCommands.REGISTER_ACK,'')

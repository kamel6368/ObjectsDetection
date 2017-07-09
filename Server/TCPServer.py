import Common.TCPConnections
import cv2
import Common.image_serialization as im_ser


class TCPServer(Common.TCPConnections.TCPServer):

    def __init__(self, address, port, buffer_size, logger):
        Common.TCPConnections.TCPServer.__init__(self, address, port, buffer_size, logger)
        #self.application_host = application_host

    def handle_message(self, command, content):
        if command == 'IMAGE':
            print content[:20]
            image = im_ser.image_from_string(content)
            cv2.imshow('dafas', image)
            cv2.waitKey(1)
        elif command == 'VIDEO':
            pass
        elif command == 'STREAM_ON_ACK':
            pass
        elif command == 'STREAM_OF_ACK':
            pass

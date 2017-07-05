import socket
from abc import ABCMeta, abstractmethod


class TCPServer:

    def __init__(self, address, port, buffer_size):
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.buffer = None
        self.exit = False

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(1)
        print 'Server started'

        conn, _ = s.accept()

        data = None
        msg_size = -1
        while not self.exit:
            chunk = conn.recv(self.buffer_size)
            if chunk:
                if data is None:
                    msg_size = int(chunk.split('|')[0])
                    data = chunk.split('|')[1]

                if len(data) + len(chunk) > msg_size:
                    data += chunk[:msg_size - len(data)]
                    self.buffer = chunk[msg_size - len(data):]
                else:
                    data += chunk

        s.close()


class TCPClient:

    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))

    def send(self, data):
        data = str(len(data)) + '|' + data
        self.socket.sendall(data)

    def close(self):
        self.socket.close()



class TCPMessageController(metaclass=ABCMeta):
    @abstractmethod
    def handle_message(self):
        pass

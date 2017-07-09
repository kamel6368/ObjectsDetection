import socket
from abc import ABCMeta, abstractmethod
from threading import Thread
import thread


class TCPServer(Thread):

    __metaclass__ = ABCMeta

    def __init__(self, address, port, buffer_size, logger):
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.buffer = None
        self.exit = False
        self.logger = logger
        Thread.__init__(self)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        s.listen(1)

        self.logger.print_msg('TCPServer started')

        conn, _ = s.accept()

        data = None
        msg_length = None

        while not self.exit:
            chunk = conn.recv(self.buffer_size)
            data, msg_length, is_complete_message = self._manage_chunk(chunk, data, msg_length)
            if is_complete_message:
                self.logger.print_msg('TCPServer received: ' + data)
                command, content = self.extract_command_content(data)
                self.handle_message(command, content)
                data = None
                msg_length = None

        s.close()
        self.logger.print_msg('TCPServer stopped')

    def _manage_chunk(self, chunk, data, msg_length):

        is_message_complete = False

        if chunk is not None:
            if data is None:
                data = ''
            data += chunk

            if msg_length is None:
                if self.buffer is not None:
                    data = self.buffer + data
                    self.buffer = None
                msg_length = int(data.split('|')[0])

            if len(data) >= msg_length:
                self.buffer = data[msg_length + 1:]
                if self.buffer == '':
                    self.buffer = None
                data = data[:msg_length]
                msg_length = None
                is_message_complete = True

        return data, msg_length, is_message_complete

    @abstractmethod
    def handle_message(self, command, content):
        raise NotImplementedError

    @staticmethod
    def extract_command_content(message):
        return message.split('|')[1], message.split('|')[2]


class TCPClient(Thread):

    def __init__(self, server_address, server_port, logger):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = None
        self.logger = logger
        Thread.__init__(self)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))

    def send(self, command, content):
        message = self._prepare_message(command, content)
        self.logger.print_msg('TCPClient send: ' + message)
        self.socket.sendall(message)

    @staticmethod
    def _prepare_message(command, content):
        data = '|' + command + '|' + content
        content_length = len(data)
        msg_length = len(str(content_length)) + content_length
        data = str(msg_length) + data
        return data

    def close(self):
        self.socket.close()

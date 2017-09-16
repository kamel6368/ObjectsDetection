import socket
from enum import Enum
from abc import ABCMeta, abstractmethod
from threading import Thread
from time import sleep


class TCPCommands:

    def __init__(self):
        pass

    REGISTER = 'REGISTER'
    REGISTER_ACK = 'REGISTER_ACK'
    IMAGE = 'IMAGE'
    IMAGE_RECEIVED = 'IMAGE_RECEIVED'
    OBJECTS = 'OBJECTS'
    STREAM_ON = 'STREAM_ON'
    STREAM_ON_ACK = 'STREAM_ON_ACK'
    STREAM_OFF = 'STREAM_OFF'
    STREAM_OFF_ACK = 'STREAM_OFF_ACK'
    SHUTDOWN = 'SHUTDOWN'
    SHUTDOWN_ACK = 'SHUTDOWN_ACK'
    SHUTDOWN_ACK_ACK = 'SHUTDOWN_ACK_ACK'
    REMOTE_SERVER_BREAK_DOWN = 'REMOTE_SERVER_BREAK_DOWN'
    VIDEO_DONE_RECORDING = 'VIDEO_DONE_RECORDING'


class StreamMode(Enum):
    EACH_FRAME = 0
    VIDEO = 1


class ClientShutdownException(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)


class InvalidMessageException(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)


class TCPServer(Thread):
    __metaclass__ = ABCMeta

    def __init__(self, address, port, buffer_size, socket_timeout, logger):
        Thread.__init__(self)
        self.name = 'TCPServer'
        self.address = address
        self.port = port
        self.buffer_size = buffer_size
        self.buffer = None
        self.logger = logger
        self.socket = None
        self.socket_timeout = socket_timeout
        self.exit = False

    def run(self):
        self._setup_socket()

        self.logger.print_msg('TCPServer/Started')

        connection = self._reconnect()

        data = None
        msg_length = None

        should_restart = False

        while not self.exit:
            if self.buffer is None:
                try:
                    chunk = connection.recv(self.buffer_size)
                except socket.timeout:
                    continue
                except socket.error:
                    self.logger.print_msg('TCPServer/Lost connection. Reconnecting...')
                    connection = self._reconnect()
                    continue

            try:
                data, msg_length, is_complete_message = self._manage_chunk(chunk, data, msg_length)
            except ClientShutdownException:
                self.logger.print_msg('TCPServer/Client shutdown. Restarting server...')
                self.disconnect()
                should_restart = True
                continue
            except InvalidMessageException:
                continue

            if is_complete_message:
                self.logger.print_msg('TCPServer/Received: ' + data)
                try:
                    command, content = self.extract_command_content(data)
                except:
                    self.logger.print_msg('TCPServer/Invalid message format. Chunk: ' + chunk)
                    continue
                self.handle_message(command, content)
                data = None
                msg_length = None

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.socket.close()
        self.logger.print_msg('TCPServer/Stopped')
        if should_restart:
            self.restart_callback()

    def disconnect(self):
        self.exit = True

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
                try:
                    msg_length = int(data.split('|')[0])
                except ValueError:
                    self.logger.print_msg('TCPServer/Invalid chunk or message: ' + chunk)
                    if chunk == '':
                        raise ClientShutdownException()
                    try:
                        splitted = data.split('|')
                        data = splitted[-4] + '|' + splitted[-3] + '|' + splitted[-2] + '|' + splitted[-1]
                        msg_length = int(splitted[-4])
                    except:
                        raise InvalidMessageException()

            if len(data) >= msg_length:
                self.buffer = data[msg_length:]
                if self.buffer == '':
                    self.buffer = None
                data = data[:msg_length - 1]
                msg_length = None
                is_message_complete = True

        return data, msg_length, is_message_complete

    def _setup_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.address, self.port))

        self.socket.listen(1)
        self.socket.settimeout(self.socket_timeout)

    def _reconnect(self):
        connection = None
        is_connected = False
        while not is_connected and not self.exit:
            try:
                connection, _ = self.socket.accept()
                is_connected = True
            except socket.timeout:
                self.logger.print_msg('TCPServer/Waiting for socket accept')
                continue

        if connection is not None:
            connection.settimeout(self.socket_timeout)
            self.logger.print_msg('TCPServer/Connected to client')
        return connection

    @abstractmethod
    def handle_message(self, command, content):
        raise NotImplementedError()

    @abstractmethod
    def restart_callback(self):
        raise NotImplementedError()

    @staticmethod
    def extract_command_content(message):
        return message.split('|')[1], message.split('|')[2]


class TCPClient:

    def __init__(self, server_address, server_port, socket_timeout, logger):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = None
        self.socket_timeout = socket_timeout
        self.logger = logger
        self.is_socket_busy = False

    def connect(self, single_try=False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.socket_timeout)
        is_connected = False
        while not is_connected:
            try:
                self.socket.connect((self.server_address, self.server_port))
                is_connected = True
                self.logger.print_msg('TCPClient/Connected to server')
            except socket.error:
                if single_try:
                    self.logger.print_msg('TCPClient/No alive connection was found')
                    break

                self.logger.print_msg('TCPClient/Waiting for connection')
                sleep(self.socket_timeout)
                continue
        return is_connected

    def send(self, command, content=''):
        message = self._prepare_message(command, content)
        self.logger.print_msg('TCPClient/Send: ' + message)
        try:
            self.socket.sendall(message)
        except socket.error:
            pass

    @staticmethod
    def _prepare_message(command, content):
        data = '|' + command + '|' + content + '|'
        data_length = len(data)
        size_flag_length = len(str(data_length))
        total_length = size_flag_length + data_length
        if len(str(total_length)) > size_flag_length:
            total_length += 1
        data = str(total_length) + data

        return data

    def disconnect(self):
        if self.socket is not None:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass
            self.socket.close()
            self.logger.print_msg('TCPClient/Stopped')

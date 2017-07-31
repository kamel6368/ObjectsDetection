import tasks
import database
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands, StreamMode
from VideoRecorder import VideoRecorder


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        self.main = main
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)

    def handle_message(self, command, content):

        if command == TCPCommands.REGISTER_ACK:
            self._register_ack_action()
        elif command == TCPCommands.OBJECTS:
            self._objects_action(content)
        elif command == TCPCommands.STREAM_ON:
            self._stream_on_action(content)
        elif command == TCPCommands.STREAM_OFF:
            self._stream_off_action()
        elif command == TCPCommands.SHUTDOWN:
            self._shutdown_action()
        elif command == TCPCommands.SHUTDOWN_ACK_ACK:
            self._shutdown_ack_ack_action()
        elif command == TCPCommands.REMOTE_SERVER_BREAK_DOWN:
            self._remote_server_break_down_action()

    def restart_callback(self):
        self.main.start_tcp_server()

    def _register_ack_action(self):
        self.main.is_registered = True
        self.main.database_connection = database.connect()

    def _objects_action(self, content):
        tasks.insert_objects_to_database(content, self.main.database_connection)
        if self.main.is_stream_on:
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)

    def _stream_on_action(self, content):
        stream_params = tasks.parse_stream_on_content(content)
        tasks.acknowledge_stream_start(self.main.tcp_client)
        self.main.is_stream_on = True
        if stream_params[0] == StreamMode.EACH_FRAME:
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)
        elif stream_params[0] == StreamMode.VIDEO:
            self.main.video_recorder = VideoRecorder(self.main, stream_params[1])
            self.main.video_recorder.start()

    def _stream_off_action(self):
        self.main.is_stream_on = False
        if self.main.video_recorder is not None:
            self.main.video_recorder.interrupt()
        tasks.acknowledge_stream_stop(self.main.tcp_client)

    def _shutdown_action(self):
        tasks.acknowledge_shutdown(self.main.tcp_client)

    def _shutdown_ack_ack_action(self):
        tasks.shutdown(self.main, self.main.tcp_server, self.main.tcp_client, self.main.video_capture)

    def _remote_server_break_down_action(self):
        self.main.is_registered = False
        tasks.register(self.main.tcp_client, self.logger)
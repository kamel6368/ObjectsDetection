import tasks
import tasksGUI
from collections import deque
from Common.serialization import image_from_string
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands, StreamMode


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)
        self.main = main

    def handle_message(self, command, content):
        if command == TCPCommands.IMAGE:
            self._image_action(content)
        elif command == TCPCommands.STREAM_ON_ACK:
            self._stream_on_ack_action()
        elif command == TCPCommands.STREAM_OFF_ACK:
            self._stream_off_ack_action()
        elif command == TCPCommands.VIDEO_DONE_RECORDING:
            self._video_done_recording_action()
        elif command == TCPCommands.REGISTER:
            self._register_action()
        elif command == TCPCommands.SHUTDOWN_ACK:
            self._shutdown_ack_action()

    def restart_callback(self):
        self.main.is_agent_alive = False
        self.main.start_tcp_server()

    def _image_action(self, content):
        image = image_from_string(content)
        if image is None:
            self.logger.print_msg('TCPServer/handle_message/invalid image')
            return
        if self.main.stream_mode == StreamMode.EACH_FRAME:
            tasks.image_action_stream_mode_each_frame(self.main, self.main.tcp_client, image)
        elif self.main.stream_mode == StreamMode.VIDEO:
            tasks.image_action_stream_mode_video(image, self.main.video_buffer, self.main.main_layout)

    def _register_action(self):
        tasks.acknowledge_agent_registration(self.main, self.main.tcp_client)
        tasksGUI.update_gui_after_registration(self.main.main_layout)

    def _shutdown_ack_action(self):
        tasks.acknowledge_agent_shutdown(self.main.tcp_client)
        self.main.is_agent_alive = False
        tasksGUI.update_gui_after_shutdown(self.main.main_layout)

    def _stream_on_ack_action(self):
        self.main.is_stream_on = True
        tasksGUI.update_gui_after_stream_on(self.main, self.main.main_layout)
        if self.main.stream_mode == StreamMode.EACH_FRAME:
            self.main.frames_buffer.clear()

    def _stream_off_ack_action(self):
        self.main.is_stream_on = False
        tasksGUI.update_gui_after_stream_off(self.main, self.main.main_layout)
        if self.main.stream_mode == StreamMode.VIDEO:
            self.main.video_buffer = deque([])


    def _video_done_recording_action(self):
        self._stream_off_ack_action()

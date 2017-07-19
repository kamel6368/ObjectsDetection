import tasks
import tasksGUI
import ImageProcessing.ObjectDetector as object_detection
from Common.serialization import image_from_string
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)
        self.main = main

    def handle_message(self, command, content):
        if command == TCPCommands.IMAGE:
            self._image_action(content)
        elif command == TCPCommands.REGISTER:
            self._register_action()
        elif command == TCPCommands.SHUTDOWN_ACK:
            self._shutdown_ack_action()
        elif command == TCPCommands.STREAM_ON_ACK:
            self._stream_on_ack_action()
        elif command == TCPCommands.STREAM_OFF_ACK:
            self._stream_off_ack_action()

    def restart_callback(self):
        self.main.is_agent_alive = False
        self.main.start_tcp_server()

    def _image_action(self, content):
        image = image_from_string(content)
        if image is None:
            self.logger.print_msg('TCPServer/handle_message/invalid image')
            return
        quantizied_image = None
        if self.main.apply_quantization:
            quantizied_image = self.main.object_detector._prepare_image_for_detection(image)

        objects = tasks.detect_objects(self.main.object_detector, image, quantizied_image)
        tasks.draw_contours_on_image(self.main.object_detector, image)
        if self.main.apply_quantization and quantizied_image is not None:
            tasks.draw_contours_on_image(self.main.object_detector, quantizied_image)
            tasksGUI.update_quantization_image(self.main.main_layout, quantizied_image)
        tasksGUI.update_raw_image(self.main.main_layout, image)
        self.main.object_detector.clear_contours()
        tasks.send_detected_object_to_agent(objects, self.main.tcp_client)

    def _register_action(self):
        tasks.acknowledge_agent_registration(self.main, self.main.tcp_client)
        tasksGUI.update_gui_after_registration(self.main.main_layout)

    def _shutdown_ack_action(self):
        tasks.acknowledge_agent_shutdown(self.main.tcp_client)
        self.main.is_agent_alive = False
        tasksGUI.update_gui_after_shutdown(self.main.main_layout)

    def _stream_on_ack_action(self):
        self.main.is_stream_on = True
        tasksGUI.update_gui_after_stream_on(self.main.main_layout)

    def _stream_off_ack_action(self):
        self.main.is_stream_on = False
        tasksGUI.update_gui_after_stream_off(self.main.main_layout)
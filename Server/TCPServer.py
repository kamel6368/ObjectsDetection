import tasks
from Common.image_serialization import image_from_string
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)
        self.main = main

    def handle_message(self, command, content):

        if command == TCPCommands.IMAGE:
            try:
                image = image_from_string(content)
            except:
                self.logger.print_msg('TCPServer/handle_message/invalid image')
                return
            tasks.show_image(self.main.main_layout, image)
            tasks.send_detected_object_to_agent(None, self.main.tcp_client)

        elif command == TCPCommands.REGISTER:
            tasks.acknowledge_agent_registration(self.main, self.main.tcp_client)
            tasks.update_gui_registration(self.main.main_layout)

        elif command == TCPCommands.SHUTDOWN_ACK:
            self.main.is_agent_alive = False
            tasks.update_gui_shutdown(self.main.main_layout)

    def restart_callback(self):
        self.main.is_agent_alive = False
        self.main.start_tcp_server()

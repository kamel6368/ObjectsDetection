import tasks
from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        self.main = main
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)

    def handle_message(self, command, content):

        if command == TCPCommands.REGISTER_ACK:
            self.main.is_registered = True
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)

        elif command == TCPCommands.OBJECTS:
            image = tasks.take_picture(self.main.video_capture)
            tasks.send_image_to_remote_server(self.main.tcp_client, image)

        elif command == TCPCommands.SHUTDOWN:
            tasks.acknowledge_shutdown(self.main.tcp_client)

        elif command == TCPCommands.SHUTDOWN_ACK_ACK:
            tasks.shutdown(self.main, self.main.tcp_server, self.main.tcp_client)

        elif command == TCPCommands.REMOTE_SERVER_BREAK_DOWN:
            self.main.is_registered = False
            tasks.register(self.main.tcp_client, self.logger)

    def restart_callback(self):
        self.main.start_tcp_server()

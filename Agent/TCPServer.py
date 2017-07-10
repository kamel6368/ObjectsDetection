from Common.TCPConnections import TCPServer as CommonTCPServer, TCPCommands


class TCPServer(CommonTCPServer):

    def __init__(self, address, port, buffer_size, socket_timeout, logger, main):
        self.main = main
        CommonTCPServer.__init__(self, address, port, buffer_size, socket_timeout, logger)

    def handle_message(self, command, content):
        if command == TCPCommands.REGISTER_ACK:
            self.main.is_registered = True
        elif command == TCPCommands.OBJECTS:
            self.main.send_image()
        elif command == TCPCommands.SHUTDOWN:
            self.main.shutdown()
        elif command == TCPCommands.REMOTE_SERVER_BREAK_DOWN:
            self.main.register()


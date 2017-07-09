from Common.Logger import Logger
from Server.TCPServer import TCPServer

address = "127.0.0.1"
port = 2465
buffer_size = 2048

logger = Logger()

TCPServer(address, port, buffer_size, logger).run()

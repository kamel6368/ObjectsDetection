from Common.config import config

from Common.TCPConnections import TCPServer

address = config('TCPServer/ip')
port = config('TCPServer/receive_port')
buffer_size = config('TCPServer/buffer_size')
TCPServer(address, port, buffer_size).run()
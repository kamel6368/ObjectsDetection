import tasks
from kivy.app import App
from kivy.lang.builder import Builder
from MainLayout import MainLayout
from Common.TCPConnections import TCPClient
from TCPServer import TCPServer
from Common.config import config
from Common.Logger import Logger


class MyApp(App):

    def __init__(self):
        self.exit = False
        self.main_layout = None
        self.tcp_server = None
        self.tcp_client = None
        self.are_agents_alive_before_startup = False
        App.__init__(self)

    def build(self):
        Builder.load_file('Layouts/main_layout.kv')
        self.main_layout = MainLayout()
        return self.main_layout

    def on_start(self):
        logger = Logger()

        receive_address = config('TCPConnection/receive_address')
        receive_port = config('TCPConnection/receive_port')
        buffer_size = config('TCPConnection/buffer_size')
        socket_timeout = config('TCPConnection/socket_timeout')
        self.tcp_server = TCPServer(receive_address, receive_port, buffer_size, socket_timeout, logger, self)

        agent_address = config('TCPConnection/agent_address')
        agent_port = config('TCPConnection/agent_port')
        self.tcp_client = TCPClient(agent_address, agent_port, socket_timeout, logger)

        tasks.try_reconnect_to_alive_agents(self, self.tcp_client)

        self.tcp_server.start()

    def on_stop(self):
        self.tcp_server.disconnect()
        self.tcp_client.disconnect()

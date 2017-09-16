from collections import deque

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

import Common.config as config
import configurable_objects_factory
import tasks
from Common.TCPConnections import StreamMode
from Server.Layouts.MainLayout import MainLayout
from Server.Layouts.SettingsLayout import SettingsLayout


class MyApp(App):

    def __init__(self):
        self.exit = False
        self.screen_manager = None
        self.main_layout = None
        self.tcp_server = None
        self.tcp_client = None
        self.is_agent_alive = False
        self.logger = None
        self.is_stream_on = False
        self.apply_quantization = False
        self.object_detector = None
        self.stream_mode = StreamMode.EACH_FRAME
        self.video_buffer = deque([])
        self.frames_buffer_size = None
        self.frames_buffer = deque([], maxlen=self.frames_buffer_size)
        self.current_frame_index = -1
        self.current_video_index = -1
        self.objects_unificator = None
        self.unified_objects = None
        App.__init__(self)

    def build(self):
        Builder.load_file('Layouts/Views/main_layout.kv')
        self.screen_manager = ScreenManager()
        self.main_layout = MainLayout(self, name='MainScreen')
        settings_layout = SettingsLayout(self.screen_manager, self, name='SettingsScreen')
        self.screen_manager.add_widget(self.main_layout)
        self.screen_manager.add_widget(settings_layout)
        return self.screen_manager

    def on_start(self):
        self._load_app_config()
        self.logger = configurable_objects_factory.create_logger()

        self.tcp_client = configurable_objects_factory.create_tcp_client(self.logger)
        tasks.try_reconnect_to_alive_agents(self, self.tcp_client)
        self.restart_tcp_server()

        self.object_detector = configurable_objects_factory.create_object_detector()
        self.objects_unificator = configurable_objects_factory.create_objects_unificator()

    def on_stop(self):
        self.tcp_server.disconnect()
        self.tcp_client.disconnect()

    def restart_tcp_server(self):
        self.tcp_server = configurable_objects_factory.create_tcp_server(self, self.logger)
        self.tcp_server.start()

    def _load_app_config(self):
        configuration = config.get_yaml()
        self.frames_buffer_size = configuration['General']['frames_buffer_size']

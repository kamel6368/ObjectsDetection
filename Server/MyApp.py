from kivy.app import App
from kivy.lang.builder import Builder
from MainLayout import MainLayout
from Common.TCPConnections import TCPServer


class TCPMessageController:



class MyApp(App):
    exit = False

    def build(self):
        Builder.load_file('Layouts/main_layout.kv')
        return MainLayout()

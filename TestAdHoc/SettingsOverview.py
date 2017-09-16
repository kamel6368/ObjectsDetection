from kivy.app import App
from kivy.lang.builder import Builder

from Server.SettingsLayout import SettingsLayout


class MyApp(App):

    def __init__(self):
        App.__init__(self)

    def build(self):
        Builder.load_file('Layouts/settings_layout.kv')
        return SettingsLayout(name='daf')

MyApp().run()

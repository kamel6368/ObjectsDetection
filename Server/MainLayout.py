import tasks
from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):

    single_image = False
    quantization_image = None

    def __init__(self, main):
        super(MainLayout, self).__init__()
        self.main = main

    def switch_single_two_images(self):
        if self.single_image:
            self.single_image = False
            self.ids.images_container.add_widget(self.quantization_image)
        else:
            self.single_image = True
            self.ids.images_container.remove_widget(self.quantization_image)

    def start_shutdown_agent_pressed(self):
        if self.main.is_agent_alive:
            tasks.shutdown_agent(self.main.tcp_client)
        else:
            tasks.start_agent()

    def update_registered_label(self):
        if self.main.is_agent_alive:
            self.ids.is_agent_registered_label.text = 'Agent is registered'
        else:
            self.ids.is_agent_registered_label.text = 'Agent is not registered'

    def update_start_shutdown_button(self):
        if self.main.is_agent_alive:
            self.ids.start_shutdown_agent_button.text = 'Shutdown agent'
        else:
            self.ids.start_shutdown_agent_button.text = 'Start agent'

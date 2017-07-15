import tasks
import tasksGUI
from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):

    single_image = False
    quantization_image = None

    def __init__(self, main):
        super(MainLayout, self).__init__()
        self.main = main

    ############################################
    # callable functions
    ############################################

    def show_quantization_image(self):
        self.ids.images_container.add_widget(self.ids.quantization_image)

    def hide_quantization_image(self):
        self.ids.images_container.remove_widget(self.ids.quantization_image)

    def update_raw_image_texture(self, texture):
        self.ids.raw_image.texture = texture

    def update_quantized_image_texture(self, texture):
        self.ids.quantization_image.texture = texture

    def enable_stream_button(self):
        self.ids.start_stop_stream_button.disabled = False

    def disable_stream_button(self):
        self.ids.start_stop_stream_button.disabled = True

    def enable_stream_mode_spinner(self):
        self.ids.stream_mode_spinner.disabled = False

    def disable_stream_mode_spinner(self):
        self.ids.stream_mode_spinner.disabled = True

    def enable_apply_quantization_checkbox(self):
        self.ids.apply_quantization_checkbox.disabled = False

    def disable_apply_quantization_checkbox(self):
        self.ids.apply_quantization_checkbox.disabled = True

    def change_registered_label_text(self, text):
        self.ids.is_agent_registered_label.text = text

    def change_start_shutdown_button_text(self, text):
        self.ids.start_shutdown_agent_button.text = text

    def change_start_stop_stream_button_text(self, text):
        self.ids.start_stop_stream_button.text = text

    ############################################
    # buttons callbacks
    ############################################

    def _single_two_images_mode_button_on_press(self):
        tasksGUI.single_two_images_mode_button_on_press(self.main, self)

    def _start_shutdown_agent_button_pressed(self):
        tasksGUI.start_shutdown_agent_button_pressed(self.main)

    def _start_stop_stream_button_on_press(self):
        tasksGUI.start_stop_stream_button_on_press(self.main)

    '''
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

    def start_stop_stream(self):
        if self.main.is_stream_on:
            tasks.stop_stream(self.main.tcp_client)
        else:
            tasks.start_stream(self.main.tcp_client)

    def update_start_stop_stream_button(self):
        if self.main.is_stream_on:
            self.ids.start_stop_stream_button.text = 'Stop stream'
        else:
            self.ids.start_stop_stream_button.text = 'Start stream'
    '''



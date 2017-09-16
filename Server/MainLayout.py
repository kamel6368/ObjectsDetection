import tasks
import tasksGUI
from kivy.uix.screenmanager import Screen


class MainLayout(Screen):

    single_image = False
    quantization_image = None

    def __init__(self, main, name=None):
        super(MainLayout, self).__init__(name=name)
        self.main = main

    ############################################
    # callable functions
    ############################################

    def show_raw_image(self):
        self.ids.quantization_image.size_hint_x = None
        self.ids.raw_image.size_hint_x = 1
        self.ids.quantization_image.width = 0

    def show_quantization_image(self):
        self.ids.raw_image.size_hint_x = None
        self.ids.quantization_image.size_hint_x = 1
        self.ids.raw_image.width = 0

    def show_both_images(self):
        self.ids.quantization_image.size_hint_x = 1
        self.ids.raw_image.size_hint_x = 1

    def update_raw_image_texture(self, texture):
        self.ids.raw_image.texture = texture

    def update_raw_image_source(self, path):
        self.ids.raw_image.source = path
        self.ids.raw_image.reload()

    def update_quantized_image_texture(self, texture):
        self.ids.quantization_image.texture = texture

    def update_quantized_image_source(self, path):
        self.ids.quantization_image.source = path
        self.ids.quantization_image.reload()

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

    def get_video_duration(self):
        return int(self.ids.video_duration_text_input.text)

    def enable_video_duration_text_input(self):
        self.ids.video_duration_text_input.disabled = False

    def disable_video_duration_text_input(self):
        self.ids.video_duration_text_input.disabled = True

    def print_on_console(self, text):
        self.ids.console.text = text

    def enable_next_frame_button(self):
        self.ids.next_frame_button.disabled = False

    def disable_next_frame_button(self):
        self.ids.next_frame_button.disabled = True

    def enable_previous_frame_button(self):
        self.ids.previous_frame_button.disabled = False

    def disable_previous_frame_button(self):
        self.ids.previous_frame_button.disabled = True

    def enable_show_only_unified_objects_checkbox(self):
        self.ids.show_only_unified_objects_checkbox.disabled = False

    def disable_show_only_unified_objects_checkbox(self):
        self.ids.show_only_unified_objects_checkbox.disabled = True

    def get_distance(self):
        return self.ids.distance_text_input.text

    def enable_distance_text_input(self):
        self.ids.distance_text_input.disabled = False

    def disable_distance_text_input(self):
        self.ids.distance_text_input.disabled = True

    def enable_settings_button(self):
        self.ids.settings_button.disabled = False

    def disable_settings_button(self):
        self.ids.settings_button.disabled = True

    def deactivate_show_only_unified_objects_checkbox(self):
        self.ids.show_only_unified_objects_checkbox.active = False

    def enable_start_shutdown_agent_button(self):
        self.ids.start_shutdown_agent_button.disabled = False

    def disable_start_shutdown_agent_button(self):
        self.ids.start_shutdown_agent_button.disabled = True

    ############################################
    # buttons callbacks
    ############################################

    def _image_mode_spinner_on_text(self):
        tasksGUI.image_mode_spinner_on_text(self.main.main_layout, self.ids.image_mode_spinner.text)

    def _start_shutdown_agent_button_pressed(self):
        tasksGUI.start_shutdown_agent_button_pressed(self.main)

    def _start_stop_stream_button_on_press(self):
        tasksGUI.start_stop_stream_button_on_press(self.main)

    def _apply_quantization_checkbox_on_state_change(self):
        tasks.change_quantization_state(self.main, self.ids.apply_quantization_checkbox.active)

    def _stream_mode_button_on_text(self):
        tasksGUI.stream_mode_button_on_text(self.main, self, self.ids.show_only_unified_objects_checkbox.active)

    def _previous_frame_button_on_press(self):
        tasksGUI.previous_frame_button_on_press(self.main, self.main.main_layout,
                                                       self.ids.show_only_unified_objects_checkbox.active)

    def _next_frame_button_on_press(self):
        tasksGUI.next_frame_button_on_press(self.main, self.main.main_layout,
                                                   self.ids.show_only_unified_objects_checkbox.active)

    def _show_only_unified_objects_checkbox_on_state_change(self):
        tasksGUI.show_only_unified_objects_checkbox_on_state_change(self.main, self.main.main_layout,
                                                                           self.ids.show_only_unified_objects_checkbox.active)

    def _settings_button_on_press(self):
        tasksGUI.show_settings_view(self.main.screen_manager)

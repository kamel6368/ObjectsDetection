import ImageProcessing.parameters_loader as img_proc_param_loader
import ObjectsUnification.parameters_loader as unif_param_loader
import Common.config as general_param_loader
import configurable_objects_factory
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class SettingsLayout(Screen):

    def __init__(self, screen_manager, main, name=None):
        self.screen_manager = screen_manager
        self.current_settings = None
        self.main = main
        super(SettingsLayout, self).__init__(name=name)
        self.ids.image_processing_settings_button.state = 'down'
        self._image_processing_button_on_press()

    ############################################
    # buttons callbacks
    ############################################

    def _back_button_on_press(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'MainScreen'

    def _image_processing_button_on_press(self):
        self.ids.objects_unification_settings_button.state = 'normal'
        self.ids.general_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = ImageProcessingSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _unification_button_on_press(self):
        self.ids.image_processing_settings_button.state = 'normal'
        self.ids.general_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = UnificationSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _general_button_on_press(self):
        self.ids.image_processing_settings_button.state = 'normal'
        self.ids.objects_unification_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = GeneralSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _save_button_on_press(self):
        try:
            if isinstance(self.current_settings, ImageProcessingSettingsLayout):
                img_proc_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                self.main.object_detector = configurable_objects_factory.create_object_detector()
            elif isinstance(self.current_settings, UnificationSettingsLayout):
                unif_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                self.main.objects_unificator = configurable_objects_factory.create_objects_unificator()
            elif isinstance(self.current_settings, GeneralSettingsLayout):
                general_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                popup = Popup(title='Please restart application', content=Label(text='To apply changes please restart application'),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
        except Exception as e:
            popup = Popup(title='Error',content=Label(text=e.message), size_hint=(None, None), size=(400, 400))
            popup.open()

    def _set_to_default_button_on_press(self):
        if isinstance(self.current_settings, ImageProcessingSettingsLayout):
            default_yaml = img_proc_param_loader.get_default_yaml()
        elif isinstance(self.current_settings, UnificationSettingsLayout):
            default_yaml = unif_param_loader.get_default_yaml()
        elif isinstance(self.current_settings, GeneralSettingsLayout):
            default_yaml = general_param_loader.get_default_yaml()
        self.current_settings.set_params_from_file(default_yaml)


class ImageProcessingSettingsLayout(ScrollView):

    def __init__(self):
        super(ImageProcessingSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = img_proc_param_loader.get_yaml()
        self.ids.horizontal_field_of_view_form.value = str(yaml['camera_info']['horizontal_field_of_view'])
        self.ids.vertical_field_of_view_form.value = str(yaml['camera_info']['vertical_field_of_view'])
        self.ids.contour_area_noise_border_form.value = str(yaml['image_processing_params']['contour_area_noise_border'])
        self.ids.min_color_bound_hsv_form.value = str(yaml['image_processing_params']['colors']['min_color_bound_hsv'])
        self.ids.max_color_bound_hsv_form.value = str(yaml['image_processing_params']['colors']['max_color_bound_hsv'])
        self.ids.red_hue_bound_form.value = str(yaml['image_processing_params']['colors']['red_hue_bound'])
        self.ids.yellow_hue_bound_form.value = str(yaml['image_processing_params']['colors']['yellow_hue_bound'])
        self.ids.green_hue_bound_form.value = str(yaml['image_processing_params']['colors']['green_hue_bound'])
        self.ids.blue_hue_bound_form.value = str(yaml['image_processing_params']['colors']['blue_hue_bound'])
        self.ids.violet_hue_bound_form.value = str(yaml['image_processing_params']['colors']['violet_hue_bound'])
        self.ids.combined_objects_detection_canny_threshold_1_form.value = \
            str(yaml['image_processing_params']['combined_objects_detection']['canny_threshold_1'])
        self.ids.combined_objects_detection_canny_threshold_2_form.value = \
            str(yaml['image_processing_params']['combined_objects_detection']['canny_threshold_2'])
        self.ids.img_prep_dark_pixels_percentage_border_form.value = \
            str(yaml['image_processing_params']['image_preparation']['dark_pixels_percentage_border'])
        self.ids.gamma_increase_form.value = \
            str(yaml['image_processing_params']['image_preparation']['gamma_increase'])
        self.ids.number_of_quantizied_colors_form.value = \
            str(yaml['image_processing_params']['image_preparation']['number_of_quantizied_colors'])
        self.ids.bright_pixel_lightness_form.value = \
            str(yaml['image_processing_params']['image_preparation']['bright_pixel_lightness'])
        self.ids.pattern_recognition_canny_threshold_1_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['canny_threshold_1'])
        self.ids.pattern_recognition_canny_threshold_2_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['canny_threshold_2'])
        self.ids.minimum_line_length_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['minimum_line_length'])
        self.ids.hough_lines_threshold_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['hough_lines_threshold'])
        self.ids.max_line_gap_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['max_line_gap'])
        self.ids.angle_epsilon_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['angle_epsilon'])
        self.ids.percentage_of_line_type_to_qualify_as_pattern_form.value = \
            str(yaml['image_processing_params']['pattern_recognition']['percentage_of_line_type_to_qualify_as_pattern'])
        self.ids.pic_merge_dark_pixels_percentage_border_form.value = \
            str(yaml['image_processing_params']['pictures_merge']['dark_pixels_percentage_border'])
        self.ids.tiny_bounds_form.value = \
            str(yaml['image_processing_params']['size_discretization']['tiny_bounds'])
        self.ids.small_bounds_form.value = \
            str(yaml['image_processing_params']['size_discretization']['small_bounds'])
        self.ids.medium_bounds_form.value = \
            str(yaml['image_processing_params']['size_discretization']['medium_bounds'])
        self.ids.big_bounds_form.value = \
            str(yaml['image_processing_params']['size_discretization']['big_bounds'])

    def create_yaml(self):
        return {
            'camera_info': {
                'horizontal_field_of_view': float(self.ids.horizontal_field_of_view_form.value),
                'vertical_field_of_view': float(self.ids.vertical_field_of_view_form.value)
            },
            'image_processing_params': {
                'contour_area_noise_border': int(self.ids.contour_area_noise_border_form.value),
                'colors': {
                    'min_color_bound_hsv': self.ids.min_color_bound_hsv_form.value,
                    'max_color_bound_hsv': self.ids.max_color_bound_hsv_form.value,
                    'red_hue_bound': self.ids.red_hue_bound_form.value,
                    'yellow_hue_bound': self.ids.yellow_hue_bound_form.value,
                    'green_hue_bound': self.ids.green_hue_bound_form.value,
                    'blue_hue_bound': self.ids.blue_hue_bound_form.value,
                    'violet_hue_bound': self.ids.violet_hue_bound_form.value
                },
                'combined_objects_detection': {
                    'canny_threshold_1': int(self.ids.combined_objects_detection_canny_threshold_1_form.value),
                    'canny_threshold_2': int(self.ids.combined_objects_detection_canny_threshold_2_form.value)
                },
                'image_preparation': {
                    'dark_pixels_percentage_border': float(self.ids.img_prep_dark_pixels_percentage_border_form.value),
                    'gamma_increase': float(self.ids.gamma_increase_form.value),
                    'number_of_quantizied_colors': int(self.ids.number_of_quantizied_colors_form.value),
                    'bright_pixel_lightness': int(self.ids.bright_pixel_lightness_form.value)
                },
                'pattern_recognition': {
                    'canny_threshold_1': int(self.ids.pattern_recognition_canny_threshold_1_form.value),
                    'canny_threshold_2': int(self.ids.pattern_recognition_canny_threshold_2_form.value),
                    'minimum_line_length': int(self.ids.minimum_line_length_form.value),
                    'hough_lines_threshold': int(self.ids.hough_lines_threshold_form.value),
                    'max_line_gap': int(self.ids.max_line_gap_form.value),
                    'angle_epsilon': int(self.ids.angle_epsilon_form.value),
                    'percentage_of_line_type_to_qualify_as_pattern':
                        float(self.ids.percentage_of_line_type_to_qualify_as_pattern_form.value)
                },
                'pictures_merge': {
                    'dark_pixels_percentage_border': float(self.ids.pic_merge_dark_pixels_percentage_border_form.value)
                },
                'size_discretization': {
                    'tiny_bounds': self.ids.tiny_bounds_form.value,
                    'small_bounds': self.ids.small_bounds_form.value,
                    'medium_bounds': self.ids.medium_bounds_form.value,
                    'big_bounds': self.ids.big_bounds_form.value
                }
            }
        }


class UnificationSettingsLayout(ScrollView):

    def __init__(self):
        super(UnificationSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = unif_param_loader.get_yaml()
        self.ids.color_weight_form.value = str(yaml['similarity']['color_weight'])
        self.ids.shape_weight_form.value = str(yaml['similarity']['shape_weight'])
        self.ids.size_weight_form.value = str(yaml['similarity']['size_weight'])
        self.ids.pattern_weight_form.value = str(yaml['similarity']['pattern_weight'])
        self.ids.symbols_weight_form.value = str(yaml['similarity']['symbols_weight'])
        self.ids.parts_weight_form.value = str(yaml['similarity']['parts_weight'])
        self.ids.min_similarity_factor_form.value = str(yaml['unification']['min_similarity_factor'])
        self.ids.work_on_copy_form.value = str(yaml['unification']['work_on_copy'])

    def create_yaml(self):
        return {
            'similarity': {
                'color_weight': float(self.ids.color_weight_form.value),
                'shape_weight': float(self.ids.shape_weight_form.value),
                'size_weight': float(self.ids.size_weight_form.value),
                'pattern_weight': float(self.ids.pattern_weight_form.value),
                'symbols_weight': float(self.ids.symbols_weight_form.value),
                'parts_weight': float(self.ids.parts_weight_form.value)
            },
            'unification': {
                'min_similarity_factor': float(self.ids.min_similarity_factor_form.value),
                'work_on_copy': True if self.ids.work_on_copy_form.value == 'True' else False
            }
        }


class GeneralSettingsLayout(ScrollView):

    def __init__(self):
        super(GeneralSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = general_param_loader.get_yaml()
        self.ids.agent_address_form.value = str(yaml['TCPConnection']['agent_address'])
        self.ids.agent_port_form.value = str(yaml['TCPConnection']['agent_port'])
        self.ids.receive_address_form.value = str(yaml['TCPConnection']['receive_address'])
        self.ids.receive_port_form.value = str(yaml['TCPConnection']['receive_port'])
        self.ids.buffer_size_form.value = str(yaml['TCPConnection']['buffer_size'])
        self.ids.socket_timeout_form.value = str(yaml['TCPConnection']['socket_timeout'])

    def create_yaml(self):
        return {
            'TCPConnection': {
                'agent_address': self.ids.agent_address_form.value,
                'agent_port': int(self.ids.agent_port_form.value),
                'receive_address': self.ids.receive_address_form.value,
                'receive_port': int(self.ids.receive_port_form.value),
                'buffer_size': int(self.ids.buffer_size_form.value),
                'socket_timeout': float(self.ids.socket_timeout_form.value)
            }
        }

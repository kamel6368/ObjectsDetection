import ImageProcessing.parameters_loader as img_proc_param_loader
from kivy.uix.scrollview import ScrollView


class ImageProcessingSettingsLayout(ScrollView):

    def __init__(self):
        super(ImageProcessingSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = img_proc_param_loader.get_yaml()
        self.ids.horizontal_field_of_view_form.value = str(yaml['camera_info']['horizontal_field_of_view'])
        self.ids.vertical_field_of_view_form.value = str(yaml['camera_info']['vertical_field_of_view'])
        self.ids.object_contour_area_noise_border_form.value = \
            str(yaml['image_processing_params']['general']['object_contour_area_noise_border'])
        self.ids.symbol_contour_area_noise_border_form.value = \
            str(yaml['image_processing_params']['general']['symbol_contour_area_noise_border'])
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
        self.ids.bright_pixel_lightness_adjust_gamma_form.value = \
            str(yaml['image_processing_params']['image_preparation']['image_preparation_bright_pixel_lightness_adjust_gamma'])
        self.ids.bright_pixel_lightness_remove_background_form.value = \
            str(yaml['image_processing_params']['image_preparation']['image_preparation_bright_pixel_lightness_remove_background'])
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
                'general': {
                    'object_contour_area_noise_border': int(self.ids.object_contour_area_noise_border_form.value),
                    'symbol_contour_area_noise_border': int(self.ids.symbol_contour_area_noise_border_form.value)
                },
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
                    'image_preparation_bright_pixel_lightness_adjust_gamma': int(self.ids.bright_pixel_lightness_adjust_gamma_form.value),
                    'image_preparation_bright_pixel_lightness_remove_background': int(self.ids.bright_pixel_lightness_remove_background_form.value),
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

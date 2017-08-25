import yaml
from ast import literal_eval


def _file_path():
    return 'Resources/image_processing_params.yaml'


def _default_file_path():
    return 'Resources/image_processing_params_default.yaml'


def load_all_from_file(object_detector):

    common_operator = object_detector.common_operator
    pattern_recognizer = object_detector.pattern_recognizer
    picture_transformer = object_detector.picture_transformer
    size_detector = object_detector.size_detector

    size_detector.horizontal_fov = \
        yaml_lookup('camera_info/horizontal_field_of_view')
    size_detector.vertical_fov = \
        yaml_lookup('camera_info/vertical_field_of_view')
    common_operator.contour_area_noise_border = \
        yaml_lookup('image_processing_params/contour_area_noise_border')
    common_operator.min_color_bound_hsv = \
        literal_eval(yaml_lookup('image_processing_params/colors/min_color_bound_hsv'))
    common_operator.max_color_bound_hsv = \
        literal_eval(yaml_lookup('image_processing_params/colors/max_color_bound_hsv'))
    common_operator.red_bound = \
        literal_eval(yaml_lookup('image_processing_params/colors/red_hue_bound'))
    common_operator.yellow_bound = \
        literal_eval(yaml_lookup('image_processing_params/colors/yellow_hue_bound'))
    common_operator.green_bound = \
        literal_eval(yaml_lookup('image_processing_params/colors/green_hue_bound'))
    common_operator.blue_bound = \
        literal_eval(yaml_lookup('image_processing_params/colors/blue_hue_bound'))
    common_operator.violet_bound = \
        literal_eval(yaml_lookup('image_processing_params/colors/violet_hue_bound'))
    object_detector.combined_objects_detection_canny_threshold_1 = \
        yaml_lookup('image_processing_params/combined_objects_detection/canny_threshold_1')
    object_detector.combined_objects_detection_canny_threshold_2 = \
        yaml_lookup('image_processing_params/combined_objects_detection/canny_threshold_2')
    object_detector.image_preparation_dark_pixels_percentage_border = \
        yaml_lookup('image_processing_params/image_preparation/dark_pixels_percentage_border')
    object_detector.image_preparation_gamma_increase = \
        yaml_lookup('image_processing_params/image_preparation/gamma_increase')
    object_detector.image_preparation_number_of_quantizied_colors = \
        yaml_lookup('image_processing_params/image_preparation/number_of_quantizied_colors')
    object_detector.image_preparation_bright_pixel_lightness = \
        yaml_lookup('image_processing_params/image_preparation/bright_pixel_lightness')
    pattern_recognizer.canny_threshold_1 = \
        yaml_lookup('image_processing_params/pattern_recognition/canny_threshold_1')
    pattern_recognizer.canny_threshold_2 = \
        yaml_lookup('image_processing_params/pattern_recognition/canny_threshold_2')
    pattern_recognizer.minimum_line_length = \
        yaml_lookup('image_processing_params/pattern_recognition/minimum_line_length')
    pattern_recognizer.hough_lines_threshold = \
        yaml_lookup('image_processing_params/pattern_recognition/hough_lines_threshold')
    pattern_recognizer.max_line_gap = \
        yaml_lookup('image_processing_params/pattern_recognition/max_line_gap')
    pattern_recognizer.angle_epsilon = \
        yaml_lookup('image_processing_params/pattern_recognition/angle_epsilon')
    pattern_recognizer.percentage_of_line_type_to_qualify_as_pattern = \
        yaml_lookup('image_processing_params/pattern_recognition/percentage_of_line_type_to_qualify_as_pattern')
    picture_transformer.pictures_merge_dark_pixels_percentage_border = \
        yaml_lookup('image_processing_params/pictures_merge/dark_pixels_percentage_border')
    size_detector.tiny_bounds = \
        literal_eval(yaml_lookup('image_processing_params/size_discretization/tiny_bounds'))
    size_detector.small_bounds = \
        literal_eval(yaml_lookup('image_processing_params/size_discretization/small_bounds'))
    size_detector.medium_bounds = \
        literal_eval(yaml_lookup('image_processing_params/size_discretization/medium_bounds'))
    size_detector.big_bounds = \
        literal_eval(yaml_lookup('image_processing_params/size_discretization/big_bounds'))


def yaml_lookup(path, return_str=False):
    stream = open(_file_path(), 'r')
    dict = yaml.load(stream)
    keys = path.split('/')
    for key in keys:
        val = dict[key]
        dict = val
    if return_str:
        return str(val)
    return val


def get_yaml():
    with open(_file_path()) as stream:
        return yaml.load(stream)


def get_default_yaml():
    with open(_default_file_path()) as stream:
        return yaml.load(stream)


def save_yaml_to_file(yaml_to_save):
    with open(_file_path(), 'w') as stream:
        yaml.dump(yaml_to_save, stream, default_flow_style=False)

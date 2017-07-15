import yaml
from ast import literal_eval


def load_all_ad_hoc(object_detector,
                    horizontal_field_of_view,
                    vertical_field_of_view,
                    contour_area_noise_border,
                    min_color_bound_hsv,
                    max_color_bound_hsv,
                    red_hue_bound,
                    yellow_hue_bound,
                    green_hue_bound,
                    blue_hue_bound,
                    violet_hue_bound,
                    combined_objects_detection_canny_threshold_1,
                    combined_objects_detection_canny_threshold_2,
                    image_preparation_dark_pixels_percentage_border,
                    image_preparation_gamma_increase,
                    image_preparation_number_of_quantizied_colors,
                    pattern_recognition_canny_threshold_1,
                    pattern_recognition_canny_threshold_2,
                    pattern_recognition_minimum_line_length,
                    pattern_recognition_hough_lines_threshold,
                    pattern_recognition_max_line_gap,
                    pattern_recognition_angle_epsilon,
                    pattern_recognition_percentage_of_line_type_to_qualify_as_pattern,
                    pictures_merge_dark_pixels_percentage_border,
                    tiny_bounds,
                    small_bounds,
                    medium_bounds,
                    big_bounds):

    common_operator = object_detector.common_operator
    pattern_recognizer = object_detector.pattern_recognizer
    picture_transformer = object_detector.picture_transformer
    size_detector = object_detector.size_detector

    size_detector.horizontal_fov = horizontal_field_of_view
    size_detector.vertical_fov = vertical_field_of_view
    common_operator.contour_area_noise_border = contour_area_noise_border
    common_operator.min_color_bound_hsv = min_color_bound_hsv
    common_operator.max_color_bound_hsv = max_color_bound_hsv
    common_operator.red_bound = red_hue_bound
    common_operator.yellow_bound = yellow_hue_bound
    common_operator.green_bound = green_hue_bound
    common_operator.blue_bound = blue_hue_bound
    common_operator.violet_bound = violet_hue_bound
    object_detector.combined_objects_detection_canny_threshold_1 = combined_objects_detection_canny_threshold_1
    object_detector.combined_objects_detection_canny_threshold_2 = combined_objects_detection_canny_threshold_2
    object_detector.image_preparation_dark_pixels_percentage_border = image_preparation_dark_pixels_percentage_border
    object_detector.image_preparation_gamma_increase = image_preparation_gamma_increase
    object_detector.image_preparation_number_of_quantizied_colors = image_preparation_number_of_quantizied_colors
    pattern_recognizer.canny_threshold_1 = pattern_recognition_canny_threshold_1
    pattern_recognizer.canny_threshold_2 = pattern_recognition_canny_threshold_2
    pattern_recognizer.minimum_line_length = pattern_recognition_minimum_line_length
    pattern_recognizer.hough_lines_threshold = pattern_recognition_hough_lines_threshold
    pattern_recognizer.max_line_gap = pattern_recognition_max_line_gap
    pattern_recognizer.angle_epsilon = pattern_recognition_angle_epsilon
    pattern_recognizer.percentage_of_line_type_to_qualify_as_pattern = \
        pattern_recognition_percentage_of_line_type_to_qualify_as_pattern
    picture_transformer.pictures_merge_dark_pixels_percentage_border = pictures_merge_dark_pixels_percentage_border
    size_detector.tiny_bounds = tiny_bounds
    size_detector.small_bounds = small_bounds
    size_detector.medium_bounds = medium_bounds
    size_detector.big_bounds = big_bounds


def load_all_from_file(object_detector):

    common_operator = object_detector.common_operator
    pattern_recognizer = object_detector.pattern_recognizer
    picture_transformer = object_detector.picture_transformer
    size_detector = object_detector.size_detector

    size_detector.horizontal_fov = \
        _yaml_lookup('camera_info/horizontal_field_of_view')
    size_detector.vertical_fov = \
        _yaml_lookup('camera_info/vertical_field_of_view')
    common_operator.contour_area_noise_border = \
        _yaml_lookup('image_processing_params/contour_area_noise_border')
    common_operator.min_color_bound_hsv = \
        literal_eval(_yaml_lookup('image_processing_params/colors/min_color_bound_hsv'))
    common_operator.max_color_bound_hsv = \
        literal_eval(_yaml_lookup('image_processing_params/colors/max_color_bound_hsv'))
    common_operator.red_bound = \
        literal_eval(_yaml_lookup('image_processing_params/colors/red_hue_bound'))
    common_operator.yellow_bound = \
        literal_eval(_yaml_lookup('image_processing_params/colors/yellow_hue_bound'))
    common_operator.green_bound = \
        literal_eval(_yaml_lookup('image_processing_params/colors/green_hue_bound'))
    common_operator.blue_bound = \
        literal_eval(_yaml_lookup('image_processing_params/colors/blue_hue_bound'))
    common_operator.violet_bound = \
        literal_eval(_yaml_lookup('image_processing_params/colors/violet_hue_bound'))
    object_detector.combined_objects_detection_canny_threshold_1 = \
        _yaml_lookup('image_processing_params/combined_objects_detection/canny_threshold_1')
    object_detector.combined_objects_detection_canny_threshold_2 = \
        _yaml_lookup('image_processing_params/combined_objects_detection/canny_threshold_2')
    object_detector.image_preparation_dark_pixels_percentage_border = \
        _yaml_lookup('image_processing_params/image_preparation/dark_pixels_percentage_border')
    object_detector.image_preparation_gamma_increase = \
        _yaml_lookup('image_processing_params/image_preparation/gamma_increase')
    object_detector.image_preparation_number_of_quantizied_colors = \
        _yaml_lookup('image_processing_params/image_preparation/number_of_quantizied_colors')
    pattern_recognizer.canny_threshold_1 = \
        _yaml_lookup('image_processing_params/pattern_recognition/canny_threshold_1')
    pattern_recognizer.canny_threshold_2 = \
        _yaml_lookup('image_processing_params/pattern_recognition/canny_threshold_2')
    pattern_recognizer.minimum_line_length = \
        _yaml_lookup('image_processing_params/pattern_recognition/minimum_line_length')
    pattern_recognizer.hough_lines_threshold = \
        _yaml_lookup('image_processing_params/pattern_recognition/hough_lines_threshold')
    pattern_recognizer.max_line_gap = \
        _yaml_lookup('image_processing_params/pattern_recognition/max_line_gap')
    pattern_recognizer.angle_epsilon = \
        _yaml_lookup('image_processing_params/pattern_recognition/angle_epsilon')
    pattern_recognizer.percentage_of_line_type_to_qualify_as_pattern = \
        _yaml_lookup('image_processing_params/pattern_recognition/percentage_of_line_type_to_qualify_as_pattern')
    picture_transformer.pictures_merge_dark_pixels_percentage_border = \
        _yaml_lookup('image_processing_params/pictures_merge/dark_pixels_percentage_border')
    size_detector.tiny_bounds = \
        _yaml_lookup('image_processing_params/size_discretization/tiny_bounds')
    size_detector.small_bounds = \
        _yaml_lookup('image_processing_params/size_discretization/small_bounds')
    size_detector.medium_bounds = \
        _yaml_lookup('image_processing_params/size_discretization/medium_bounds')
    size_detector.big_bounds = \
        _yaml_lookup('image_processing_params/size_discretization/big_bounds')


def _yaml_lookup(path):
    stream = open('Resources/image_processing_params.yaml', 'r')
    dict = yaml.load(stream)
    keys = path.split('/')
    for key in keys:
        val = dict[key]
        dict = val
    return val

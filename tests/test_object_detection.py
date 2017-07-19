import cv2
from unittest import TestCase
from ImageProcessing.ObjectDetector import ObjectDetector
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject
from DataModel.Symbol import Symbol
from DataModel.enums import Color, Shape, Pattern
from ImageProcessing.parameters_loader import load_all_from_file


class ObjectDetectorTest(TestCase):

    def setUp(self):
        self.detector = ObjectDetector()
        load_all_from_file(self.detector)

    def test_detect_object_red_rectangle_with_green_triangle(self):
        frame = cv2.imread('Resources/images/obj_det_red_rectangle.bmp')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)

        obj = None
        for x in objects_list:
            if x.color is Color.RED and x.shape is Shape.RECTANGLE and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.GREEN and x.symbols[0].shape is Shape.TRIANGLE:
                obj = x
                break
        assert obj is not None

    def test_detect_object_blue_square_with_red_triangle_and_green_parallelogram(self):
        frame = cv2.imread('Resources/images/obj_det_blue_rectangle.bmp')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)
        obj = None
        for x in objects_list:
            if x.color is Color.BLUE and x.shape is Shape.SQUARE and len(x.symbols) is 2:
                matched_symbols = 0
                for symbol in x.symbols:
                    if (symbol.color is Color.RED and self._is_triangle(symbol.shape)) or \
                            (symbol.color is Color.GREEN and symbol.shape is Shape.SQUARE):
                        matched_symbols += 1
                if matched_symbols is 2:
                    obj = x
                    break
        assert obj is not None

    def test_detect_object_blue_pentagon_with_red_parallelogram(self):
        frame = cv2.imread('Resources/images/obj_det_blue_pentagon.bmp')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)

        obj = None
        for x in objects_list:
            if x.color is Color.BLUE and x.shape is Shape.PENTAGON and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.RED and x.symbols[0].shape is Shape.SQUARE:
                obj = x
                break
        assert obj is not None

    def test_detect_object_green_triangle_with_blue_rectangle(self):
        frame = cv2.imread('Resources/images/obj_det_green_triangle.bmp')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)

        obj = None
        for x in objects_list:
            if x.color is Color.GREEN and self._is_triangle(x.shape) and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.BLUE and x.symbols[0].shape is Shape.RECTANGLE:
                obj = x
                break
        assert obj is not None

    def test_detect_object_all_objects(self):
        frame = cv2.imread('Resources/images/obj_det_all.jpg')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)

        obj = None
        for x in objects_list:
            if x.color is Color.RED and x.shape is Shape.RECTANGLE and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.GREEN and x.symbols[0].shape is Shape.TRIANGLE:
                obj = x
                break
        assert obj is not None

        obj = None
        for x in objects_list:
            if x.color is Color.BLUE and x.shape is Shape.SQUARE and len(x.symbols) is 2:
                matched_symbols = 0
                for symbol in x.symbols:
                    if (symbol.color is Color.RED and self._is_triangle(symbol.shape)) or \
                            (symbol.color is Color.GREEN and symbol.shape is Shape.SQUARE):
                        matched_symbols += 1
                if matched_symbols is 2:
                    obj = x
                    break
        assert obj is not None

        obj = None
        for x in objects_list:
            if x.color is Color.BLUE and x.shape is Shape.PENTAGON and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.RED and x.symbols[0].shape is Shape.SQUARE:
                obj = x
                break
        assert obj is not None

        obj = None
        for x in objects_list:
            if x.color is Color.GREEN and self._is_triangle(x.shape) and len(x.symbols) is 1 and \
                            x.symbols[0].color is Color.BLUE and x.symbols[0].shape is Shape.RECTANGLE:
                obj = x
                break
        assert obj is not None

    def test_detect_object_green_triangle_pattern_horizontal_lines(self):
        frame = cv2.imread('Resources/images/obj_det_green_triangle_pattern_hor_lines.bmp')
        objects_list = self.detector.detect_objects(frame, real_distance=None, auto_contour_clear=False,
                                               prepare_image_before_detection=False)

        assert len(objects_list) is 1
        obj = objects_list[0]
        assert obj.color is Color.GREEN
        assert obj.pattern is Pattern.HORIZONTAL_LINES
        assert obj.pattern_color is Color.RED

    def test_find_combined_objects_single_object(self):
        img = cv2.imread('Resources/images/comb_obj_single.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 1

        correct_part_count = 0
        if isinstance(objects_list[0], CombinedObject) and len(objects_list[0].parts) is 3:
            for part in objects_list[0].parts:
                if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 0) or \
                   (part.color is Color.RED and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                   (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 0):
                    correct_part_count += 1

        assert correct_part_count is 3

    def test_find_combined_objects_two_objects(self):
        img = cv2.imread('Resources/images/comb_obj_two.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 2
        assert isinstance(objects_list[0], CombinedObject)
        assert isinstance(objects_list[1], CombinedObject)

        correct_part_count_for_first = 0
        correct_part_count_for_second = 0

        for x in objects_list:
            if len(x.parts) is 3:
                for part in x.parts:
                    if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.RED and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 0):
                        correct_part_count_for_first += 1
            elif len(x.parts) is 4:
                for part in x.parts:
                    if (part.color is Color.YELLOW and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.BLUE and part.shape is Shape.PENTAGON and len(part.symbols) is 0) or \
                       (part.color is Color.RED and part.shape is Shape.HEXAGON and len(part.symbols) is 0):
                        correct_part_count_for_second += 1

        assert correct_part_count_for_first is 3
        assert correct_part_count_for_second is 4

    def test_find_combined_objects_single_object_with_symbols(self):
        img = cv2.imread('Resources/images/comb_obj_symbol.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 1

        correct_part_count = 0
        if isinstance(objects_list[0], CombinedObject) and len(objects_list[0].parts) is 3:
            for part in objects_list[0].parts:
                if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 1 and
                        part.symbols[0].color is Color.YELLOW and part.symbols[0].shape is Shape.PENTAGON) or \
                   (part.color is Color.RED and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                   (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 1 and
                        part.symbols[0].color is Color.BLUE and part.symbols[0].shape is Shape.RECTANGLE):
                    correct_part_count += 1

        assert correct_part_count is 3

    def test_find_combined_objects_two_objects_with_symbols(self):
        img = cv2.imread('Resources/images/comb_obj_two_symbols.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 2
        assert isinstance(objects_list[0], CombinedObject)
        assert isinstance(objects_list[1], CombinedObject)

        correct_part_count_for_first = 0
        corret_part_count_for_second = 0

        for object in objects_list:
            if len(object.parts) is 3:
                for part in object.parts:
                    if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 1 and
                                part.symbols[0].color is Color.YELLOW and part.symbols[0].shape is Shape.PENTAGON) or \
                       (part.color is Color.RED and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 1 and
                            part.symbols[0].color is Color.BLUE and part.symbols[0].shape is Shape.RECTANGLE):
                        correct_part_count_for_first += 1
            elif len(object.parts) is 4:
                for part in object.parts:
                    if (part.color is Color.YELLOW and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.BLUE and part.shape is Shape.PENTAGON and len(part.symbols) is 1 and
                            part.symbols[0].color is Color.VIOLET and part.symbols[0].shape is Shape.TRIANGLE) or \
                       (part.color is Color.RED and part.shape is Shape.HEXAGON and len(part.symbols) is 1 and
                            part.symbols[0].color is Color.BLUE and part.symbols[0].shape is Shape.RECTANGLE):
                        corret_part_count_for_second += 1

        assert correct_part_count_for_first is 3
        assert corret_part_count_for_second is 4


    def test_find_combined_objects_single_object_symbol_and_pattern(self):
        img = cv2.imread('Resources/images/comb_obj_single_symbol_and_pattern.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 1
        assert isinstance(objects_list[0], CombinedObject)
        assert len(objects_list[0].parts) is 3

        correct_part_count = 0

        for object in objects_list:
            for part in object.parts:
                if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 1 and part.pattern is Pattern.NONE and
                        part.symbols[0].color is Color.YELLOW and part.symbols[0].shape is Shape.PENTAGON) or \
                    (part.color is Color.RED and self._is_triangle(part.shape) and len(part.symbols) is 0) or \
                    (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 0 and
                        part.pattern is Pattern.HORIZONTAL_LINES and part.pattern_color is Color.RED):
                        correct_part_count += 1

        assert correct_part_count is 3

    def test_find_combined_objects_two_objects_with_symbols_and_pattern(self):
        img = cv2.imread('Resources/images/comb_obj_two_symbol_and_pattern.bmp')
        objects_list = self.detector.detect_objects(img, real_distance=None, prepare_image_before_detection=False)

        assert len(objects_list) is 2
        assert isinstance(objects_list[0], CombinedObject)
        assert isinstance(objects_list[1], CombinedObject)

        correct_part_count_for_first = 0
        corret_part_count_for_second = 0

        for object in objects_list:
            if len(object.parts) is 3:
                for part in object.parts:
                    if (part.color is Color.GREEN and part.shape is Shape.RECTANGLE and len(part.symbols) is 1 and
                                part.symbols[0].color is Color.BLUE and part.symbols[0].shape is Shape.PENTAGON) or \
                       (part.color is Color.RED and self._is_triangle(part.shape) and len(part.symbols) is 0) or \
                       (part.color is Color.YELLOW and part.shape is Shape.PENTAGON and len(part.symbols) is 0 and
                            part.pattern is Pattern.VERTICAL_LINES and part.pattern_color is Color.BLUE):
                        correct_part_count_for_first += 1
            elif len(object.parts) is 4:
                for part in object.parts:
                    if (part.color is Color.YELLOW and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 0) or \
                       (part.color is Color.YELLOW and part.shape is Shape.EQUILATERAL_TRIANGLE and len(part.symbols) is 1 and
                            part.symbols[0].shape is Shape.RECTANGLE and part.symbols[0].color is Color.RED) or \
                       (part.color is Color.BLUE and part.shape is Shape.PENTAGON and len(part.symbols) is 0 and
                            part.pattern is Pattern.LEFT_INCLINED_LINES and part.pattern_color is Color.RED) or \
                       (part.color is Color.RED and part.shape is Shape.HEXAGON and len(part.symbols) is 0):
                        corret_part_count_for_second += 1

        assert correct_part_count_for_first is 3
        assert corret_part_count_for_second is 4

    '''
    There is no 100% guarantee that triangle will be detected as three point curve.
    Sometimes it is recognized as 4 points curve but it is still ok, because extra point is very close to
    one of other three main points. That gives chance to reduce this extra point using RDP algorithm - shape_detection in
    our case.
    '''

    def test__detect_basic_objects_contours_blue_pentagon(self):
        frame = cv2.imread('Resources/images/obj_det_blue_pentagon.bmp')
        contours = self.detector._detect_basic_objects_contours(Color.BLUE, frame)
        assert len(contours) is 1
        assert contours[0].shape[0] is 5 or contours[0].shape[0] is 6

    def test__detect_basic_objects_contours_red_square(self):
        frame = cv2.imread('Resources/images/obj_det_blue_pentagon.bmp')
        contours = self.detector._detect_basic_objects_contours(Color.RED, frame)
        assert len(contours) is 1
        assert contours[0].shape[0] is 4 or contours[0].shape[0] is 5

    def test__detect_basic_objects_contours_green_triangle(self):
        frame = cv2.imread('Resources/images/obj_det_green_triangle.bmp')
        contours = self.detector._detect_basic_objects_contours(Color.GREEN, frame)
        assert len(contours) is 1
        assert contours[0].shape[0] is 3 or contours[0].shape is 4

    def test__detect_basic_objects_contours_blue_rectangle(self):
        frame = cv2.imread('Resources/images/obj_det_green_triangle.bmp')
        contours = self.detector._detect_basic_objects_contours(Color.BLUE, frame)
        assert len(contours) is 1
        assert contours[0].shape[0] is 3 or contours[0].shape[0] is 4

    def _is_triangle(self, shape):
        return shape is Shape.TRIANGLE or shape is Shape.EQUILATERAL_TRIANGLE or shape is Shape.ISOSCELES_TRIANGLE

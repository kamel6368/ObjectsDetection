import cv2
from unittest import TestCase
from ImageProcessing.ObjectDetector import ObjectDetector
from ImageProcessing.parameters_loader import load_all_from_file
from DataModel.enums import Pattern, Color


class PatternRecognizerTest(TestCase):

    def setUp(self):
        self.object_detector = ObjectDetector()
        load_all_from_file(self.object_detector)
        self.pattern_recognizer = self.object_detector.pattern_recognizer

    def test_find_pattern_vertical_lines(self):
        img = cv2.imread('Resources/images/pattern_rec_vert_lines.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.VERTICAL_LINES
        assert pattern_color is Color.GREEN

    def test_find_pattern_horizontal_lines(self):
        img = cv2.imread('Resources/images/pattern_rec_hor_lines.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.HORIZONTAL_LINES
        assert pattern_color is Color.RED

    def test_find_pattern_left_inclined_lines(self):
        img = cv2.imread('Resources/images/pattern_rec_left_inc_lines.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.LEFT_INCLINED_LINES
        assert pattern_color is Color.RED

    def test_find_pattern_right_inclined_lines(self):
        img = cv2.imread('Resources/images/pattern_rec_right_inc_lines.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.RIGHT_INCLINED_LINES
        assert pattern_color is Color.YELLOW

    def test_find_pattern_grid(self):
        img = cv2.imread('Resources/images/pattern_rec_grid.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.GRID
        assert pattern_color is Color.RED

    def test_find_pattern_inclined_grid(self):
        img = cv2.imread('Resources/images/pattern_rec_inc_grid.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.INCLINED_GRID
        assert pattern_color is Color.GREEN

    def test_find_pattern_no_pattern(self):
        img = cv2.imread('Resources/images/pattern_rec_no_pattern.bmp')
        pattern, pattern_color = self.pattern_recognizer.find_pattern(img)
        assert pattern is Pattern.NONE
        assert pattern_color is Color.NONE

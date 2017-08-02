import ObjectsUnification.similarity as similarity
from unittest import TestCase
from DataModel.enums import Color, Shape, Size, Pattern
from DataModel.Symbol import Symbol
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject


# Those should be treated as smoke tests.


class SimilarityTest(TestCase):
    def test_color_similarity(self):
        color_similarity = similarity.calculate_colors_similarity(Color.RED, Color.RED)
        self.assertEqual(1, color_similarity)
        color_similarity = similarity.calculate_colors_similarity(Color.RED, Color.VIOLET)
        self.assertTrue(0 < color_similarity < 1)
        color_similarity = similarity.calculate_colors_similarity(Color.NONE, Color.RED)
        self.assertEqual(0, color_similarity)
        color_similarity = similarity.calculate_colors_similarity(Color.NONE, Color.NONE)
        self.assertEqual(1, color_similarity)
        color_similarity = similarity.calculate_colors_similarity(Color.RED, Color.GREEN)
        self.assertEqual(0, color_similarity)

    def test_shape_similarity(self):
        shape_similarity = similarity.calculate_shapes_similarity(Shape.SQUARE, Shape.SQUARE)
        self.assertEqual(1, shape_similarity)
        shape_similarity = similarity.calculate_shapes_similarity(Shape.TRIANGLE, Shape.EQUILATERAL_TRIANGLE)
        self.assertTrue(0 < shape_similarity < 1)
        shape_similarity = similarity.calculate_shapes_similarity(Shape.INVALID, Shape.RECTANGLE)
        self.assertEqual(0, shape_similarity)
        shape_similarity = similarity.calculate_shapes_similarity(Shape.INVALID, Shape.INVALID)
        self.assertEqual(1, shape_similarity)
        shape_similarity = similarity.calculate_shapes_similarity(Shape.RECTANGLE, Shape.ELLIPSE)
        self.assertEqual(0, shape_similarity)

    def test_size_similarity(self):
        size_similarity = similarity.calculate_size_similarity(Size.TINY, Size.TINY)
        self.assertEqual(1, size_similarity)
        size_similarity = similarity.calculate_size_similarity(Size.TINY, Size.SMALL)
        self.assertTrue(0 < size_similarity < 1)
        size_similarity = similarity.calculate_size_similarity(Size.NONE, Size.LARGE)
        self.assertEqual(0, size_similarity)
        size_similarity = similarity.calculate_size_similarity(Size.NONE, Size.NONE)
        self.assertEqual(1, size_similarity)
        size_similarity = similarity.calculate_size_similarity(Size.TINY, Size.LARGE)
        self.assertEqual(0, size_similarity)

    def test_pattern_similarity(self):
        pattern_similarity = similarity.calculate_pattern_similarity(Pattern.RIGHT_INCLINED_LINES,
                                                                     Pattern.RIGHT_INCLINED_LINES)
        self.assertEqual(1, pattern_similarity)
        pattern_similarity = similarity.calculate_pattern_similarity(Pattern.RIGHT_INCLINED_LINES,
                                                                     Pattern.HORIZONTAL_LINES)
        self.assertTrue(0 < pattern_similarity < 1)
        pattern_similarity = similarity.calculate_pattern_similarity(Pattern.NONE, Pattern.HORIZONTAL_LINES)
        self.assertEqual(0, pattern_similarity)
        pattern_similarity = similarity.calculate_pattern_similarity(Pattern.NONE, Pattern.NONE)
        self.assertEqual(1, pattern_similarity)
        pattern_similarity = similarity.calculate_pattern_similarity(Pattern.VERTICAL_LINES, Pattern.HORIZONTAL_LINES)
        self.assertEqual(0, pattern_similarity)

    def test_symbol_to_symbol_similarity(self):
        symbol_1 = Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.GREEN)
        symbol_2 = Symbol(Shape.RECTANGLE, Size.BIG, Size.TINY, Color.RED)
        symbol_similarity = similarity.calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight=1.0,
                                                                             shape_weight=1.0, size_weight=1.0)
        self.assertEqual(symbol_similarity, 0.5)

        symbol_1 = Symbol(Shape.RECTANGLE, Size.LARGE, Size.MEDIUM, Color.GREEN)
        symbol_2 = Symbol(Shape.RECTANGLE, Size.BIG, Size.TINY, Color.RED)
        symbol_similarity = similarity.calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight=1.0,
                                                                             shape_weight=1.0, size_weight=1.0)
        self.assertLess(symbol_similarity, 0.5)

        symbol_1 = Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.GREEN)
        symbol_2 = Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.RED)
        symbol_similarity = similarity.calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight=1.0,
                                                                             shape_weight=1.0, size_weight=1.0)
        self.assertGreater(symbol_similarity, 0.5)

        symbol_1 = Symbol(Shape.CIRCLE, Size.TINY, Size.MEDIUM, Color.GREEN)
        symbol_2 = Symbol(Shape.RECTANGLE, Size.BIG, Size.TINY, Color.RED)
        symbol_similarity = similarity.calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight=1.0,
                                                                             shape_weight=1.0, size_weight=1.0)
        self.assertEqual(symbol_similarity, 0.0)

        symbol_1 = Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.RED)
        symbol_2 = Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.RED)
        symbol_similarity = similarity.calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight=1.0,
                                                                             shape_weight=1.0, size_weight=1.0)
        self.assertEqual(symbol_similarity, 1.0)

    def test_list_of_symbols_similarity(self):
        symbols_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        symbols_2 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET)]
        symbol_similarity = similarity.calculate_list_similarity(symbols_1, symbols_2, color_weight=1.0,
                                                                 shape_weight=1.0, size_weight=1.0, pattern_weight=1.0,
                                                                 symbols_weight=1.0)
        self.assertAlmostEqual(0.6667, symbol_similarity, places=3)

    def test_simple_object_to_simple_object_similarity(self):
        symbols_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        object_1 = SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW, Pattern.HORIZONTAL_LINES,
                                Color.GREEN, symbols_1)

        symbols_2 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET)]
        object_2 = SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW, Pattern.HORIZONTAL_LINES,
                                Color.GREEN, symbols_2)
        objects_similarity = similarity.calculate_simple_object_to_simple_object_similarity(object_1, object_2,
                                                                                            color_weight=1.0,
                                                                                            shape_weight=1.0,
                                                                                            size_weight=1.0,
                                                                                            pattern_weight=1.0,
                                                                                            symbols_weight=1.0)
        self.assertGreater(objects_similarity, 0.5)

        symbols_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        object_1 = SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW, Pattern.HORIZONTAL_LINES,
                                Color.GREEN, symbols_1)

        symbols_2 = [Symbol(Shape.TRIANGLE, Size.TINY, Size.TINY, Color.YELLOW)]
        object_2 = SimpleObject(Shape.HEXAGON, Size.LARGE, Size.LARGE, Color.RED, Pattern.NONE,
                                Color.NONE, symbols_2)
        objects_similarity = similarity.calculate_simple_object_to_simple_object_similarity(object_1, object_2,
                                                                                            color_weight=1.0,
                                                                                            shape_weight=1.0,
                                                                                            size_weight=1.0,
                                                                                            pattern_weight=1.0,
                                                                                            symbols_weight=1.0)
        self.assertLess(objects_similarity, 0.5)

        symbols_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        object_1 = SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW, Pattern.HORIZONTAL_LINES,
                                Color.GREEN, symbols_1)

        symbols_2 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        object_2 = SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW, Pattern.HORIZONTAL_LINES,
                                Color.GREEN, symbols_2)
        objects_similarity = similarity.calculate_simple_object_to_simple_object_similarity(object_1, object_2,
                                                                                            color_weight=1.0,
                                                                                            shape_weight=1.0,
                                                                                            size_weight=1.0,
                                                                                            pattern_weight=1.0,
                                                                                            symbols_weight=1.0)
        self.assertEqual(objects_similarity, 1)

    def test_simple_object_to_combined_object_similarity(self):
        simple_object = SimpleObject(Shape.ELLIPSE, Size.LARGE, Size.LARGE, Color.RED, Pattern.HORIZONTAL_LINES,
                                     Color.GREEN, [])
        combined_object = CombinedObject(Shape.ELLIPSE, Size.LARGE, Size.LARGE, [simple_object])
        objects_similarity = similarity.calculate_simple_object_to_combined_object_similarity(simple_object,
                                                                                              combined_object)
        self.assertEqual(0, objects_similarity)

    @staticmethod
    def test_combined_object_to_combined_object_similarity():
        symbols_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                     Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                     Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        simple_objects_1 = [SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW,
                                         Pattern.HORIZONTAL_LINES, Color.GREEN, symbols_1)]
        combined_object_1 = CombinedObject(Shape.PENTAGON, Size.MEDIUM, Size.MEDIUM, simple_objects_1)

        symbols_2_1 = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                       Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET)]
        symbols_2_2 = [Symbol(Shape.CIRCLE, Size.TINY, Size.MEDIUM, Color.GREEN),
                       Symbol(Shape.RECTANGLE, Size.BIG, Size.TINY, Color.RED)]
        simple_objects_2 = [SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW,
                                         Pattern.HORIZONTAL_LINES, Color.GREEN, symbols_2_1),
                            SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW,
                                         Pattern.HORIZONTAL_LINES, Color.GREEN, symbols_2_2)]

        combined_object_2 = CombinedObject(Shape.HEXAGON, Size.MEDIUM, Size.MEDIUM, simple_objects_2)

        similarity.calculate_combine_object_to_combined_object_similarity(combined_object_1,
                                                                          combined_object_2,
                                                                          color_weight=1.0,
                                                                          shape_weight=1.0,
                                                                          size_weight=1.0,
                                                                          pattern_weight=1.0,
                                                                          parts_weight=1.0,
                                                                          symbols_weight=1.0)

    def test_calculate_objects_similarity_should_return_according_to_objects_type(self):
        symbols = [Symbol(Shape.HEPTAGON, Size.LARGE, Size.LARGE, Color.GREEN),
                   Symbol(Shape.CIRCLE, Size.SMALL, Size.TINY, Color.VIOLET),
                   Symbol(Shape.KITE, Size.MEDIUM, Size.MEDIUM, Color.RED)]
        simple_objects = [SimpleObject(Shape.RECTANGLE, Size.MEDIUM, Size.SMALL, Color.YELLOW,
                                       Pattern.HORIZONTAL_LINES, Color.GREEN, symbols)]
        combined_object = CombinedObject(Shape.PENTAGON, Size.MEDIUM, Size.MEDIUM, simple_objects)
        simple_object = simple_objects[0]

        result = similarity.calculate_objects_similarity(simple_object,
                                                         simple_object,
                                                         color_weight=1.0,
                                                         shape_weight=1.0,
                                                         size_weight=1.0,
                                                         pattern_weight=1.0,
                                                         parts_weight=1.0,
                                                         symbols_weight=1.0)
        self.assertEqual(1.0, result)

        result = similarity.calculate_objects_similarity(combined_object,
                                                         combined_object,
                                                         color_weight=1.0,
                                                         shape_weight=1.0,
                                                         size_weight=1.0,
                                                         pattern_weight=1.0,
                                                         parts_weight=1.0,
                                                         symbols_weight=1.0)
        self.assertEqual(1.0, result)

        result = similarity.calculate_objects_similarity(simple_object,
                                                         combined_object,
                                                         color_weight=1.0,
                                                         shape_weight=1.0,
                                                         size_weight=1.0,
                                                         pattern_weight=1.0,
                                                         parts_weight=1.0,
                                                         symbols_weight=1.0)
        self.assertEqual(0, result)

        result = similarity.calculate_objects_similarity(combined_object,
                                                         simple_object,
                                                         color_weight=1.0,
                                                         shape_weight=1.0,
                                                         size_weight=1.0,
                                                         pattern_weight=1.0,
                                                         parts_weight=1.0,
                                                         symbols_weight=1.0)
        self.assertEqual(0, result)

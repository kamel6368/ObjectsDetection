import unittest
import json
from DataModel.enums import Color, Pattern, Shape, Size
from DataModel.Symbol import Symbol
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject


class SymbolTest(unittest.TestCase):

    def setUp(self):
        self.symbol = Symbol(Shape.ELLIPSE, Size.LARGE, Size.MEDIUM, Color.GREEN)

    def test_serialize_should_return_json_id_none(self):
        result_dict = self.symbol.to_dictionary()
        self.assertEqual('Symbol', result_dict['class'])
        self.assertEqual(Shape.ELLIPSE.value, result_dict['shape'])
        self.assertEqual(Size.LARGE.value, result_dict['width'])
        self.assertEqual(Size.MEDIUM.value, result_dict['height'])
        self.assertEqual(Color.GREEN.value, result_dict['color'])
        self.assertEqual(None, result_dict['id'])

    def test_to_dictionary_should_return_json_id_not_none(self):
        self.symbol.id = 3
        result_dict = self.symbol.to_dictionary()
        self.assertEqual('Symbol', result_dict['class'])
        self.assertEqual(Shape.ELLIPSE.value, result_dict['shape'])
        self.assertEqual(Size.LARGE.value, result_dict['width'])
        self.assertEqual(Size.MEDIUM.value, result_dict['height'])
        self.assertEqual(Color.GREEN.value, result_dict['color'])
        self.assertEqual(3, result_dict['id'])

    def test_deserialize_should_return_symbol_object_id_none(self):
        symbol_json = {"class":"Symbol", "shape":1, "width":2, "height":3, "color":4, "id":None}
        result_symbol = Symbol.from_dictionary(symbol_json)
        self.assertEqual(Shape(1), result_symbol.shape)
        self.assertEqual(Size(2), result_symbol.width)
        self.assertEqual(Size(3), result_symbol.height)
        self.assertEqual(Color(4), result_symbol.color)
        self.assertEqual(None, result_symbol.id)

    def test_deserialize_should_return_symbol_object_id_not_none(self):
        symbol_json = {"class":"Symbol", "shape":1, "width":2, "height":3, "color":4, "id":5}
        result_symbol = Symbol.from_dictionary(symbol_json)
        self.assertEqual(Shape(1), result_symbol.shape)
        self.assertEqual(Size(2), result_symbol.width)
        self.assertEqual(Size(3), result_symbol.height)
        self.assertEqual(Color(4), result_symbol.color)
        self.assertEqual(5, result_symbol.id)

    def test_deserialize_should_raise_exception_invalid_json(self):
        symbol_json = {"class":"Symbol", "shape":1, "width":2, "height":3, "color":4}
        self.assertRaises(Exception, Symbol.from_dictionary, symbol_json)


class SimpleObjectTest(unittest.TestCase):

    def setUp(self):
        symbols = [
            Symbol(Shape.ELLIPSE, Size.LARGE, Size.MEDIUM, Color.GREEN),
            Symbol(Shape.CIRCLE, Size.BIG, Size.SMALL, Color.BLUE),
            Symbol(Shape.HEXAGON, Size.MEDIUM, Size.MEDIUM, Color.YELLOW)
        ]
        self.simple_object = SimpleObject(Shape.HEPTAGON, Size.MEDIUM, Size.BIG, Color.YELLOW,
                                          Pattern.HORIZONTAL_LINES, Color.GREEN, symbols)

    def test_to_dictionary_should_return_json_id_none(self):
        result_dict = self.simple_object.to_dictionary()
        self.assertEqual('SimpleObject', result_dict['class'])
        self.assertEqual(Shape.HEPTAGON.value, result_dict['shape'])
        self.assertEqual(Size.MEDIUM.value, result_dict['width'])
        self.assertEqual(Size.BIG.value, result_dict['height'])
        self.assertEqual(Color.YELLOW.value, result_dict['color'])
        self.assertEqual(Pattern.HORIZONTAL_LINES.value, result_dict['pattern'])
        self.assertEqual(Color.GREEN.value, result_dict['pattern_color'])
        self.assertEqual(None, result_dict['id'])
        symbols_dict = result_dict['symbols']
        self.assertEqual('Symbol', symbols_dict[0]['class'])
        self.assertEqual(Shape.ELLIPSE.value, symbols_dict[0]['shape'])
        self.assertEqual(Size.LARGE.value, symbols_dict[0]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[0]['height'])
        self.assertEqual(Color.GREEN.value, symbols_dict[0]['color'])
        self.assertEqual(None, symbols_dict[0]['id'])

        self.assertEqual('Symbol', symbols_dict[1]['class'])
        self.assertEqual(Shape.CIRCLE.value, symbols_dict[1]['shape'])
        self.assertEqual(Size.BIG.value, symbols_dict[1]['width'])
        self.assertEqual(Size.SMALL.value, symbols_dict[1]['height'])
        self.assertEqual(Color.BLUE.value, symbols_dict[1]['color'])
        self.assertEqual(None, symbols_dict[1]['id'])

        self.assertEqual('Symbol', symbols_dict[2]['class'])
        self.assertEqual(Shape.HEXAGON.value, symbols_dict[2]['shape'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[2]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[2]['height'])
        self.assertEqual(Color.YELLOW.value, symbols_dict[2]['color'])
        self.assertEqual(None, symbols_dict[2]['id'])

    def test_to_dictionary_should_return_json_id_not_none(self):
        self.simple_object.id = 999
        result_dict = self.simple_object.to_dictionary()
        self.assertEqual('SimpleObject', result_dict['class'])
        self.assertEqual(Shape.HEPTAGON.value, result_dict['shape'])
        self.assertEqual(Size.MEDIUM.value, result_dict['width'])
        self.assertEqual(Size.BIG.value, result_dict['height'])
        self.assertEqual(Color.YELLOW.value, result_dict['color'])
        self.assertEqual(Pattern.HORIZONTAL_LINES.value, result_dict['pattern'])
        self.assertEqual(Color.GREEN.value, result_dict['pattern_color'])
        self.assertEqual(999, result_dict['id'])
        symbols_dict = result_dict['symbols']
        self.assertEqual('Symbol', symbols_dict[0]['class'])
        self.assertEqual(Shape.ELLIPSE.value, symbols_dict[0]['shape'])
        self.assertEqual(Size.LARGE.value, symbols_dict[0]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[0]['height'])
        self.assertEqual(Color.GREEN.value, symbols_dict[0]['color'])
        self.assertEqual(None, symbols_dict[0]['id'])

        self.assertEqual('Symbol', symbols_dict[1]['class'])
        self.assertEqual(Shape.CIRCLE.value, symbols_dict[1]['shape'])
        self.assertEqual(Size.BIG.value, symbols_dict[1]['width'])
        self.assertEqual(Size.SMALL.value, symbols_dict[1]['height'])
        self.assertEqual(Color.BLUE.value, symbols_dict[1]['color'])
        self.assertEqual(None, symbols_dict[1]['id'])

        self.assertEqual('Symbol', symbols_dict[2]['class'])
        self.assertEqual(Shape.HEXAGON.value, symbols_dict[2]['shape'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[2]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[2]['height'])
        self.assertEqual(Color.YELLOW.value, symbols_dict[2]['color'])
        self.assertEqual(None, symbols_dict[2]['id'])

    def test_from_dictionary_should_return_symbol_object_id_none(self):
        simple_object_json = {"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":5,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":5,"height":4, "color":3, "id":None},{"class":"Symbol", "shape":2,"width":1, "height":0, "color":1, "id":None}]}
        result_simple_object = SimpleObject.from_dictionary(simple_object_json)
        self.assertEqual(Shape(1), result_simple_object.shape)
        self.assertEqual(Size(2), result_simple_object.width)
        self.assertEqual(Size(3), result_simple_object.height)
        self.assertEqual(Color(4), result_simple_object.color)
        self.assertEqual(Pattern(5), result_simple_object.pattern)
        self.assertEqual(Color(5), result_simple_object.pattern_color)
        self.assertEqual(None, result_simple_object.id)

        self.assertEqual(Shape(1), result_simple_object.symbols[0].shape)
        self.assertEqual(Size(2), result_simple_object.symbols[0].width)
        self.assertEqual(Size(3), result_simple_object.symbols[0].height)
        self.assertEqual(Color(4), result_simple_object.symbols[0].color)
        self.assertEqual(None, result_simple_object.symbols[0].id)

        self.assertEqual(Shape(6), result_simple_object.symbols[1].shape)
        self.assertEqual(Size(5), result_simple_object.symbols[1].width)
        self.assertEqual(Size(4), result_simple_object.symbols[1].height)
        self.assertEqual(Color(3), result_simple_object.symbols[1].color)
        self.assertEqual(None, result_simple_object.symbols[1].id)

        self.assertEqual(Shape(2), result_simple_object.symbols[2].shape)
        self.assertEqual(Size(1), result_simple_object.symbols[2].width)
        self.assertEqual(Size(0), result_simple_object.symbols[2].height)
        self.assertEqual(Color(1), result_simple_object.symbols[2].color)
        self.assertEqual(None, result_simple_object.symbols[2].id)

    def test_from_dictionary_should_return_symbol_object_id_not_none(self):
        simple_object_json = {"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":5,"id":5,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":0,"height":1, "color":2, "id":None},{"class":"Symbol", "shape":3,"width":4, "height":5, "color":1, "id":None}]}
        result_simple_object = SimpleObject.from_dictionary(simple_object_json)
        self.assertEqual(Shape(1), result_simple_object.shape)
        self.assertEqual(Size(2), result_simple_object.width)
        self.assertEqual(Size(3), result_simple_object.height)
        self.assertEqual(Color(4), result_simple_object.color)
        self.assertEqual(Pattern(5), result_simple_object.pattern)
        self.assertEqual(Color(5), result_simple_object.pattern_color)
        self.assertEqual(5, result_simple_object.id)

        self.assertEqual(Shape(1), result_simple_object.symbols[0].shape)
        self.assertEqual(Size(2), result_simple_object.symbols[0].width)
        self.assertEqual(Size(3), result_simple_object.symbols[0].height)
        self.assertEqual(Color(4), result_simple_object.symbols[0].color)
        self.assertEqual(None, result_simple_object.symbols[0].id)

        self.assertEqual(Shape(6), result_simple_object.symbols[1].shape)
        self.assertEqual(Size(0), result_simple_object.symbols[1].width)
        self.assertEqual(Size(1), result_simple_object.symbols[1].height)
        self.assertEqual(Color(2), result_simple_object.symbols[1].color)
        self.assertEqual(None, result_simple_object.symbols[1].id)

        self.assertEqual(Shape(3), result_simple_object.symbols[2].shape)
        self.assertEqual(Size(4), result_simple_object.symbols[2].width)
        self.assertEqual(Size(5), result_simple_object.symbols[2].height)
        self.assertEqual(Color(1), result_simple_object.symbols[2].color)
        self.assertEqual(None, result_simple_object.symbols[2].id)

    def test_from_dictionary_should_raise_exception_invalid_json(self):
        simple_object_json = '{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"id":5,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":None},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":None}]}'
        self.assertRaises(Exception, Symbol.from_dictionary, simple_object_json)


class CombinedObjectTest(unittest.TestCase):

    def setUp(self):
        symbols = [
            Symbol(Shape.ELLIPSE, Size.LARGE, Size.MEDIUM, Color.GREEN)
        ]
        simple_objects = [
            SimpleObject(Shape.HEPTAGON, Size.MEDIUM, Size.BIG, Color.YELLOW,
                         Pattern.HORIZONTAL_LINES, Color.GREEN, symbols)
        ]
        self.combined_object = CombinedObject(Shape.RECTANGLE, Size.MEDIUM, Size.LARGE, simple_objects)

    def test_to_dictionary_should_return_json_id_none(self):
        result_dict = self.combined_object.to_dictionary()
        self.assertEqual('CombinedObject', result_dict['class'])
        self.assertEqual(Shape.RECTANGLE.value, result_dict['shape'])
        self.assertEqual(Size.MEDIUM.value, result_dict['width'])
        self.assertEqual(Size.LARGE.value, result_dict['height'])
        self.assertEqual(None, result_dict['id'])

        simple_objects = result_dict['parts']
        self.assertEqual('SimpleObject', simple_objects[0]['class'])
        self.assertEqual(Shape.HEPTAGON.value, simple_objects[0]['shape'])
        self.assertEqual(Size.MEDIUM.value, simple_objects[0]['width'])
        self.assertEqual(Size.BIG.value, simple_objects[0]['height'])
        self.assertEqual(Color.YELLOW.value, simple_objects[0]['color'])
        self.assertEqual(Pattern.HORIZONTAL_LINES.value, simple_objects[0]['pattern'])
        self.assertEqual(Color.GREEN.value, simple_objects[0]['pattern_color'])
        self.assertEqual(None, simple_objects[0]['id'])
        symbols_dict = simple_objects[0]['symbols']
        self.assertEqual('Symbol', symbols_dict[0]['class'])
        self.assertEqual(Shape.ELLIPSE.value, symbols_dict[0]['shape'])
        self.assertEqual(Size.LARGE.value, symbols_dict[0]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[0]['height'])
        self.assertEqual(Color.GREEN.value, symbols_dict[0]['color'])
        self.assertEqual(None, symbols_dict[0]['id'])

    def test_to_dictionary_should_return_json_id_not_none(self):
        self.combined_object.id = 999
        result_dict = self.combined_object.to_dictionary()
        self.assertEqual('CombinedObject', result_dict['class'])
        self.assertEqual(Shape.RECTANGLE.value, result_dict['shape'])
        self.assertEqual(Size.MEDIUM.value, result_dict['width'])
        self.assertEqual(Size.LARGE.value, result_dict['height'])
        self.assertEqual(999, result_dict['id'])

        simple_objects = result_dict['parts']
        self.assertEqual('SimpleObject', simple_objects[0]['class'])
        self.assertEqual(Shape.HEPTAGON.value, simple_objects[0]['shape'])
        self.assertEqual(Size.MEDIUM.value, simple_objects[0]['width'])
        self.assertEqual(Size.BIG.value, simple_objects[0]['height'])
        self.assertEqual(Color.YELLOW.value, simple_objects[0]['color'])
        self.assertEqual(Pattern.HORIZONTAL_LINES.value, simple_objects[0]['pattern'])
        self.assertEqual(Color.GREEN.value, simple_objects[0]['pattern_color'])
        self.assertEqual(None, simple_objects[0]['id'])

        symbols_dict = simple_objects[0]['symbols']
        self.assertEqual('Symbol', symbols_dict[0]['class'])
        self.assertEqual(Shape.ELLIPSE.value, symbols_dict[0]['shape'])
        self.assertEqual(Size.LARGE.value, symbols_dict[0]['width'])
        self.assertEqual(Size.MEDIUM.value, symbols_dict[0]['height'])
        self.assertEqual(Color.GREEN.value, symbols_dict[0]['color'])
        self.assertEqual(None, symbols_dict[0]['id'])

    def test_from_dictionary_should_return_symbol_object_id_none(self):
        combined_object_json = {"class":"CombinedObject","shape":1,"width":2,"height":3,"id":None,"parts":[{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":5,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":1,"height":2, "color":3, "id":None},{"class":"Symbol", "shape":4,"width":5, "height":1, "color":1, "id":None}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":2,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":1, "width":2,"height":3, "color":4, "id":None},{"class":"Symbol", "shape":5,"width":1, "height":1, "color":2, "id":None}]}]}
        result_combined_object = CombinedObject.from_dictionary(combined_object_json)
        self.assertEqual(Shape(1), result_combined_object.shape)
        self.assertEqual(Size(2), result_combined_object.width)
        self.assertEqual(Size(3), result_combined_object.height)
        self.assertEqual(None, result_combined_object.id)

        self.assertEqual(Shape(1), result_combined_object.parts[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[0].color)
        self.assertEqual(Pattern(5), result_combined_object.parts[0].pattern)
        self.assertEqual(Color(5), result_combined_object.parts[0].pattern_color)
        self.assertEqual(None, result_combined_object.parts[0].id)

        self.assertEqual(Shape(1), result_combined_object.parts[0].symbols[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[0].symbols[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[0].symbols[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[0].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[0].id)

        self.assertEqual(Shape(6), result_combined_object.parts[0].symbols[1].shape)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[1].width)
        self.assertEqual(Size(2), result_combined_object.parts[0].symbols[1].height)
        self.assertEqual(Color(3), result_combined_object.parts[0].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[1].id)

        self.assertEqual(Shape(4), result_combined_object.parts[0].symbols[2].shape)
        self.assertEqual(Size(5), result_combined_object.parts[0].symbols[2].width)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[2].height)
        self.assertEqual(Color(1), result_combined_object.parts[0].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[2].id)

        self.assertEqual(Shape(1), result_combined_object.parts[1].shape)
        self.assertEqual(Size(2), result_combined_object.parts[1].width)
        self.assertEqual(Size(3), result_combined_object.parts[1].height)
        self.assertEqual(Color(4), result_combined_object.parts[1].color)
        self.assertEqual(Pattern(5), result_combined_object.parts[1].pattern)
        self.assertEqual(Color(2), result_combined_object.parts[1].pattern_color)
        self.assertEqual(None, result_combined_object.parts[1].id)

        self.assertEqual(Shape(1), result_combined_object.parts[1].symbols[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[1].symbols[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[1].symbols[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[1].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[0].id)

        self.assertEqual(Shape(1), result_combined_object.parts[1].symbols[1].shape)
        self.assertEqual(Size(2), result_combined_object.parts[1].symbols[1].width)
        self.assertEqual(Size(3), result_combined_object.parts[1].symbols[1].height)
        self.assertEqual(Color(4), result_combined_object.parts[1].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[1].id)

        self.assertEqual(Shape(5), result_combined_object.parts[1].symbols[2].shape)
        self.assertEqual(Size(1), result_combined_object.parts[1].symbols[2].width)
        self.assertEqual(Size(1), result_combined_object.parts[1].symbols[2].height)
        self.assertEqual(Color(2), result_combined_object.parts[1].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[2].id)

    def test_from_dictionary_should_return_symbol_object_id_not_none(self):
        combined_object_json = {"class":"CombinedObject","shape":1,"width":2,"height":3,"id":999,"parts":[{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":2,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":1,"height":2, "color":3, "id":None},{"class":"Symbol", "shape":4,"width":5, "height":1, "color":2, "id":None}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":2,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":1,"height":2, "color":3, "id":None},{"class":"Symbol", "shape":4,"width":5, "height":1, "color":2, "id":None}]}]}
        result_combined_object = CombinedObject.from_dictionary(combined_object_json)
        self.assertEqual(Shape(1), result_combined_object.shape)
        self.assertEqual(Size(2), result_combined_object.width)
        self.assertEqual(Size(3), result_combined_object.height)
        self.assertEqual(999, result_combined_object.id)

        self.assertEqual(Shape(1), result_combined_object.parts[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[0].color)
        self.assertEqual(Pattern(5), result_combined_object.parts[0].pattern)
        self.assertEqual(Color(2), result_combined_object.parts[0].pattern_color)
        self.assertEqual(None, result_combined_object.parts[0].id)

        self.assertEqual(Shape(1), result_combined_object.parts[0].symbols[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[0].symbols[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[0].symbols[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[0].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[0].id)

        self.assertEqual(Shape(6), result_combined_object.parts[0].symbols[1].shape)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[1].width)
        self.assertEqual(Size(2), result_combined_object.parts[0].symbols[1].height)
        self.assertEqual(Color(3), result_combined_object.parts[0].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[1].id)

        self.assertEqual(Shape(4), result_combined_object.parts[0].symbols[2].shape)
        self.assertEqual(Size(5), result_combined_object.parts[0].symbols[2].width)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[2].height)
        self.assertEqual(Color(2), result_combined_object.parts[0].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[2].id)

        self.assertEqual(Shape(1), result_combined_object.parts[1].shape)
        self.assertEqual(Size(2), result_combined_object.parts[1].width)
        self.assertEqual(Size(3), result_combined_object.parts[1].height)
        self.assertEqual(Color(4), result_combined_object.parts[1].color)
        self.assertEqual(Pattern(5), result_combined_object.parts[1].pattern)
        self.assertEqual(Color(2), result_combined_object.parts[1].pattern_color)
        self.assertEqual(None, result_combined_object.parts[1].id)

        self.assertEqual(Shape(1), result_combined_object.parts[1].symbols[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[1].symbols[0].width)
        self.assertEqual(Size(3), result_combined_object.parts[1].symbols[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[1].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[0].id)

        self.assertEqual(Shape(6), result_combined_object.parts[1].symbols[1].shape)
        self.assertEqual(Size(1), result_combined_object.parts[1].symbols[1].width)
        self.assertEqual(Size(2), result_combined_object.parts[1].symbols[1].height)
        self.assertEqual(Color(3), result_combined_object.parts[1].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[1].id)

        self.assertEqual(Shape(4), result_combined_object.parts[1].symbols[2].shape)
        self.assertEqual(Size(5), result_combined_object.parts[1].symbols[2].width)
        self.assertEqual(Size(1), result_combined_object.parts[1].symbols[2].height)
        self.assertEqual(Color(2), result_combined_object.parts[1].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[2].id)

    def test_from_dictionary_should_raise_exception_invalid_json(self):
        combined_object_json = '{"class":"CombinedObject","shape":1,"width":2,"height":3,"id":999,"parts":[{"class":"SimpleObject","width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":None},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":None}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":None,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":None},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":None},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":None}]}]}'
        self.assertRaises(Exception, Symbol.from_dictionary, combined_object_json)
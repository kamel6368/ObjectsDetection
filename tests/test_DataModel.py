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
        result = self.symbol.serialize()
        result_dict = json.loads(result)
        self.assertEqual('Symbol', result_dict['class'])
        self.assertEqual(Shape.ELLIPSE.value, result_dict['shape'])
        self.assertEqual(Size.LARGE.value, result_dict['width'])
        self.assertEqual(Size.MEDIUM.value, result_dict['height'])
        self.assertEqual(Color.GREEN.value, result_dict['color'])
        self.assertEqual(None, result_dict['id'])

    def test_serialize_should_return_json_id_not_none(self):
        self.symbol.id = 3
        result = self.symbol.serialize()
        result_dict = json.loads(result)
        self.assertEqual('Symbol', result_dict['class'])
        self.assertEqual(Shape.ELLIPSE.value, result_dict['shape'])
        self.assertEqual(Size.LARGE.value, result_dict['width'])
        self.assertEqual(Size.MEDIUM.value, result_dict['height'])
        self.assertEqual(Color.GREEN.value, result_dict['color'])
        self.assertEqual(3, result_dict['id'])

    def test_deserialize_should_return_symbol_object_id_none(self):
        symbol_json = '{"class":"Symbol", "shape":1, "width":2, "height":3, "color":4, "id":null}'
        result_symbol = Symbol.deserialize(symbol_json)
        self.assertEqual(1, result_symbol.shape)
        self.assertEqual(2, result_symbol.width)
        self.assertEqual(3, result_symbol.height)
        self.assertEqual(4, result_symbol.color)
        self.assertEqual(None, result_symbol.id)

    def test_deserialize_should_return_symbol_object_id_not_none(self):
        symbol_json = '{"class":"Symbol", "shape":1, "width":2, "height":3, "color":4, "id":5}'
        result_symbol = Symbol.deserialize(symbol_json)
        self.assertEqual(1, result_symbol.shape)
        self.assertEqual(2, result_symbol.width)
        self.assertEqual(3, result_symbol.height)
        self.assertEqual(4, result_symbol.color)
        self.assertEqual(5, result_symbol.id)

    def test_deserialize_should_raise_exception_invalid_json(self):
        symbol_json = '{"class":"Symbol", "shape":1, "width":2, "height":3, "color":4}'
        self.assertRaises(Exception, Symbol.deserialize, symbol_json)


class SimpleObjectTest(unittest.TestCase):

    def setUp(self):
        symbols = [
            Symbol(Shape.ELLIPSE, Size.LARGE, Size.MEDIUM, Color.GREEN),
            Symbol(Shape.CIRCLE, Size.BIG, Size.SMALL, Color.BLUE),
            Symbol(Shape.HEXAGON, Size.MEDIUM, Size.MEDIUM, Color.YELLOW)
        ]
        self.simple_object = SimpleObject(Shape.HEPTAGON, Size.MEDIUM, Size.BIG, Color.YELLOW,
                                          Pattern.HORIZONTAL_LINES, Color.GREEN, symbols)

    def test_serialize_should_return_json_id_none(self):
        result = self.simple_object.serialize()
        result_dict = json.loads(result)
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

    def test_serialize_should_return_json_id_not_none(self):
        self.simple_object.id = 999
        result = self.simple_object.serialize()
        result_dict = json.loads(result)
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

    def test_deserialize_should_return_symbol_object_id_none(self):
        simple_object_json = '{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}'
        result_simple_object = SimpleObject.deserialize(simple_object_json)
        self.assertEqual(1, result_simple_object.shape)
        self.assertEqual(2, result_simple_object.width)
        self.assertEqual(3, result_simple_object.height)
        self.assertEqual(4, result_simple_object.color)
        self.assertEqual(5, result_simple_object.pattern)
        self.assertEqual(6, result_simple_object.pattern_color)
        self.assertEqual(None, result_simple_object.id)

        self.assertEqual(1, result_simple_object.symbols[0].shape)
        self.assertEqual(2, result_simple_object.symbols[0].width)
        self.assertEqual(3, result_simple_object.symbols[0].height)
        self.assertEqual(4, result_simple_object.symbols[0].color)
        self.assertEqual(None, result_simple_object.symbols[0].id)

        self.assertEqual(6, result_simple_object.symbols[1].shape)
        self.assertEqual(7, result_simple_object.symbols[1].width)
        self.assertEqual(8, result_simple_object.symbols[1].height)
        self.assertEqual(9, result_simple_object.symbols[1].color)
        self.assertEqual(None, result_simple_object.symbols[1].id)

        self.assertEqual(13, result_simple_object.symbols[2].shape)
        self.assertEqual(12, result_simple_object.symbols[2].width)
        self.assertEqual(11, result_simple_object.symbols[2].height)
        self.assertEqual(10, result_simple_object.symbols[2].color)
        self.assertEqual(None, result_simple_object.symbols[2].id)

    def test_deserialize_should_return_symbol_object_id_not_none(self):
        simple_object_json = '{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":5,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}'
        result_simple_object = SimpleObject.deserialize(simple_object_json)
        self.assertEqual(1, result_simple_object.shape)
        self.assertEqual(2, result_simple_object.width)
        self.assertEqual(3, result_simple_object.height)
        self.assertEqual(4, result_simple_object.color)
        self.assertEqual(5, result_simple_object.pattern)
        self.assertEqual(6, result_simple_object.pattern_color)
        self.assertEqual(5, result_simple_object.id)

        self.assertEqual(1, result_simple_object.symbols[0].shape)
        self.assertEqual(2, result_simple_object.symbols[0].width)
        self.assertEqual(3, result_simple_object.symbols[0].height)
        self.assertEqual(4, result_simple_object.symbols[0].color)
        self.assertEqual(None, result_simple_object.symbols[0].id)

        self.assertEqual(6, result_simple_object.symbols[1].shape)
        self.assertEqual(7, result_simple_object.symbols[1].width)
        self.assertEqual(8, result_simple_object.symbols[1].height)
        self.assertEqual(9, result_simple_object.symbols[1].color)
        self.assertEqual(None, result_simple_object.symbols[1].id)

        self.assertEqual(13, result_simple_object.symbols[2].shape)
        self.assertEqual(12, result_simple_object.symbols[2].width)
        self.assertEqual(11, result_simple_object.symbols[2].height)
        self.assertEqual(10, result_simple_object.symbols[2].color)
        self.assertEqual(None, result_simple_object.symbols[2].id)

    def test_deserialize_should_raise_exception_invalid_json(self):
        simple_object_json = '{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"id":5,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}'
        self.assertRaises(Exception, Symbol.deserialize, simple_object_json)


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

    def test_serialize_should_return_json_id_none(self):
        result = self.combined_object.serialize()
        result_dict = json.loads(result)
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

    def test_serialize_should_return_json_id_not_none(self):
        self.combined_object.id = 999
        result = self.combined_object.serialize()
        result_dict = json.loads(result)
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

    def test_deserialize_should_return_symbol_object_id_none(self):
        combined_object_json = '{"class":"CombinedObject","shape":1,"width":2,"height":3,"id":null,"parts":[{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}]}'
        result_combined_object = CombinedObject.deserialize(combined_object_json)
        self.assertEqual(1, result_combined_object.shape)
        self.assertEqual(2, result_combined_object.width)
        self.assertEqual(3, result_combined_object.height)
        self.assertEqual(None, result_combined_object.id)

        self.assertEqual(1, result_combined_object.parts[0].shape)
        self.assertEqual(2, result_combined_object.parts[0].width)
        self.assertEqual(3, result_combined_object.parts[0].height)
        self.assertEqual(4, result_combined_object.parts[0].color)
        self.assertEqual(5, result_combined_object.parts[0].pattern)
        self.assertEqual(6, result_combined_object.parts[0].pattern_color)
        self.assertEqual(None, result_combined_object.parts[0].id)

        self.assertEqual(1, result_combined_object.parts[0].symbols[0].shape)
        self.assertEqual(2, result_combined_object.parts[0].symbols[0].width)
        self.assertEqual(3, result_combined_object.parts[0].symbols[0].height)
        self.assertEqual(4, result_combined_object.parts[0].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[0].id)

        self.assertEqual(6, result_combined_object.parts[0].symbols[1].shape)
        self.assertEqual(7, result_combined_object.parts[0].symbols[1].width)
        self.assertEqual(8, result_combined_object.parts[0].symbols[1].height)
        self.assertEqual(9, result_combined_object.parts[0].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[1].id)

        self.assertEqual(13, result_combined_object.parts[0].symbols[2].shape)
        self.assertEqual(12, result_combined_object.parts[0].symbols[2].width)
        self.assertEqual(11, result_combined_object.parts[0].symbols[2].height)
        self.assertEqual(10, result_combined_object.parts[0].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[2].id)

        self.assertEqual(1, result_combined_object.parts[1].shape)
        self.assertEqual(2, result_combined_object.parts[1].width)
        self.assertEqual(3, result_combined_object.parts[1].height)
        self.assertEqual(4, result_combined_object.parts[1].color)
        self.assertEqual(5, result_combined_object.parts[1].pattern)
        self.assertEqual(6, result_combined_object.parts[1].pattern_color)
        self.assertEqual(None, result_combined_object.parts[1].id)

        self.assertEqual(1, result_combined_object.parts[1].symbols[0].shape)
        self.assertEqual(2, result_combined_object.parts[1].symbols[0].width)
        self.assertEqual(3, result_combined_object.parts[1].symbols[0].height)
        self.assertEqual(4, result_combined_object.parts[1].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[0].id)

        self.assertEqual(6, result_combined_object.parts[1].symbols[1].shape)
        self.assertEqual(7, result_combined_object.parts[1].symbols[1].width)
        self.assertEqual(8, result_combined_object.parts[1].symbols[1].height)
        self.assertEqual(9, result_combined_object.parts[1].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[1].id)

        self.assertEqual(13, result_combined_object.parts[1].symbols[2].shape)
        self.assertEqual(12, result_combined_object.parts[1].symbols[2].width)
        self.assertEqual(11, result_combined_object.parts[1].symbols[2].height)
        self.assertEqual(10, result_combined_object.parts[1].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[2].id)

    def test_deserialize_should_return_symbol_object_id_not_none(self):
        combined_object_json = '{"class":"CombinedObject","shape":1,"width":2,"height":3,"id":999,"parts":[{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}]}'
        result_combined_object = CombinedObject.deserialize(combined_object_json)
        self.assertEqual(1, result_combined_object.shape)
        self.assertEqual(2, result_combined_object.width)
        self.assertEqual(3, result_combined_object.height)
        self.assertEqual(999, result_combined_object.id)

        self.assertEqual(1, result_combined_object.parts[0].shape)
        self.assertEqual(2, result_combined_object.parts[0].width)
        self.assertEqual(3, result_combined_object.parts[0].height)
        self.assertEqual(4, result_combined_object.parts[0].color)
        self.assertEqual(5, result_combined_object.parts[0].pattern)
        self.assertEqual(6, result_combined_object.parts[0].pattern_color)
        self.assertEqual(None, result_combined_object.parts[0].id)

        self.assertEqual(1, result_combined_object.parts[0].symbols[0].shape)
        self.assertEqual(2, result_combined_object.parts[0].symbols[0].width)
        self.assertEqual(3, result_combined_object.parts[0].symbols[0].height)
        self.assertEqual(4, result_combined_object.parts[0].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[0].id)

        self.assertEqual(6, result_combined_object.parts[0].symbols[1].shape)
        self.assertEqual(7, result_combined_object.parts[0].symbols[1].width)
        self.assertEqual(8, result_combined_object.parts[0].symbols[1].height)
        self.assertEqual(9, result_combined_object.parts[0].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[1].id)

        self.assertEqual(13, result_combined_object.parts[0].symbols[2].shape)
        self.assertEqual(12, result_combined_object.parts[0].symbols[2].width)
        self.assertEqual(11, result_combined_object.parts[0].symbols[2].height)
        self.assertEqual(10, result_combined_object.parts[0].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[0].symbols[2].id)

        self.assertEqual(1, result_combined_object.parts[1].shape)
        self.assertEqual(2, result_combined_object.parts[1].width)
        self.assertEqual(3, result_combined_object.parts[1].height)
        self.assertEqual(4, result_combined_object.parts[1].color)
        self.assertEqual(5, result_combined_object.parts[1].pattern)
        self.assertEqual(6, result_combined_object.parts[1].pattern_color)
        self.assertEqual(None, result_combined_object.parts[1].id)

        self.assertEqual(1, result_combined_object.parts[1].symbols[0].shape)
        self.assertEqual(2, result_combined_object.parts[1].symbols[0].width)
        self.assertEqual(3, result_combined_object.parts[1].symbols[0].height)
        self.assertEqual(4, result_combined_object.parts[1].symbols[0].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[0].id)

        self.assertEqual(6, result_combined_object.parts[1].symbols[1].shape)
        self.assertEqual(7, result_combined_object.parts[1].symbols[1].width)
        self.assertEqual(8, result_combined_object.parts[1].symbols[1].height)
        self.assertEqual(9, result_combined_object.parts[1].symbols[1].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[1].id)

        self.assertEqual(13, result_combined_object.parts[1].symbols[2].shape)
        self.assertEqual(12, result_combined_object.parts[1].symbols[2].width)
        self.assertEqual(11, result_combined_object.parts[1].symbols[2].height)
        self.assertEqual(10, result_combined_object.parts[1].symbols[2].color)
        self.assertEqual(None, result_combined_object.parts[1].symbols[2].id)

    def test_deserialize_should_raise_exception_invalid_json(self):
        combined_object_json = '{"class":"CombinedObject","shape":1,"width":2,"height":3,"id":999,"parts":[{"class":"SimpleObject","width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]},{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}]}'
        self.assertRaises(Exception, Symbol.deserialize, combined_object_json)
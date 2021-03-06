import json
import Common.serialization as serialization
from unittest import TestCase
from DataModel.Symbol import Symbol
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject
from DataModel.enums import Shape, Color, Pattern, Size


class SerializationTest(TestCase):

    def test_serialization_should_return_json_as_expected(self):
        symbols_1 = [Symbol(Shape.ELLIPSE, Size.MEDIUM, Size.TINY, Color.VIOLET),
                     Symbol(Shape.TRIANGLE, Size.SMALL, Size.SMALL, Color.BLUE),
                     Symbol(Shape.KITE, Size.BIG, Size.LARGE, Color.GREEN)]
        simple_object_1 = SimpleObject(Shape.HEXAGON, Size.LARGE, Size.MEDIUM, Color.RED, Pattern.HORIZONTAL_LINES,
                                       Color.GREEN, symbols_1)

        symbols_2 = [Symbol(Shape.TRIANGLE, Size.TINY, Size.TINY, Color.YELLOW),
                     Symbol(Shape.RECTANGLE, Size.BIG, Size.MEDIUM, Color.RED)]
        simple_object_2 = SimpleObject(Shape.CIRCLE, Size.MEDIUM, Size.LARGE, Color.VIOLET, Pattern.VERTICAL_LINES,
                                       Color.RED, symbols_2)

        combined_object = CombinedObject(Shape.TRIANGLE, Size.MEDIUM, Size.LARGE, [simple_object_1, simple_object_2])
        result = serialization.serialize_list_of_objects([simple_object_1, simple_object_2, combined_object])
        objects_list = json.loads(result)
        result_simple_object_1 = objects_list[0]
        result_simple_object_2 = objects_list[1]
        result_combined_object = objects_list[2]

        self.assertEqual(SimpleObject.__name__, result_simple_object_2['class'])
        self.assertEqual(2, result_simple_object_2['width'])
        self.assertEqual(15, result_simple_object_2['shape'])
        self.assertEqual(0, result_simple_object_2['pattern_color'])
        self.assertEqual(1, result_simple_object_2['pattern'])
        self.assertEqual(4, result_simple_object_2['color'])
        self.assertEqual(None, result_simple_object_2['id'])
        self.assertEqual(4, result_simple_object_2['height'])
        self.assertEqual(Symbol.__name__, result_simple_object_2['symbols'][0]['class'])
        self.assertEqual(1, result_simple_object_2['symbols'][0]['color'])
        self.assertEqual(2, result_simple_object_2['symbols'][0]['shape'])
        self.assertEqual(0, result_simple_object_2['symbols'][0]['width'])
        self.assertEqual(0, result_simple_object_2['symbols'][0]['height'])
        self.assertEqual(None, result_simple_object_2['symbols'][0]['id'])
        self.assertEqual(Symbol.__name__, result_simple_object_2['symbols'][1]['class'])
        self.assertEqual(0, result_simple_object_2['symbols'][1]['color'])
        self.assertEqual(6, result_simple_object_2['symbols'][1]['shape'])
        self.assertEqual(3, result_simple_object_2['symbols'][1]['width'])
        self.assertEqual(2, result_simple_object_2['symbols'][1]['height'])
        self.assertEqual(None, result_simple_object_2['symbols'][1]['id'])

        self.assertEqual(SimpleObject.__name__, result_simple_object_1['class'])
        self.assertEqual(4, result_simple_object_1['width'])
        self.assertEqual(12, result_simple_object_1['shape'])
        self.assertEqual(2, result_simple_object_1['pattern_color'])
        self.assertEqual(0, result_simple_object_1['pattern'])
        self.assertEqual(0, result_simple_object_1['color'])
        self.assertEqual(None, result_simple_object_1['id'])
        self.assertEqual(2, result_simple_object_1['height'])
        self.assertEqual(Symbol.__name__, result_simple_object_1['symbols'][0]['class'])
        self.assertEqual(4, result_simple_object_1['symbols'][0]['color'])
        self.assertEqual(16, result_simple_object_1['symbols'][0]['shape'])
        self.assertEqual(2, result_simple_object_1['symbols'][0]['width'])
        self.assertEqual(0, result_simple_object_1['symbols'][0]['height'])
        self.assertEqual(None, result_simple_object_1['symbols'][0]['id'])
        self.assertEqual(Symbol.__name__, result_simple_object_1['symbols'][1]['class'])
        self.assertEqual(3, result_simple_object_1['symbols'][1]['color'])
        self.assertEqual(2, result_simple_object_1['symbols'][1]['shape'])
        self.assertEqual(1, result_simple_object_1['symbols'][1]['width'])
        self.assertEqual(1, result_simple_object_1['symbols'][1]['height'])
        self.assertEqual(None, result_simple_object_1['symbols'][1]['id'])
        self.assertEqual(Symbol.__name__, result_simple_object_1['symbols'][2]['class'])
        self.assertEqual(2, result_simple_object_1['symbols'][2]['color'])
        self.assertEqual(18, result_simple_object_1['symbols'][2]['shape'])
        self.assertEqual(3, result_simple_object_1['symbols'][2]['width'])
        self.assertEqual(4, result_simple_object_1['symbols'][2]['height'])
        self.assertEqual(None, result_simple_object_1['symbols'][2]['id'])

        self.assertEqual(CombinedObject.__name__, result_combined_object['class'])
        self.assertEqual(2, result_combined_object['shape'])
        self.assertEqual(2, result_combined_object['width'])
        self.assertEqual(4, result_combined_object['height'])
        self.assertEqual(None, result_combined_object['id'])
        self.assertEqual(SimpleObject.__name__, result_combined_object['parts'][0]['class'])
        self.assertEqual(4, result_combined_object['parts'][0]['width'])
        self.assertEqual(12, result_combined_object['parts'][0]['shape'])
        self.assertEqual(2, result_combined_object['parts'][0]['pattern_color'])
        self.assertEqual(0, result_combined_object['parts'][0]['pattern'])
        self.assertEqual(0, result_combined_object['parts'][0]['color'])
        self.assertEqual(None, result_combined_object['parts'][0]['id'])
        self.assertEqual(2, result_combined_object['parts'][0]['height'])
        self.assertEqual(Symbol.__name__, result_combined_object['parts'][0]['symbols'][0]['class'])
        self.assertEqual(4, result_combined_object['parts'][0]['symbols'][0]['color'])
        self.assertEqual(16, result_combined_object['parts'][0]['symbols'][0]['shape'])
        self.assertEqual(2, result_combined_object['parts'][0]['symbols'][0]['width'])
        self.assertEqual(0, result_combined_object['parts'][0]['symbols'][0]['height'])
        self.assertEqual(None, result_combined_object['parts'][0]['symbols'][0]['id'])
        self.assertEqual(Symbol.__name__, result_combined_object['parts'][0]['symbols'][1]['class'])
        self.assertEqual(3, result_combined_object['parts'][0]['symbols'][1]['color'])
        self.assertEqual(2, result_combined_object['parts'][0]['symbols'][1]['shape'])
        self.assertEqual(1, result_combined_object['parts'][0]['symbols'][1]['width'])
        self.assertEqual(1, result_combined_object['parts'][0]['symbols'][1]['height'])
        self.assertEqual(None, result_combined_object['parts'][0]['symbols'][1]['id'])
        self.assertEqual(Symbol.__name__, result_combined_object['parts'][0]['symbols'][2]['class'])
        self.assertEqual(2, result_combined_object['parts'][0]['symbols'][2]['color'])
        self.assertEqual(18, result_combined_object['parts'][0]['symbols'][2]['shape'])
        self.assertEqual(3, result_combined_object['parts'][0]['symbols'][2]['width'])
        self.assertEqual(4, result_combined_object['parts'][0]['symbols'][2]['height'])
        self.assertEqual(None, result_combined_object['parts'][0]['symbols'][2]['id'])
        self.assertEqual(SimpleObject.__name__, result_combined_object['parts'][1]['class'])
        self.assertEqual(2, result_combined_object['parts'][1]['width'])
        self.assertEqual(15, result_combined_object['parts'][1]['shape'])
        self.assertEqual(0, result_combined_object['parts'][1]['pattern_color'])
        self.assertEqual(1, result_combined_object['parts'][1]['pattern'])
        self.assertEqual(4, result_combined_object['parts'][1]['color'])
        self.assertEqual(None, result_combined_object['parts'][1]['id'])
        self.assertEqual(4, result_combined_object['parts'][1]['height'])
        self.assertEqual(Symbol.__name__, result_combined_object['parts'][1]['symbols'][0]['class'])
        self.assertEqual(1, result_combined_object['parts'][1]['symbols'][0]['color'])
        self.assertEqual(2, result_combined_object['parts'][1]['symbols'][0]['shape'])
        self.assertEqual(0, result_combined_object['parts'][1]['symbols'][0]['width'])
        self.assertEqual(0, result_combined_object['parts'][1]['symbols'][0]['height'])
        self.assertEqual(None, result_combined_object['parts'][1]['symbols'][0]['id'])
        self.assertEqual(Symbol.__name__, result_combined_object['parts'][1]['symbols'][1]['class'])
        self.assertEqual(0, result_combined_object['parts'][1]['symbols'][1]['color'])
        self.assertEqual(6, result_combined_object['parts'][1]['symbols'][1]['shape'])
        self.assertEqual(3, result_combined_object['parts'][1]['symbols'][1]['width'])
        self.assertEqual(2, result_combined_object['parts'][1]['symbols'][1]['height'])
        self.assertEqual(None, result_combined_object['parts'][1]['symbols'][1]['id'])



    def test_deserialization_should_return_list_of_objects_from_json(self):
        json_str = '[' + \
'{\"symbols\": [{\"color\": 4, \"height\": 0, \"width\": 2, \"shape\": 16, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 3, \"height\": 1, \"width\": 1, \"shape\": 2, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 2, \"height\": 4, \"width\": 3, \"shape\": 18, \"id\": null, \"class\": \"Symbol\"}], \"width\": 4, \"shape\": 12, \"pattern_color\": 2, \"color\": 0, \"pattern\": 0, \"id\": null, \"class\": \"SimpleObject\", \"height\": 2},' + \
'{\"symbols\": [{\"color\": 1, \"height\": 0, \"width\": 0, \"shape\": 2, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 0, \"height\": 2, \"width\": 3, \"shape\": 6, \"id\": null, \"class\": \"Symbol\"}], \"width\": 2, \"shape\": 15, \"pattern_color\": 0, \"color\": 4, \"pattern\": 1, \"id\": null, \"class\": \"SimpleObject\", \"height\": 4}, ' + \
'{\"class\": \"CombinedObject\", \"width\": 2, \"shape\": 2, \"parts\": [{\"symbols\": [{\"color\": 4, \"height\": 0, \"width\": 2, \"shape\": 16, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 3, \"height\": 1, \"width\": 1, \"shape\": 2, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 2, \"height\": 4, \"width\": 3, \"shape\": 18, \"id\": null, \"class\": \"Symbol\"}], \"width\": 4, \"shape\": 12, \"pattern_color\": 2, \"color\": 0, \"pattern\": 0, \"height\": 2, \"class\": \"SimpleObject\", \"id\": null}, {\"symbols\": [{\"color\": 1, \"height\": 0, \"width\": 0, \"shape\": 2, \"id\": null, \"class\": \"Symbol\"}, {\"color\": 0, \"height\": 2, \"width\": 3, \"shape\": 6, \"id\": null, \"class\": \"Symbol\"}], \"width\": 2, \"shape\": 15, \"pattern_color\": 0, \"color\": 4, \"pattern\": 1, \"height\": 4, \"class\": \"SimpleObject\", \"id\": null}], \"height\": 4, \"id\": null}]'
        objects = serialization.deserialize_list_of_objects(json_str)
        result_simple_object_1 = objects[0]
        result_simple_object_2 = objects[1]
        result_combined_object = objects[2]

        self.assertEqual(Size(4), result_simple_object_1.width)
        self.assertEqual(Shape(12), result_simple_object_1.shape)
        self.assertEqual(Color(2), result_simple_object_1.pattern_color)
        self.assertEqual(Pattern(0), result_simple_object_1.pattern)
        self.assertEqual(Color(0), result_simple_object_1.color)
        self.assertEqual(None, result_simple_object_1.id)
        self.assertEqual(Size(2), result_simple_object_1.height)
        self.assertEqual(Color(4), result_simple_object_1.symbols[0].color)
        self.assertEqual(Shape(16), result_simple_object_1.symbols[0].shape)
        self.assertEqual(Size(2), result_simple_object_1.symbols[0].width)
        self.assertEqual(Size(0), result_simple_object_1.symbols[0].height)
        self.assertEqual(None, result_simple_object_1.symbols[0].id)
        self.assertEqual(Color(3), result_simple_object_1.symbols[1].color)
        self.assertEqual(Shape(2), result_simple_object_1.symbols[1].shape)
        self.assertEqual(Size(1), result_simple_object_1.symbols[1].width)
        self.assertEqual(Size(1), result_simple_object_1.symbols[1].height)
        self.assertEqual(None, result_simple_object_1.symbols[1].id)
        self.assertEqual(Color(2), result_simple_object_1.symbols[2].color)
        self.assertEqual(Shape(18), result_simple_object_1.symbols[2].shape)
        self.assertEqual(Size(3), result_simple_object_1.symbols[2].width)
        self.assertEqual(Size(4), result_simple_object_1.symbols[2].height)
        self.assertEqual(None, result_simple_object_1.symbols[2].id)

        self.assertEqual(Size(2), result_simple_object_2.width)
        self.assertEqual(Shape(15), result_simple_object_2.shape)
        self.assertEqual(Color(0), result_simple_object_2.pattern_color)
        self.assertEqual(Pattern(1), result_simple_object_2.pattern)
        self.assertEqual(Color(4), result_simple_object_2.color)
        self.assertEqual(None, result_simple_object_2.id)
        self.assertEqual(Size(4), result_simple_object_2.height)
        self.assertEqual(Color(1), result_simple_object_2.symbols[0].color)
        self.assertEqual(Shape(2), result_simple_object_2.symbols[0].shape)
        self.assertEqual(Size(0), result_simple_object_2.symbols[0].width)
        self.assertEqual(Size(0), result_simple_object_2.symbols[0].height)
        self.assertEqual(None, result_simple_object_2.symbols[0].id)
        self.assertEqual(Color(0), result_simple_object_2.symbols[1].color)
        self.assertEqual(Shape(6), result_simple_object_2.symbols[1].shape)
        self.assertEqual(Size(3), result_simple_object_2.symbols[1].width)
        self.assertEqual(Size(2), result_simple_object_2.symbols[1].height)
        self.assertEqual(None, result_simple_object_2.symbols[1].id)

        self.assertEqual(Shape(2), result_combined_object.shape)
        self.assertEqual(Size(2), result_combined_object.width)
        self.assertEqual(Size(4), result_combined_object.height)
        self.assertEqual(None, result_combined_object.id)
        self.assertEqual(Size(4), result_combined_object.parts[0].width)
        self.assertEqual(Shape(12), result_combined_object.parts[0].shape)
        self.assertEqual(Color(2), result_combined_object.parts[0].pattern_color)
        self.assertEqual(Pattern(0), result_combined_object.parts[0].pattern)
        self.assertEqual(Color(0), result_combined_object.parts[0].color)
        self.assertEqual(None, result_combined_object.parts[0].id)
        self.assertEqual(Size(2), result_combined_object.parts[0].height)
        self.assertEqual(Color(4), result_combined_object.parts[0].symbols[0].color)
        self.assertEqual(Shape(16), result_combined_object.parts[0].symbols[0].shape)
        self.assertEqual(Size(2), result_combined_object.parts[0].symbols[0].width)
        self.assertEqual(Size(0), result_combined_object.parts[0].symbols[0].height)
        self.assertEqual(None, result_combined_object.parts[0].symbols[0].id)
        self.assertEqual(Color(3), result_combined_object.parts[0].symbols[1].color)
        self.assertEqual(Shape(2), result_combined_object.parts[0].symbols[1].shape)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[1].width)
        self.assertEqual(Size(1), result_combined_object.parts[0].symbols[1].height)
        self.assertEqual(None, result_combined_object.parts[0].symbols[1].id)
        self.assertEqual(Color(2), result_combined_object.parts[0].symbols[2].color)
        self.assertEqual(Shape(18), result_combined_object.parts[0].symbols[2].shape)
        self.assertEqual(Size(3), result_combined_object.parts[0].symbols[2].width)
        self.assertEqual(Size(4), result_combined_object.parts[0].symbols[2].height)
        self.assertEqual(None, result_combined_object.parts[0].symbols[2].id)
        self.assertEqual(Size(2), result_combined_object.parts[1].width)
        self.assertEqual(Shape(15), result_combined_object.parts[1].shape)
        self.assertEqual(Color(0), result_combined_object.parts[1].pattern_color)
        self.assertEqual(Pattern(1), result_combined_object.parts[1].pattern)
        self.assertEqual(Color(4), result_combined_object.parts[1].color)
        self.assertEqual(None, result_combined_object.parts[1].id)
        self.assertEqual(Size(4), result_combined_object.parts[1].height)
        self.assertEqual(Color(1), result_combined_object.parts[1].symbols[0].color)
        self.assertEqual(Shape(2), result_combined_object.parts[1].symbols[0].shape)
        self.assertEqual(Size(0), result_combined_object.parts[1].symbols[0].width)
        self.assertEqual(Size(0), result_combined_object.parts[1].symbols[0].height)
        self.assertEqual(None, result_combined_object.parts[1].symbols[0].id)
        self.assertEqual(Color(0), result_combined_object.parts[1].symbols[1].color)
        self.assertEqual(Shape(6), result_combined_object.parts[1].symbols[1].shape)
        self.assertEqual(Size(3), result_combined_object.parts[1].symbols[1].width)
        self.assertEqual(Size(2), result_combined_object.parts[1].symbols[1].height)
        self.assertEqual(None, result_combined_object.parts[1].symbols[1].id)




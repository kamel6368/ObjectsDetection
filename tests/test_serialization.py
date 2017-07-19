import Common.serialization as serialization
from unittest import TestCase


class SerializationTest(TestCase):


    def test_deserialization_should_return_list_of_objects_from_json(self):
        json_str = '[{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":null,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}, ' + \
                   '{"class":"SimpleObject","shape":1,"width":2,"height":3,"color":4,"pattern":5,"pattern_color":6,"id":5,"symbols":[{"class":"Symbol", "shape":1, "width":2, "height":3,"color":4, "id":null},{"class":"Symbol", "shape":6, "width":7,"height":8, "color":9, "id":null},{"class":"Symbol", "shape":13,"width":12, "height":11, "color":10, "id":null}]}]'

        objects = serialization.deserialize_list_of_objects(json_str)
        self.assertEqual(1, objects[0].shape)
        self.assertEqual(2, objects[0].width)
        self.assertEqual(3, objects[0].height)
        self.assertEqual(4, objects[0].color)
        self.assertEqual(5, objects[0].pattern)
        self.assertEqual(6, objects[0].pattern_color)
        self.assertEqual(None, objects[0].id)
        self.assertEqual(1, objects[0].symbols[0].shape)
        self.assertEqual(2, objects[0].symbols[0].width)
        self.assertEqual(3, objects[0].symbols[0].height)
        self.assertEqual(4, objects[0].symbols[0].color)
        self.assertEqual(6, objects[0].symbols[1].shape)
        self.assertEqual(7, objects[0].symbols[1].width)
        self.assertEqual(8, objects[0].symbols[1].height)
        self.assertEqual(9, objects[0].symbols[1].color)

        self.assertEqual(1, objects[1].shape)
        self.assertEqual(2, objects[1].width)
        self.assertEqual(3, objects[1].height)
        self.assertEqual(4, objects[1].color)
        self.assertEqual(5, objects[1].pattern)
        self.assertEqual(6, objects[1].pattern_color)
        self.assertEqual(5, objects[1].id)
        self.assertEqual(1, objects[1].symbols[0].shape)
        self.assertEqual(2, objects[1].symbols[0].width)
        self.assertEqual(3, objects[1].symbols[0].height)
        self.assertEqual(4, objects[1].symbols[0].color)
        self.assertEqual(6, objects[1].symbols[1].shape)
        self.assertEqual(7, objects[1].symbols[1].width)
        self.assertEqual(8, objects[1].symbols[1].height)
        self.assertEqual(9, objects[1].symbols[1].color)

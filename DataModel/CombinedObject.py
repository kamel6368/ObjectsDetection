import json
from SimpleObject import SimpleObject
from enums import Shape, Size


class CombinedObject:

    def __init__(self, shape, width, height, parts, id=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.parts = parts
        self.id = id

    @staticmethod
    def from_dictionary(dictionary):
        if dictionary['class'] != CombinedObject.__name__:
            raise ValueError('Given string is not serialized CombinedObject')
        dictionary_parts = dictionary['parts']
        parts = []
        for dictionary_part in dictionary_parts:
            parts.append(SimpleObject.from_dictionary(dictionary_part))
        return CombinedObject(Shape(dictionary['shape']),
                              Size(dictionary['width']),
                              Size(dictionary['height']),
                              parts,
                              dictionary['id'])

    def to_dictionary(self):
        dict_parts = []
        for part in self.parts:
            dict_parts.append(part.to_dictionary())
        return {'class': CombinedObject.__name__,
                'id': self.id,
                'shape': self.shape.value,
                'width': self.width.value,
                'height': self.height.value,
                'parts': dict_parts
                }

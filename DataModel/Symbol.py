import json
from enums import Shape, Color, Size


class Symbol:

    def __init__(self, shape, width, height, color, id=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.color = color
        self.id = id

    @staticmethod
    def from_dictionary(dictionary):
        if dictionary['class'] != Symbol.__name__:
            raise ValueError('Given string is not serialized Symbol')
        return Symbol(Shape(dictionary['shape']),
                      Size(dictionary['width']),
                      Size(dictionary['height']),
                      Color(dictionary['color']),
                      dictionary['id'])

    def to_dictionary(self):
        return {'class': Symbol.__name__,
                'id': self.id,
                'shape': self.shape.value,
                'width': self.width.value,
                'height': self.height.value,
                'color': self.color.value
                }

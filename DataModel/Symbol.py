import json


class Symbol:

    def __init__(self, shape, width, height, color, id=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.color = color
        self.id = id

    def serialize(self):
        return json.dumps({
            'class': Symbol.__name__,
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'color': self.color.value,
            'id': self.id
        })

    @staticmethod
    def deserialize(dictionary):
        if isinstance(dictionary, str):
            dictionary = json.loads(dictionary)
        if dictionary['class'] != Symbol.__name__:
            raise ValueError('Given string is not serialized Symbol')
        return Symbol(dictionary['shape'],
                      dictionary['width'],
                      dictionary['height'],
                      dictionary['color'],
                      dictionary['id'])

    def to_dictionary(self):
        return {'class': Symbol.__name__,
                'id': self.id,
                'shape': self.shape.value,
                'width': self.width.value,
                'height': self.height.value,
                'color': self.color.value
                }

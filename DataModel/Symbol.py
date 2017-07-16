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
            'class': 'Symbol',
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'color': self.color.value,
            'id': self.id
        })

    @staticmethod
    def deserialize(json_str):
        if isinstance(json_str, dict):
            dictionary = json_str
        else:
            dictionary = json.loads(json_str)
        if dictionary['class'] != 'Symbol':
            raise ValueError('Given string is not serialized Symbol')
        return Symbol(dictionary['shape'],
                      dictionary['width'],
                      dictionary['height'],
                      dictionary['color'],
                      dictionary['id'])

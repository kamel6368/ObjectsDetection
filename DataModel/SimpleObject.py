import enums
import json
from Symbol import Symbol


class SimpleObject:

    def __init__(self, shape, width, height, color, pattern, pattern_color, symbols, id=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.color = color
        self.pattern = pattern
        self.pattern_color = pattern_color
        self.symbols = symbols
        self.id = id

    def quasi_equals(self, symbol):
        are_equal = (self.shape == symbol.shape) or (self._is_triangle(self) and
                                                      self._is_triangle(symbol))
        are_equal = are_equal and self.color == symbol.color
        are_equal = are_equal and self.height == symbol.height
        are_equal = are_equal and self.width == symbol.width

        return are_equal

    def to_string(self):
        result = 'Shape: ' + str(self.color) + ' ' + str(self.shape) + ' ' + str(self.width) + ' ' + str(self.height) + ' ' + \
                 str(self.pattern) + ' ' + str(self.pattern_color) + '\n'
        for symbol in self.symbols:
            result += '\t' + symbol.to_string()
        return result

    @staticmethod
    def _is_triangle(object):
        return object.shape is enums.Shape.TRIANGLE or object.shape is enums.Shape.EQUILATERAL_TRIANGLE or \
               object.shape is enums.Shape.ISOSCELES_TRIANGLE

    def serialize(self):
        dictionary_symbols = []
        for symbol in self.symbols:
            dictionary_symbols.append(symbol.to_dictionary())
        result = json.dumps({
            'class': SimpleObject.__name__,
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'color': self.color.value,
            'pattern': self.pattern.value,
            'pattern_color': self.pattern_color.value,
            'symbols': dictionary_symbols,
            'id': self.id
        })
        return result

    @staticmethod
    def deserialize(dictionary):
        if isinstance(dictionary, str):
            dictionary = json.loads(dictionary)
        if dictionary['class'] != SimpleObject.__name__:
            raise ValueError('Given string is not serialized SimpleObject')
        symbols = []
        dictionary_symbols = dictionary['symbols']
        for dictionary_symbol in dictionary_symbols:
            symbols.append(Symbol.deserialize(json.dumps(dictionary_symbol)))
        return SimpleObject(dictionary['shape'],
                            dictionary['width'],
                            dictionary['height'],
                            dictionary['color'],
                            dictionary['pattern'],
                            dictionary['pattern_color'],
                            symbols,
                            dictionary['id'])

    def to_dictionary(self):
        dict_symbols = []
        for symbol in self.symbols:
            dict_symbols.append(symbol.to_dictionary())
        return {'class': SimpleObject.__name__,
                'id': self.id,
                'shape': self.shape.value,
                'width': self.width.value,
                'height': self.height.value,
                'color': self.color.value,
                'pattern': self.pattern.value,
                'pattern_color': self.pattern_color.value,
                'symbols': dict_symbols
                }

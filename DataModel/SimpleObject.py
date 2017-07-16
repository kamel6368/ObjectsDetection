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

    def quasi_equals(self, another):
        are_equal = (self.shape == another.shape) or (self._is_triangle() and another._is_triangle())
        are_equal = are_equal and self.color == another.color
        are_equal = are_equal and self.height == another.height
        are_equal = are_equal and self.width == another.width
        are_equal = are_equal and self.pattern == another.pattern
        are_equal = are_equal and self.pattern_color == another.pattern_color
        are_equal = are_equal and len(self.symbols) == len(self.symbols)
        if not are_equal:
            return False

        if len(self.symbols) != len(another.symbols):
            return False

        for i in range(0, len(self.symbols)):
            are_equal = are_equal and self.symbols[i].quasi_equals(another.symbols[i])
        return are_equal

    def to_string(self):
        result = 'Shape: ' + str(self.color) + ' ' + str(self.shape) + ' ' + str(self.width) + ' ' + str(self.height) + ' ' + \
                 str(self.pattern) + ' ' + str(self.pattern_color) + '\n'
        for symbol in self.symbols:
            result += '\t' + symbol.to_string()
        return result

    def _is_triangle(self):
        return self.shape is enums.Shape.TRIANGLE or self.shape is enums.Shape.EQUILATERAL_TRIANGLE or \
               self.shape is enums.Shape.ISOSCELES_TRIANGLE

    def serialize(self):
        serialized_symbols = []
        for symbol in self.symbols:
            serialized_symbols.append(symbol.serialize())
        return json.dumps({
            'class': 'SimpleObject',
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'color': self.color.value,
            'pattern': self.pattern.value,
            'pattern_color': self.pattern_color.value,
            'symbols': json.dumps(serialized_symbols),
            'id': self.id
        })

    @staticmethod
    def deserialize(json_str):
        if isinstance(json_str, dict):
            dictionary = json_str
        else:
            dictionary = json.loads(json_str)
        if dictionary['class'] != 'SimpleObject':
            raise ValueError('Given string is not serialized SimpleObject')
        symbols = []
        serialized_symbols = dictionary['symbols']
        for serialized_symbol in serialized_symbols:
            symbols.append(Symbol.deserialize(serialized_symbol))
        return SimpleObject(dictionary['shape'],
                            dictionary['width'],
                            dictionary['height'],
                            dictionary['color'],
                            dictionary['pattern'],
                            dictionary['pattern_color'],
                            symbols,
                            dictionary['id'])

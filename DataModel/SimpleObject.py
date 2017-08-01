import json
from Symbol import Symbol
from enums import Shape, Color, Size, Pattern


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

    @staticmethod
    def _is_triangle(object):
        return object.shape is Shape.TRIANGLE or object.shape is Shape.EQUILATERAL_TRIANGLE or \
               object.shape is Shape.ISOSCELES_TRIANGLE

    @staticmethod
    def from_dictionary(dictionary):
        if dictionary['class'] != SimpleObject.__name__:
            raise ValueError('Given string is not serialized SimpleObject')
        symbols = []
        dictionary_symbols = dictionary['symbols']
        for dictionary_symbol in dictionary_symbols:
            symbols.append(Symbol.from_dictionary(dictionary_symbol))
        return SimpleObject(Shape(dictionary['shape']),
                            Size(dictionary['width']),
                            Size(dictionary['height']),
                            Color(dictionary['color']),
                            Pattern(dictionary['pattern']),
                            Color(dictionary['pattern_color']),
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

    def to_string(self, one_line=False, separator=', '):
        str_symbols = self._list_of_symbols_to_string(one_line, separator)

        parts = [
            'Simple Object',
            'Shape - ' + str(self.shape).split('.')[1],
            'Color - ' + str(self.color).split('.')[1],
            'Width - ' + str(self.width).split('.')[1],
            'Height - ' + str(self.height).split('.')[1],
            'Pattern - ' + str(self.pattern).split('.')[1],
            'Pattern Color - ' + str(self.pattern_color).split('.')[1],
            str_symbols
        ]
        if one_line:
            return ''.join([p + separator for p in parts])[:-2]
        else:
            return '\n'.join(parts)

    def _list_of_symbols_to_string(self, one_line, separator):
        if self.symbols == []:
            return 'Symbols: None'
        str_symbols = 'Symbols: [' if one_line else 'Symbols:\n'
        if one_line:
            for symbol in self.symbols:
                str_symbols += '(' + symbol.to_string(one_line=True, separator=separator) + '), '
            str_symbols = str_symbols[:-2] + ']'
        else:
            for symbol in self.symbols:
                str_symbols += symbol.to_string(one_line=False) + '\n\n'
            str_symbols = str_symbols[:-2]
            str_symbols = '\t'.join(str_symbols.splitlines(True))
        return str_symbols

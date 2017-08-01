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
    '''
    def to_string(self, one_line=False, separator=','):
        str_parts = self._list_of_simple_objects_to_string(one_line, separator)

        parts = [
            'Simple Object',
            'Shape - ' + str(self.shape).split('.')[1],
            'Width - ' + str(self.width).split('.')[1],
            'Height - ' + str(self.height).split('.')[1],
            str_parts
        ]
        if one_line:
            return ''.join([p + separator for p in str_parts])[:-2]
        else:
            return '\t' + '\t'.join(str_parts.splitlines(True))

    def _list_of_simple_objects_to_string(self, one_line, separator):
        str_parts = 'Parts: [' if one_line else 'Parts:\n'
        if one_line:
            for part in self.parts:
                str_parts += '(' + part.to_string(one_line=True, separator=separator) + ')'
            str_parts += ']'
        else:
            for part in self.parts:
                str_parts += part.to_string(one_line=False) + '\n'
            str_parts = str_parts[:-1]
        return str_parts
    '''
    def to_string(self, one_line=False, separator=', '):
        str_parts = self._list_of_simple_objects_to_string(one_line, separator)

        parts = [
            'Combined Object',
            'Shape - ' + str(self.shape).split('.')[1],
            'Width - ' + str(self.width).split('.')[1],
            'Height - ' + str(self.height).split('.')[1],
            str_parts
        ]
        if one_line:
            return ''.join([p + separator for p in parts])[:-2]
        else:
            return '\n'.join(parts)

    def _list_of_simple_objects_to_string(self, one_line, separator):
        if self.parts == []:
            return 'Parts: None'
        str_parts = 'Parts: [' if one_line else 'Parts:\n'
        if one_line:
            for part in self.parts:
                str_parts += '(' + part.to_string(one_line=True, separator=separator) + '), '
            str_parts = str_parts[:-2] + ']'
        else:
            for part in self.parts:
                str_parts += part.to_string(one_line=False) + '\n\n'
            str_parts = str_parts[:-2]
            str_parts = '\t'.join(str_parts.splitlines(True))
        return str_parts

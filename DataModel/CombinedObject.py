import json
from SimpleObject import SimpleObject


class CombinedObject:

    def __init__(self, shape, width, height, parts, id=None):
        self.shape = shape
        self.width = width
        self.height = height
        self.parts = parts
        self.id = id

    def serialize(self):
        dictionary_parts = []
        for part in self.parts:
            dictionary_parts.append(part.to_dictionary())
        return json.dumps({
            'class': CombinedObject.__name__,
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'parts': dictionary_parts,
            'id': self.id
        })

    @staticmethod
    def deserialize(dictionary):
        if isinstance(dictionary, str):
            dictionary = json.loads(dictionary)
        if dictionary['class'] != CombinedObject.__name__:
            raise ValueError('Given string is not serialized CombinedObject')
        dictionary_parts = dictionary['parts']
        parts = []
        for dictionary_part in dictionary_parts:
            parts.append(SimpleObject.deserialize(json.dumps(dictionary_part)))
        return CombinedObject(dictionary['shape'],
                              dictionary['width'],
                              dictionary['height'],
                              parts,
                              dictionary['id'])

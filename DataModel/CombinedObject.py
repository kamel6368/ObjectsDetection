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
        serialized_parts = []
        for part in self.parts:
            serialized_parts.append(part.serialize())
        return json.dumps({
            'class': 'CombinedObject',
            'shape': self.shape.value,
            'width': self.width.value,
            'height': self.height.value,
            'parts': json.dumps(serialized_parts),
            'id': self.id
        })

    @staticmethod
    def deserialize(json_str):
        if isinstance(json_str, dict):
            dictionary = json_str
        else:
            dictionary = json.loads(json_str)
        if dictionary['class'] != 'CombinedObject':
            raise ValueError('Given string is not serialized CombinedObject')
        serialized_parts = dictionary['parts']
        parts = []
        for serialized_part in serialized_parts:
            parts.append(SimpleObject.deserialize(serialized_part))
        return CombinedObject(dictionary['shape'],
                              dictionary['width'],
                              dictionary['height'],
                              parts,
                              dictionary['id'])

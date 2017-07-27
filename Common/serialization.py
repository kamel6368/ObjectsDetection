import cv2
import numpy as np
import base64
import json
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject

def image_to_string(image):
    _, jpg_as_text = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(jpg_as_text)
    return jpg_as_text


def image_from_string(string):
    try:
        image = base64.b64decode(string)
        image = np.frombuffer(image, dtype=np.uint8)
        image = cv2.imdecode(image, flags=1)
    except:
        image = None
    return image


def serialize_list_of_objects(objects):
    serialized_objects = []
    for object in objects:
        serialized_objects.append(object.to_dictionary())
    result = json.dumps(serialized_objects)
    return result


def deserialize_list_of_objects(json_str):
    objects_str = json.loads(json_str)
    result = []
    for object_str in objects_str:
        dictionary_object = object_str
        if dictionary_object['class'] == SimpleObject.__name__:
            result.append(SimpleObject.from_dictionary(dictionary_object))
        elif dictionary_object['class'] == CombinedObject.__name__:
            result.append(CombinedObject.from_dictionary(dictionary_object))
    return result

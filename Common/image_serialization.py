import cv2
import numpy as np
import base64


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

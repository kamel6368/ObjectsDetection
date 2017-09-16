import cv2
from kivy.graphics.texture import Texture


def list_of_objects_to_string(objects):
    result = ''
    for object in objects:
        result += object.to_string().replace('\t', '    ') + '\n\n'
    return result


def list_of_objects_with_certainty_factor_to_string(objects):
    result = ''
    for tuple in objects:
        object_str = tuple[0].to_string().replace('\t', '    ')
        temp = object_str.split('\n')
        temp[0] += '    (Certainty Factor: ' + str(tuple[1]) + ')'
        result += '\n'.join(temp) + '\n\n'
    return result


def convert_cv2_image_to_kivy_texture(frame):
    buf1 = cv2.flip(frame, 0)
    buf = buf1.tostring()
    image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    return image_texture

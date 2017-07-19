import cv2
import json
from Common.serialization import serialize_list_of_objects
from DataModel.enums import Color
from kivy.graphics.texture import Texture
from Common.TCPConnections import TCPCommands


def try_reconnect_to_alive_agents(main, tcp_client):
    main.is_agent_alive = tcp_client.connect(single_try=True)
    if main.is_agent_alive:
        tcp_client.send(TCPCommands.REMOTE_SERVER_BREAK_DOWN, '')


def acknowledge_agent_registration(main, tcp_client):
    if not main.is_agent_alive:
        tcp_client.connect()
    tcp_client.send(TCPCommands.REGISTER_ACK, '')
    main.is_agent_alive = True


def send_detected_object_to_agent(objects, tcp_client):
    content = serialize_list_of_objects(objects)
    tcp_client.send(TCPCommands.OBJECTS, content)


def convert_cv2_image_to_kivy_texture(frame):
    buf1 = cv2.flip(frame, 0)
    buf = buf1.tostring()
    image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    return image_texture


def start_agent():
    pass


def shutdown_agent(tcp_client):
    tcp_client.send(TCPCommands.SHUTDOWN, '')


def acknowledge_agent_shutdown(tcp_client):
    tcp_client.send(TCPCommands.SHUTDOWN_ACK_ACK, '')


def start_stream(tcp_client):
    tcp_client.send(TCPCommands.STREAM_ON, '')


def stop_stream(tcp_client):
    tcp_client.send(TCPCommands.STREAM_OFF, '')


def detect_objects(object_detector, raw_image, quantizied_image):
    image_to_process = raw_image
    if quantizied_image is not None:
        image_to_process = quantizied_image
    return object_detector.detect_objects(image_to_process, real_distance=None,
                                          auto_contour_clear=False, prepare_image_before_detection=False)


def change_quantization_state(main, should_enable):
    main.apply_quantization = should_enable


def draw_contours_on_image(object_detector, image):
    for single_contour in object_detector.detected_contours:
        draw_color = (0, 0, 0)
        if single_contour[0] is Color.RED:
            draw_color = (0, 0, 255)
        elif single_contour[0] is Color.YELLOW:
            draw_color = (40, 244, 255)
        elif single_contour[0] is Color.GREEN:
            draw_color = (0, 255, 0)
        elif single_contour[0] is Color.BLUE:
            draw_color = (255, 0, 0)
        elif single_contour[0] is Color.VIOLET:
            draw_color = (188, 0, 105)
        cv2.drawContours(image, [single_contour[1]], -1, draw_color, 2)

import cv2
from kivy.graphics.texture import Texture
from kivy.clock import mainthread
from Common.TCPConnections import TCPCommands


def try_reconnect_to_alive_agents(main, tcp_client):
    main.are_agents_alive_before_startup = tcp_client.connect(single_try=True)
    if main.are_agents_alive_before_startup:
        tcp_client.send(TCPCommands.REMOTE_SERVER_BREAK_DOWN, '')


@mainthread
def show_image(layout, image):
    image_texture = convert_cv2_image_to_kivy_texture(image)
    layout.ids.raw_image.texture = image_texture


def acknowledge_agent_registration(main, tcp_client):
    if not main.are_agents_alive_before_startup:
        tcp_client.connect()
    tcp_client.send(TCPCommands.REGISTER_ACK, '')


def send_detected_object_to_agent(objects, tcp_client):

    if objects is None:
        objects = []

    tcp_client.send(TCPCommands.OBJECTS, '')


def convert_cv2_image_to_kivy_texture(frame):
    buf1 = cv2.flip(frame, 0)
    buf = buf1.tostring()
    image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    return image_texture

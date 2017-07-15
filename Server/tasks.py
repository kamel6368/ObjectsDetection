import cv2
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

    if objects is None:
        objects = []

    tcp_client.send(TCPCommands.OBJECTS, '')


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


def detect_objects(image, is_quantized):
    pass
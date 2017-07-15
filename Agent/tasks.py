from Common.image_serialization import image_to_string
from Common.TCPConnections import TCPCommands


def send_image_to_remote_server(tcp_client, image):
    img_str = image_to_string(image)
    tcp_client.send(TCPCommands.IMAGE, img_str)


def take_picture(video_capture):
    return video_capture.read()


def register(tcp_client, logger):
    logger.print_msg('tasks/register begin')
    tcp_client.connect()
    tcp_client.send(TCPCommands.REGISTER, '')
    logger.print_msg('tasks/register end')


def acknowledge_shutdown(tcp_client):
    tcp_client.send(TCPCommands.SHUTDOWN_ACK, '')


def shutdown(main, tcp_server, tcp_client, video_capture):
    video_capture.release()
    if tcp_server is not None:
        tcp_server.disconnect()
    if tcp_client is not None:
        tcp_client.disconnect()
    main.exit = True


def acknowledge_stream_start(tcp_client):
    tcp_client.send(TCPCommands.STREAM_ON_ACK, '')


def acknowledge_stream_stop(tcp_client):
    tcp_client.send(TCPCommands.STREAM_OFF_ACK, '')


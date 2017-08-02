import cv2
import tasksGUI
from collections import deque
from Common.serialization import serialize_list_of_objects
from DataModel.enums import Color
from kivy.graphics.texture import Texture
from Common.TCPConnections import TCPCommands, StreamMode


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


def start_stream(main, tcp_client, main_layout):
    if main.stream_mode == StreamMode.VIDEO:
        clear_video_buffer(main)
    video_duration = main_layout.get_video_duration()
    tcp_client.send(TCPCommands.STREAM_ON, prepare_content_for_stream_on(main.stream_mode, video_duration))


def prepare_content_for_stream_on(stream_mode, duration):
    content = 'STREAM_MODE:' + str(stream_mode.value)
    if stream_mode == StreamMode.VIDEO:
        content += ';DURATION:' + str(duration)
    return content


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


def change_stream_mode(main):
    if main.stream_mode == StreamMode.VIDEO:
        main.stream_mode = StreamMode.EACH_FRAME
    elif main.stream_mode == StreamMode.EACH_FRAME:
        main.stream_mode = StreamMode.VIDEO


def image_action_stream_mode_each_frame(main, tcp_client, image):
    quantizied_image = None
    if main.apply_quantization:
        quantizied_image = main.object_detector._prepare_image_for_detection(image)

    objects = detect_objects(main.object_detector, image, quantizied_image)
    draw_contours_on_image(main.object_detector, image)
    if main.apply_quantization and quantizied_image is not None:
        draw_contours_on_image(main.object_detector, quantizied_image)
        tasksGUI.update_quantization_image(main.main_layout, quantizied_image)
    tasksGUI.update_raw_image(main.main_layout, image)
    objects_string = list_of_objects_to_string(objects)
    tasksGUI.print_on_console(main.main_layout, objects_string)
    main.frames_buffer.append([image, quantizied_image, objects_string])
    main.object_detector.clear_contours()
    send_detected_object_to_agent(objects, tcp_client)


def image_action_stream_mode_video(image, video_buffer, main_layout):
    video_buffer.append(image)
    tasksGUI.update_raw_image(main_layout, image)


def list_of_objects_to_string(objects):
    result = ''
    for object in objects:
        result += object.to_string() + '\n'
    return result


def extract_objects_from_video(video_buffer, apply_quantization, object_detector, objects_unificator,
                               main, main_layout):
    objects_each_frame = []
    for frame_index in range(len(video_buffer)):
        raw_frame = video_buffer[frame_index]
        quantizied_frame = None
        if apply_quantization:
            quantizied_frame = object_detector._prepare_image_for_detection(raw_frame)

        detected_objects = detect_objects(object_detector, raw_frame, quantizied_frame)
        objects_each_frame.append(detected_objects)
        draw_contours_on_image(object_detector, raw_frame)
        if quantizied_frame is not None:
            draw_contours_on_image(object_detector, quantizied_frame)

        objects_str = list_of_objects_to_string(detected_objects)
        main.video_buffer[frame_index] = [raw_frame, quantizied_frame, objects_str]

        tasksGUI.update_raw_image(main_layout, raw_frame)
        if quantizied_frame is not None:
            tasksGUI.update_quantization_image(main_layout, quantizied_frame)
        tasksGUI.print_on_console(main_layout, objects_str)
        object_detector.clear_contours()
    unified_objects = objects_unificator.unify_objects(objects_each_frame)
    main.unified_objects = unified_objects


def clear_frames_buffer(main):
    main.frames_buffer.clear()


def clear_video_buffer(main):
    main.video_buffer.clear()


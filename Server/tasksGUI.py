import tasks
import numpy as np
from kivy.clock import mainthread
from Common.TCPConnections import StreamMode


def single_two_images_mode_button_on_press(main, main_layout):
    if main.single_image_mode:
        main.single_image_mode = False
        main_layout.show_quantization_image()
    else:
        main.single_image_mode = True
        main_layout.hide_quantization_image()


def start_shutdown_agent_button_pressed(main):
    if main.is_agent_alive:
        tasks.shutdown_agent(main.tcp_client)
    else:
        tasks.start_agent()


def start_stop_stream_button_on_press(main):
    if main.is_stream_on:
        tasks.stop_stream(main.tcp_client)
    else:
        tasks.start_stream(main, main.tcp_client, main.main_layout)


@mainthread
def update_raw_image(main_layout, image):
    image = tasks.convert_cv2_image_to_kivy_texture(image)
    main_layout.update_raw_image_texture(image)


@mainthread
def update_quantization_image(main_layout, quantized_image):
    quantized_image = tasks.convert_cv2_image_to_kivy_texture(quantized_image)
    main_layout.update_quantized_image_texture(quantized_image)


def update_gui_after_registration(main_layout):
    main_layout.change_registered_label_text('Agent is registered')
    main_layout.change_start_shutdown_button_text('Shutdown agent')
    main_layout.enable_stream_button()
    main_layout.enable_stream_mode_spinner()
    main_layout.enable_apply_quantization_checkbox()


def update_gui_after_shutdown(main_layout):
    main_layout.change_registered_label_text('Agent is not registered')
    main_layout.change_start_shutdown_button_text('Start agent')
    main_layout.disable_stream_button()


def update_gui_after_stream_on(main, main_layout):
    if main.stream_mode == StreamMode.VIDEO:
        main_layout.disable_apply_quantization_checkbox()
        main_layout.disable_video_duration_text_input()
    main_layout.change_start_stop_stream_button_text('Stop stream')
    main_layout.disable_stream_mode_spinner()
    main_layout.disable_next_frame_button()
    main_layout.disable_previous_frame_button()


def update_gui_after_stream_off(main, main_layout, enable_frames_switching):
    main_layout.change_start_stop_stream_button_text('Start stream')
    main_layout.enable_stream_mode_spinner()

    if enable_frames_switching:
        main_layout.enable_previous_frame_button()

    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_apply_quantization_checkbox()
        main_layout.enable_video_duration_text_input()
        main_layout.enable_show_only_unified_objects_checkbox()


def stream_mode_button_on_text(main, main_layout):
    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_video_duration_text_input()
    elif main.stream_mode == StreamMode.EACH_FRAME:
        main_layout.disable_video_duration_text_input()


def print_on_console(main_layout, text):
    main_layout.print_on_console(text)


@mainthread
def previous_frame_button_on_press(main, main_layout):
    buffer = determine_buffer_for_switching_frames(main)
    if main.current_frame_index == len(buffer) - 1:
        main_layout.enable_next_frame_button()
    main.current_frame_index -= 1
    if main.current_frame_index == 0:
        main_layout.disable_previous_frame_button()
    update_gui_after_user_switched_frame(main, main_layout, buffer)


@mainthread
def next_frame_button_on_press(main, main_layout):
    buffer = determine_buffer_for_switching_frames(main)
    if main.current_frame_index == 0:
        main_layout.enable_previous_frame_button()
    main.current_frame_index += 1
    if main.current_frame_index == len(buffer) - 1:
        main_layout.disable_next_frame_button()
    update_gui_after_user_switched_frame(main, main_layout, buffer)


def determine_buffer_for_switching_frames(main):
    if main.stream_mode == StreamMode.EACH_FRAME:
        return main.frames_buffer
    if main.stream_mode == StreamMode.VIDEO:
        return main.video_buffer


def update_gui_after_user_switched_frame(main, main_layout, buffer):
    triple = buffer[main.current_frame_index]

    if isinstance(triple[0], np.ndarray):
        image = triple[0] = tasks.convert_cv2_image_to_kivy_texture(triple[0])
    else:
        image = triple[0]

    if isinstance(triple[1], np.ndarray):
        quantization_image = triple[1] = tasks.convert_cv2_image_to_kivy_texture(triple[1])
    else:
        quantization_image = triple[1]

    objects_string = triple[2]
    main_layout.update_raw_image_texture(image)
    if quantization_image is not None:
        main_layout.update_quantized_image_texture(quantization_image)
    main_layout.print_on_console(objects_string)


def show_only_unified_objects_checkbox(main, main_layout):
    pass


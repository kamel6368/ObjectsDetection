import numpy as np
from kivy.clock import mainthread

import tasks
from Common.TCPConnections import StreamMode


def image_mode_spinner_on_text(main_layout, mode):
    if mode == 'Raw Image':
        main_layout.show_raw_image()
    elif mode == 'Quantized image':
        main_layout.show_quantization_image()
    elif mode == 'Both images':
        main_layout.show_both_images()


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
    main_layout.disable_settings_button()
    main_layout.disable_distance_text_input()


def update_gui_after_stream_off(main, main_layout, enable_frames_switching):
    main_layout.change_start_stop_stream_button_text('Start stream')
    main_layout.enable_stream_mode_spinner()
    main_layout.enable_settings_button()
    main_layout.enable_distance_text_input()

    if enable_frames_switching:
        main_layout.enable_previous_frame_button()

    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_apply_quantization_checkbox()
        main_layout.enable_video_duration_text_input()
        main_layout.enable_show_only_unified_objects_checkbox()


def stream_mode_button_on_text(main, main_layout, show_only_unified_objects):
    tasks.change_stream_mode(main)
    update_gui_after_stream_mode_switch(main, main_layout, show_only_unified_objects)


def update_gui_after_video_done_recording(main_layout):
    main_layout.disable_stream_button()


def print_on_console(main_layout, text):
    main_layout.print_on_console(text)


@mainthread
def previous_frame_button_on_press(main, main_layout, show_only_unified_objects):
    buffer = determine_buffer_for_switching_frames(main)
    current_index = determine_current_index_for_switching_frames(main)
    current_index -= 1
    update_next_and_previous_frame_buttons(main_layout, buffer, current_index)
    update_current_index(main, current_index)
    update_gui_after_user_switched_frame(main_layout, buffer, current_index, show_only_unified_objects)


@mainthread
def next_frame_button_on_press(main, main_layout, show_only_unified_objects):
    buffer = determine_buffer_for_switching_frames(main)
    current_index = determine_current_index_for_switching_frames(main)
    current_index += 1
    update_next_and_previous_frame_buttons(main_layout, buffer, current_index)
    update_current_index(main, current_index)
    update_gui_after_user_switched_frame(main_layout, buffer, current_index, show_only_unified_objects)


def update_next_and_previous_frame_buttons(main_layout, buffer, current_index):
    if len(buffer) == 0:
        main_layout.disable_next_frame_button()
        main_layout.disable_previous_frame_button()
    elif current_index == 0:
        main_layout.disable_previous_frame_button()
        main_layout.enable_next_frame_button()
    elif 0 < current_index < len(buffer) - 1:
        main_layout.enable_previous_frame_button()
        main_layout.enable_next_frame_button()
    elif current_index == len(buffer) - 1:
        main_layout.enable_previous_frame_button()
        main_layout.disable_next_frame_button()


def determine_buffer_for_switching_frames(main):
    if main.stream_mode == StreamMode.EACH_FRAME:
        return main.frames_buffer
    if main.stream_mode == StreamMode.VIDEO:
        return main.video_buffer


def determine_current_index_for_switching_frames(main):
    if main.stream_mode == StreamMode.EACH_FRAME:
        return main.current_frame_index
    elif main.stream_mode == StreamMode.VIDEO:
        return main.current_video_index


def update_current_index(main, current_index):
    if main.stream_mode == StreamMode.EACH_FRAME:
        main.current_frame_index = current_index
    elif main.stream_mode == StreamMode.VIDEO:
        main.current_video_index = current_index


def update_gui_after_user_switched_frame(main_layout, buffer, current_index, show_only_unified_objects):
    if current_index < 0:
        set_raw_image_to_no_content(main_layout)
        set_quantized_image_to_no_content(main_layout)
        return

    triple = buffer[current_index]

    if isinstance(triple[0], np.ndarray):
        image = triple[0] = tasks.convert_cv2_image_to_kivy_texture(triple[0])
    else:
        image = triple[0]

    if isinstance(triple[1], np.ndarray):
        quantization_image = triple[1] = tasks.convert_cv2_image_to_kivy_texture(triple[1])
    else:
        quantization_image = triple[1]

    main_layout.update_raw_image_texture(image)
    if quantization_image is None:
        set_quantized_image_to_no_content(main_layout)
    else:
        main_layout.update_quantized_image_texture(quantization_image)

    if not show_only_unified_objects:
        print_objects_on_console(main_layout, buffer, current_index)


def print_objects_on_console(main_layout, buffer, current_index):
    main_layout.print_on_console(buffer[current_index][2])


def show_only_unified_objects_checkbox_on_state_change(main, main_layout, is_active):
    if is_active:
        objects_str = tasks.list_of_objects_with_certainty_factor_to_string(main.unified_objects)
        main_layout.print_on_console(objects_str)
    elif main.stream_mode == StreamMode.EACH_FRAME:
        print_objects_on_console(main_layout, main.frames_buffer, main.current_frame_index)
    elif main.stream_mode == StreamMode.VIDEO:
        print_objects_on_console(main_layout, main.video_buffer, main.current_video_index)


def update_gui_after_stream_mode_switch(main, main_layout, show_only_unified_objects):
    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_video_duration_text_input()
        main_layout.enable_show_only_unified_objects_checkbox()
        update_next_and_previous_frame_buttons(main_layout, main.video_buffer, main.current_video_index)
        update_gui_after_user_switched_frame(main_layout, main.video_buffer, main.current_video_index,
                                             show_only_unified_objects)
    elif main.stream_mode == StreamMode.EACH_FRAME:
        main_layout.disable_video_duration_text_input()
        main_layout.disable_show_only_unified_objects_checkbox()
        update_next_and_previous_frame_buttons(main_layout, main.frames_buffer, main.current_frame_index)
        update_gui_after_user_switched_frame(main_layout, main.frames_buffer, main.current_frame_index,
                                             show_only_unified_objects)


@mainthread
def set_quantized_image_to_no_content(main_layout):
    main_layout.update_quantized_image_source(no_content_image_path())


@mainthread
def set_raw_image_to_no_content(main_layout):
    main_layout.update_raw_image_source(no_content_image_path())


def no_content_image_path():
    return 'Resources/no_image.jpg'


@mainthread
def show_settings_view(screen_manager):
    screen_manager.transition.direction = 'left'
    screen_manager.current = 'SettingsScreen'


def get_distance(main_layout):
    dist_string = main_layout.get_distance()
    if len(dist_string) == 0:
        return 0.0
    return float(dist_string)

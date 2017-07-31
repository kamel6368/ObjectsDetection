import tasks
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
    image_texture = tasks.convert_cv2_image_to_kivy_texture(image)
    main_layout.update_raw_image_texture(image_texture)


@mainthread
def update_quantization_image(main_layout, quantized_image):
    image_texture = tasks.convert_cv2_image_to_kivy_texture(quantized_image)
    main_layout.update_quantized_image_texture(image_texture)


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


def update_gui_after_stream_off(main, main_layout):
    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_apply_quantization_checkbox()
        main_layout.enable_video_duration_text_input()
    main_layout.change_start_stop_stream_button_text('Start stream')
    main_layout.enable_stream_mode_spinner()


def stream_mode_button_on_text(main, main_layout):
    if main.stream_mode == StreamMode.VIDEO:
        main_layout.enable_video_duration_text_input()
    elif main.stream_mode == StreamMode.EACH_FRAME:
        main_layout.disable_video_duration_text_input()


def print_on_console(main_layout, text):
    main_layout.print_on_console(text)

def previous_frame_button_on_press(main, main_layout):
    main.current_frame -= 1
    if main.current_frame == 1:
        main_layout.disable_previous_frame_button()
    triple = main.frames_buffer[main.current_frame]
    image = triple[0]
    quantization_image = triple[1]
    objects_string = triple[2]
    main_layout.update_raw_image_texture(image)
    if quantization_image is not None:
        main_layout.update_quantization_image(quantization_image)
    main_layout.print_on_console(objects_string)

def next_frame_button_on_press():
    pass
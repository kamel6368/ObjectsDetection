from config import config
from Logger import Logger


def create_logger():
    console_print = config('Logger/console_print')
    file_print = config('Logger/file_print')
    logs_path = config('Logger/logs_path')
    return Logger(console_print, file_print, logs_path)

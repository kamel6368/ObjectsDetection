from datetime import datetime
import os


class Logger:

    def __init__(self, console_print=True, file_print=False, logs_path=None):
        self.console_print = console_print
        self.file_print = file_print
        self.logs_path = logs_path

    def print_msg(self, message):
        if len(message) > 100:
            message = message[:100]
        message = Logger._append_time_to_message(message)
        if self.file_print:
            file_name = Logger._assume_file_name()
            self._print_to_file(message, file_name, self.logs_path)

        if self.console_print:
            print message

    @staticmethod
    def _append_time_to_message(message):
        current_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        message = '[' + current_time + ']: ' + message
        return message

    @staticmethod
    def _print_to_file(log, file_name, file_path):
        file_name = file_path + file_name
        current_working_directory = os.path.dirname(os.getcwd())
        file_name = os.path.join(current_working_directory, file_name)
        with open(file_name, 'a') as log_file:
            log_file.write(log + '\n')

    @staticmethod
    def _assume_file_name():
        current_date_file_name = datetime.today().strftime('%d-%m-%Y')
        current_date_file_name += '.log'
        return current_date_file_name

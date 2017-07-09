
class Logger:

    def __init__(self, console_print=True, file_print=False, log_file=None):
        self.console_print = console_print
        self.file_print = file_print
        self.log_file = log_file

    def print_msg(self, message):
        if self.file_print:
            pass

        if self.console_print:
            if len(message) > 100:
                message = message[:100]
            print message


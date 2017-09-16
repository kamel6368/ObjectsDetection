import Common.config as general_param_loader
from kivy.uix.scrollview import ScrollView


class GeneralSettingsLayout(ScrollView):

    def __init__(self):
        super(GeneralSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = general_param_loader.get_yaml()
        self.ids.agent_address_form.value = str(yaml['TCPConnection']['agent_address'])
        self.ids.agent_port_form.value = str(yaml['TCPConnection']['agent_port'])
        self.ids.receive_address_form.value = str(yaml['TCPConnection']['receive_address'])
        self.ids.receive_port_form.value = str(yaml['TCPConnection']['receive_port'])
        self.ids.buffer_size_form.value = str(yaml['TCPConnection']['buffer_size'])
        self.ids.socket_timeout_form.value = str(yaml['TCPConnection']['socket_timeout'])

        self.ids.console_print_form.value = str(yaml['Logger']['console_print'])
        self.ids.file_print_form.value = str(yaml['Logger']['file_print'])
        self.ids.logs_path_form.value = str(yaml['Logger']['logs_path'])

        self.ids.frames_buffer_size_form.value = str(yaml['General']['frames_buffer_size'])

    def create_yaml(self):
        return {
            'TCPConnection': {
                'agent_address': self.ids.agent_address_form.value,
                'agent_port': int(self.ids.agent_port_form.value),
                'receive_address': self.ids.receive_address_form.value,
                'receive_port': int(self.ids.receive_port_form.value),
                'buffer_size': int(self.ids.buffer_size_form.value),
                'socket_timeout': float(self.ids.socket_timeout_form.value)
            },
            'Logger': {
                'console_print': True if self.ids.console_print_form.value == 'True' else False,
                'file_print': True if self.ids.file_print_form.value == 'True' else False,
                'logs_path': self.ids.logs_path_form.value
            },
            'General': {
                'frames_buffer_size': self.ids.frames_buffer_size_form.value
            }
        }

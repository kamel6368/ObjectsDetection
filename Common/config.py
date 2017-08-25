import yaml


def _file_path():
    return 'Resources/config.yaml'


def _default_file_path():
    return 'Resources/config_default.yaml'


def config(path, return_str=False):
    stream = open(_file_path(), 'r')
    dict = yaml.load(stream)

    keys = path.split('/')
    for key in keys:
        val = dict[key]
        dict = val
    if return_str:
        return str(val)
    return val


def get_yaml():
    with open(_file_path()) as stream:
        return yaml.load(stream)


def get_default_yaml():
    with open(_default_file_path()) as stream:
        return yaml.load(stream)


def save_yaml_to_file(yaml_to_save):
    with open(_file_path(), 'w') as stream:
        yaml.dump(yaml_to_save, stream, default_flow_style=False)

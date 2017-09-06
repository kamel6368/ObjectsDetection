import yaml


def _file_path():
    return 'Resources/objects_unification_params.yaml'


def _default_file_path():
    return 'Resources/objects_unification_params_default.yaml'


def load_all_from_file_for_similarity(similarity_calculator):

    similarity_calculator.color_weight = \
        yaml_lookup('similarity/color_weight')
    similarity_calculator.shape_weight = \
        yaml_lookup('similarity/shape_weight')
    similarity_calculator.size_weight = \
        yaml_lookup('similarity/size_weight')
    similarity_calculator.pattern_weight = \
        yaml_lookup('similarity/pattern_weight')
    similarity_calculator.symbols_weight = \
        yaml_lookup('similarity/symbols_weight')
    similarity_calculator.parts_weight = \
        yaml_lookup('similarity/parts_weight')


def load_all_from_file_for_unification(objects_unificator):

    objects_unificator.min_similarity_factor = yaml_lookup('unification/min_similarity_factor')
    objects_unificator.min_connection_length_percentage = yaml_lookup('unification/min_connection_length_percentage')
    work_on_copy = yaml_lookup('unification/work_on_copy')
    objects_unificator.work_on_copy = True if work_on_copy == 'True' else False


def yaml_lookup(path, return_str=False):
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

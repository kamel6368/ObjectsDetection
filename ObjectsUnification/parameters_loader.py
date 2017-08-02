import yaml


def load_all_from_file_for_similarity(similarity_calculator):

    similarity_calculator.color_weight = \
        _yaml_lookup('similarity/color_weight')
    similarity_calculator.shape_weight = \
        _yaml_lookup('similarity/shape_weight')
    similarity_calculator.size_weight = \
        _yaml_lookup('similarity/size_weight')
    similarity_calculator.pattern_weight = \
        _yaml_lookup('similarity/pattern_weight')
    similarity_calculator.symbols_weight = \
        _yaml_lookup('similarity/symbols_weight')
    similarity_calculator.parts_weight = \
        _yaml_lookup('similarity/parts_weight')


def load_all_from_file_for_unification(objects_unificator):

    objects_unificator.min_similarity_factor = \
        _yaml_lookup('unification/min_similarity_factor')
    work_on_copy = _yaml_lookup('unification/work_on_copy')
    objects_unificator.work_on_copy = True if work_on_copy == 'True' else False


def _yaml_lookup(path):
    stream = open('Resources/objects_unification_params.yaml', 'r')
    dict = yaml.load(stream)
    keys = path.split('/')
    for key in keys:
        val = dict[key]
        dict = val
    return val

import ObjectsUnification.parameters_loader as unif_param_loader
from kivy.uix.scrollview import ScrollView


class UnificationSettingsLayout(ScrollView):

    def __init__(self):
        super(UnificationSettingsLayout, self).__init__()
        self.set_params_from_file()

    def set_params_from_file(self, yaml=None):
        if yaml is None:
            yaml = unif_param_loader.get_yaml()
        self.ids.color_weight_form.value = str(yaml['similarity']['color_weight'])
        self.ids.shape_weight_form.value = str(yaml['similarity']['shape_weight'])
        self.ids.size_weight_form.value = str(yaml['similarity']['size_weight'])
        self.ids.pattern_weight_form.value = str(yaml['similarity']['pattern_weight'])
        self.ids.symbols_weight_form.value = str(yaml['similarity']['symbols_weight'])
        self.ids.parts_weight_form.value = str(yaml['similarity']['parts_weight'])
        self.ids.min_similarity_factor_form.value = str(yaml['unification']['min_similarity_factor'])
        self.ids.min_connection_length_percentage_form.value = str(yaml['unification']['min_connection_length_percentage'])
        self.ids.work_on_copy_form.value = str(yaml['unification']['work_on_copy'])

    def create_yaml(self):
        return {
            'similarity': {
                'color_weight': float(self.ids.color_weight_form.value),
                'shape_weight': float(self.ids.shape_weight_form.value),
                'size_weight': float(self.ids.size_weight_form.value),
                'pattern_weight': float(self.ids.pattern_weight_form.value),
                'symbols_weight': float(self.ids.symbols_weight_form.value),
                'parts_weight': float(self.ids.parts_weight_form.value)
            },
            'unification': {
                'min_similarity_factor': float(self.ids.min_similarity_factor_form.value),
                'min_connection_length_percentage': float(self.ids.min_connection_length_percentage_form.value),
                'work_on_copy': True if self.ids.work_on_copy_form.value == 'True' else False
            }
        }


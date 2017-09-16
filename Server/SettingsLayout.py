import ImageProcessing.parameters_loader as img_proc_param_loader
import ObjectsUnification.parameters_loader as unif_param_loader
import Common.config as general_param_loader
import configurable_objects_factory
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from Layouts.GeneralSettingsLayout import GeneralSettingsLayout
from Layouts.ImageProcessingSettingsLayout import ImageProcessingSettingsLayout
from Layouts.UnificationSettingsLayout import UnificationSettingsLayout


class SettingsLayout(Screen):

    def __init__(self, screen_manager, main, name=None):
        self.screen_manager = screen_manager
        self.current_settings = None
        self.main = main
        super(SettingsLayout, self).__init__(name=name)
        self.ids.image_processing_settings_button.state = 'down'
        self._image_processing_button_on_press()

    ############################################
    # buttons callbacks
    ############################################

    def _back_button_on_press(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'MainScreen'

    def _image_processing_button_on_press(self):
        self.ids.objects_unification_settings_button.state = 'normal'
        self.ids.general_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = ImageProcessingSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _unification_button_on_press(self):
        self.ids.image_processing_settings_button.state = 'normal'
        self.ids.general_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = UnificationSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _general_button_on_press(self):
        self.ids.image_processing_settings_button.state = 'normal'
        self.ids.objects_unification_settings_button.state = 'normal'
        self.ids.settings_holder.clear_widgets()
        self.current_settings = GeneralSettingsLayout()
        self.ids.settings_holder.add_widget(self.current_settings)

    def _save_button_on_press(self):
        try:
            if isinstance(self.current_settings, ImageProcessingSettingsLayout):
                img_proc_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                self.main.object_detector = configurable_objects_factory.create_object_detector()
                self._show_saved_popup()
            elif isinstance(self.current_settings, UnificationSettingsLayout):
                unif_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                self.main.objects_unificator = configurable_objects_factory.create_objects_unificator()
                self._show_saved_popup()
            elif isinstance(self.current_settings, GeneralSettingsLayout):
                general_param_loader.save_yaml_to_file(self.current_settings.create_yaml())
                popup = Popup(title='Please restart application', content=Label(text='To apply changes please restart application'),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
        except Exception as e:
            popup = Popup(title='Error',content=Label(text=e.message), size_hint=(None, None), size=(400, 400))
            popup.open()


    def _show_saved_popup(self):
        popup = Popup(title='Saved',
                      content=Label(text='Saved'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def _set_to_default_button_on_press(self):
        if isinstance(self.current_settings, ImageProcessingSettingsLayout):
            default_yaml = img_proc_param_loader.get_default_yaml()
        elif isinstance(self.current_settings, UnificationSettingsLayout):
            default_yaml = unif_param_loader.get_default_yaml()
        elif isinstance(self.current_settings, GeneralSettingsLayout):
            default_yaml = general_param_loader.get_default_yaml()
        self.current_settings.set_params_from_file(default_yaml)

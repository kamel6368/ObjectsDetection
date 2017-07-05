from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):

    single_image = False
    quantization_image = None

    def __init__(self):
        super(MainLayout, self).__init__()
        self.quantization_image = self.ids.quantization_image

    def switch_single_two_images(self):
        if self.single_image:
            self.single_image = False
            self.ids.images_container.add_widget(self.quantization_image)
        else:
            self.single_image = True
            self.ids.images_container.remove_widget(self.quantization_image)

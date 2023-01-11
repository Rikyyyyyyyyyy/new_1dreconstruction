from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty
import Reconstruct as rc
Builder.load_file('kv_set.kv')

class FileChoosePopup(Popup):
    load = ObjectProperty()

class MyStackLayout(StackLayout):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    FilePath  = None
    Modulation = None
    AcquisitionRate = None

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.get_file.text = self.file_path

    def callback(self):
        self.Modulation = self.ids.moInput.text
        self.AcquisitionRate = self.ids.acInput.text
        running_info = rc.runReconstruct(self.file_path,self.Modulation,self.AcquisitionRate)
        popup = Popup(title='Result Info',content=Label(text=running_info),size_hint=(None, None), size=(400, 400))
        popup.open()
        return 
    


class Reconstruct(App):
    def build(self):
        self.window = GridLayout()
        #add widgets to window
        self.window.cols =1 
        self.window.add_widget(Image(source = "tmic_logo.png"))
        return MyStackLayout()
   

if __name__ == "__main__":
    Window.clearcolor = (1, 1, 1, 1)
    Reconstruct().run()




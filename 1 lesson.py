from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDBoxLayout:
    orientation: "vertical"
    spacing: "10dp"

    MDLabel:
        text: "Привет, KivyMD!"
        halign: "center"
        theme_text_color: "Primary"
        font_style: "H4"

    MDRaisedButton:
        text: "Нажми меня"
        pos_hint: {"center_x": 0.5}
'''

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

MyApp().run()
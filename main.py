from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText


class MainApp(MDApp):
    def build(self):
        screen = MDScreen()

        # Текст
        label = MDLabel(
            text="Привет, KivyMD!",
            halign="center",
            theme_text_color="Primary",
            font_style="Display",
            pos_hint={"center_y": 0.7}
        )

        # Кнопка
        button = MDButton(
            MDButtonText(text="Нажми меня"),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        button.bind(on_release=lambda x: print("Кнопка нажата!"))
        button1 = MDButton(
            MDButtonText(text="Вторая кнопка"),
            pos_hint={"center_x": 0.5, "center_y": 0.4}
        )
        button1.bind(on_release=lambda x: print("Вторая кнопка нажата!"))

        screen.add_widget(label)
        screen.add_widget(button)
        screen.add_widget(button1)
        return screen


MainApp().run()
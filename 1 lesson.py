from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon
from kivymd.uix.scrollview import MDScrollView


class NotesApp(MDApp):
    def build(self):
        self.screen = MDScreen()

        # Поле ввода
        self.text_field = MDTextField(
            hint_text="Введите заметку",
            mode="outlined",
            pos_hint={"center_x": 0.5, "top": 0.85},
            size_hint_x=0.8,
        )
        self.text_field.helper_text_color_normal = (0, 0, 0, 1)

        # Кнопка
        add_button = MDButton(
            MDButtonText(text="Добавить"),
            pos_hint={"center_x": 0.5, "top": 0.7},
            size_hint_x=0.8,
        )
        add_button.bind(on_release=self.add_note)

        # Список заметок
        self.note_list = MDList()
        scroll = MDScrollView(
            self.note_list,
            pos_hint={"center_x": 0.5, "top": 0.7},
            size_hint=(0.8, 0.6),
        )

        self.screen.add_widget(self.text_field)
        self.screen.add_widget(add_button)
        self.screen.add_widget(scroll)

        return self.screen

    def add_note(self, *args):
        text = self.text_field.text.strip()
        if text:
            list_item = MDListItem(
                MDListItemLeadingIcon(icon="note-text-outline"),  # можно убрать
                MDListItemHeadlineText(text=text),
                on_release=lambda x: print(f"Выбрано: {text}")
            )
            self.note_list.add_widget(list_item)
            self.text_field.text = ""


NotesApp().run()
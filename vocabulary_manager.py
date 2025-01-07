import json
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window


class VocabularyManager:
    def __init__(self, filename="vocabulary.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add_word(self, word, translation, example, example_translation):
        entry = {
            "word": word,
            "translation": translation,
            "example": example,
            "example_translation": example_translation
        }
        self.data.append(entry)
        self.save_data()

    def get_words(self):
        return self.data


class VocabularyApp(App):
    def build(self):
        Window.size = (900, 700)  # Размер окна
        self.manager = VocabularyManager()

        self.root = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # Добавление кнопки для добавления слова
        self.add_button = Button(text="Добавить слово", size_hint=(1, None), height=70, background_normal='', background_color=(0.2, 0.6, 0.8, 1), font_size=26, bold=True)
        self.add_button.bind(on_press=self.show_add_word_popup)
        self.root.add_widget(self.add_button)

        # Кнопка для отображения слов
        self.display_button = Button(text="Показать слова", size_hint=(1, None), height=70, background_normal='', background_color=(0.2, 0.6, 0.8, 1), font_size=26, bold=True)
        self.display_button.bind(on_press=self.show_words)
        self.root.add_widget(self.display_button)

        # Кнопка выхода
        self.exit_button = Button(text="Выход", size_hint=(1, None), height=70, background_normal='', background_color=(0.8, 0.2, 0.2, 1), font_size=26, bold=True)
        self.exit_button.bind(on_press=self.stop)
        self.root.add_widget(self.exit_button)

        return self.root

    def show_add_word_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical', spacing=20, padding=20)

        self.word_input = TextInput(hint_text="Введите английское слово", size_hint=(1, None), height=50, multiline=False, font_size=22)
        self.translation_input = TextInput(hint_text="Введите перевод", size_hint=(1, None), height=50, multiline=False, font_size=22)
        self.example_input = TextInput(hint_text="Введите пример на английском", size_hint=(1, None), height=50, multiline=True, font_size=22)
        self.example_translation_input = TextInput(hint_text="Перевод примера", size_hint=(1, None), height=50, multiline=True, font_size=22)

        save_button = Button(text="Сохранить", size_hint=(1, None), height=70, background_normal='', background_color=(0.2, 0.8, 0.2, 1), font_size=26, bold=True)
        save_button.bind(on_press=self.add_word)

        popup_content.add_widget(self.word_input)
        popup_content.add_widget(self.translation_input)
        popup_content.add_widget(self.example_input)
        popup_content.add_widget(self.example_translation_input)
        popup_content.add_widget(save_button)

        self.popup = Popup(title="Добавить слово", content=popup_content, size_hint=(0.8, 0.8))
        self.popup.open()

    def add_word(self, instance):
        word = self.word_input.text
        translation = self.translation_input.text
        example = self.example_input.text
        example_translation = self.example_translation_input.text

        if not all([word, translation, example, example_translation]):
            return

        self.manager.add_word(word, translation, example, example_translation)
        self.popup.dismiss()

    def show_words(self, instance):
        words = self.manager.get_words()

        if not words:
            popup = Popup(title="Словарь пуст", content=Label(text="В словаре пока нет слов."), size_hint=(0.6, 0.4))
            popup.open()
            return

        # Используем ScrollView для прокрутки длинного списка
        scroll_layout = BoxLayout(orientation='vertical', padding=20, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        for i, entry in enumerate(words, 1):
            word_label = Label(
                text=f"{i}. {entry['word']} - {entry['translation']}",
                size_hint_y=None,
                height=80,  # Увеличиваем высоту строки
                font_size=28,  # Увеличиваем размер шрифта
                color=(0.2, 0.6, 0.8, 1)  # Цвет текста
            )
            example_label = Label(
                text=f"   Пример: {entry['example']}",
                size_hint_y=None,
                height=80,  # Увеличиваем высоту строки
                font_size=24,  # Увеличиваем размер шрифта
                color=(0.4, 0.4, 0.4, 1)  # Цвет текста
            )
            example_translation_label = Label(
                text=f"   Перевод: {entry['example_translation']}",
                size_hint_y=None,
                height=80,  # Увеличиваем высоту строки
                font_size=24,  # Увеличиваем размер шрифта
                color=(0.4, 0.4, 0.4, 1)  # Цвет текста
            )

            scroll_layout.add_widget(word_label)
            scroll_layout.add_widget(example_label)
            scroll_layout.add_widget(example_translation_label)

        # Оборачиваем наш контейнер в ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(scroll_layout)

        self.popup = Popup(title="Список слов", content=scroll_view, size_hint=(0.8, 0.8))
        self.popup.open()


if __name__ == "__main__":
    VocabularyApp().run()


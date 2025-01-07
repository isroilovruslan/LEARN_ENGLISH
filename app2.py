import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

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
        return f"Слово '{word}' успешно добавлено!"

    def get_words(self):
        return self.data

class VocabularyApp:
    def __init__(self, root):
        self.manager = VocabularyManager()
        self.root = root
        self.root.title("Vocabulary Manager")

        # Add Word Button
        self.add_button = tk.Button(root, text="Добавить слово", command=self.add_word)
        self.add_button.pack(pady=5)

        # Display Words Button
        self.display_button = tk.Button(root, text="Показать слова", command=self.display_words)
        self.display_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(root, text="Выход", command=root.quit)
        self.exit_button.pack(pady=5)

    def add_word(self):
        word = simpledialog.askstring("Добавить слово", "Введите английское слово:")
        if not word:
            return

        translation = simpledialog.askstring("Добавить перевод", "Введите перевод слова:")
        if not translation:
            return

        example = simpledialog.askstring("Добавить пример", "Введите пример использования на английском:")
        if not example:
            return

        example_translation = simpledialog.askstring("Добавить перевод примера", "Введите перевод примера на русском:")
        if not example_translation:
            return

        message = self.manager.add_word(word, translation, example, example_translation)
        messagebox.showinfo("Успех", message)

    def display_words(self):
        words = self.manager.get_words()
        if not words:
            messagebox.showinfo("Словарь пуст", "В словаре пока нет слов.")
            return

        display_window = tk.Toplevel(self.root)
        display_window.title("Список слов")

        text = tk.Text(display_window, wrap=tk.WORD, width=50, height=20)
        text.pack(expand=True, fill=tk.BOTH)

        for i, entry in enumerate(words, 1):
            text.insert(tk.END, f"{i}. {entry['word']} - {entry['translation']}\n")
            text.insert(tk.END, f"   Пример: {entry['example']}\n")
            text.insert(tk.END, f"   Перевод: {entry['example_translation']}\n\n")
        text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()

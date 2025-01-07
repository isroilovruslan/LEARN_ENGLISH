import json
import os
import random
import pyttsx3
from guess_word import GuessWord
from gtts import gTTS





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

    def add_word(self):
        word = input("Введите английское слово: ").strip()
        translation = input("Введите перевод слова: ").strip()
        example = input("Введите пример использования на английском: ").strip()
        example_translation = input("Введите перевод примера на русском: ").strip()
        entry = {
            "word": word,
            "translation": translation,
            "example": example,
            "example_translation": example_translation
        }
        self.data.append(entry)
        self.save_data()
        print(f"\nСлово '{word}' успешно добавлено!\n")

    def display_words(self):
        if not self.data:
            print("\nСловарь пуст!\n")
            return

        print("\nТекущие слова в словаре:\n")
        for i, entry in enumerate(self.data, 1):
            print(f"{i}. {entry['word']} - {entry['translation']}\n   Пример: {entry['example']}\n   Перевод: {entry['example_translation']}\n")



class WordPractice:
    def __init__(self):
        self.words = VocabularyManager()
        self.data = self.words.data
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 130)  # Устанавливаем скорость речи


    def random_word(self):
        while True:
            # Случайный выбор слова
            result = random.choice(self.data)
            print(f"\nСлово: {result['word']} - {result['translation']}")
            print(f"Пример: {result['example']}")
            print(f"Перевод примера: {result['example_translation']}")

            # Озвучиваем слово
            self.engine.say(result['word'])
            self.engine.runAndWait()

            # Опции для пользователя
            while True:
                print("\n[1] Повторить озвучивание")
                print("[2] Показать новое слово")
                print("[3] Выход")
                choice = input("Выберите действие: ")

                if choice == '1':
                    # Повторное озвучивание
                    self.engine.say(result['word'])
                    self.engine.runAndWait()
                elif choice == '2':
                    # Выход из внутреннего цикла для выбора нового слова
                    break
                elif choice == '3':
                    # Завершение программы
                    print("Выход из программы.")
                    return
                else:
                    print("Некорректный выбор. Попробуйте снова.")


manager = VocabularyManager()
voise_of_word = WordPractice()
manager2 = GuessWord()


funcs = {'1': manager.add_word,
         '2': manager.display_words,
         '3': voise_of_word.random_word,
         '4': manager2.play_game}

while True:
    print("\nМеню:")
    print("1. Добавить слово")
    print("2. Показать слова")
    print("3. Рандомное слово")
    print("4. Угадай слова")
    print('5. Выход')

    choice = input("Введите номер действия: ").strip()

    if choice.isdigit() and choice in funcs:
        funcs[choice]()

    elif choice == "5":
        print("\nДо свидания!")
        break
    else:
        print("\nПожалуйста, выберите корректное действие!\n")





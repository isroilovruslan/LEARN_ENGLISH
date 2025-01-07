import random


class GuessWord:
    def __init__(self):
        self.words = None

    def load_words(self):
        from main import VocabularyManager
        self.words = VocabularyManager()

    def check_answer(self, user_input, correct_word):
        """
        Проверяет ответ пользователя.
        Возвращает True, если ответ верный, и False в противном случае.
        """
        if user_input.lower() == correct_word:
            print('Правильно!')
            return True
        else:
            print('Неправильно, попробуйте снова!')
            return False

    def play_game(self):
        if self.words is None:
            self.load_words()

        print("Добро пожаловать в игру 'Угадай слово'!")
        print('Для завершения игры отправьте "1".\n')

        while True:
            random_obj = random.choice(self.words.data)
            word = random_obj.get('word', '')
            translation = random_obj.get('translation', '').upper()
            example = random_obj.get('example', 'Пример отсутствует.')
            example_translation = random_obj.get('example_translation', 'Перевод примера отсутствует.')

            print(f'Как переводится слово "{translation}": ')

            while True:
                user_input = input('--> ')
                if user_input == '1':
                    print('Игра окончена. Спасибо за игру!')
                    return
                if self.check_answer(user_input, word):
                    print(f'Пример использования: {example}')
                    print(f'Перевод примера: {example_translation}\n')
                    break

            continue_game = input('Хотите продолжить игру? (да/нет): ').strip().lower()
            if continue_game not in ['да', 'yes']:
                print('Спасибо за игру! До встречи!')
                break

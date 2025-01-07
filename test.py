import re

# 1. Исключение для неверного домена
class DomainException(Exception):
    pass

# 2. Класс для работы с доменами
class Domain:
    # Конструктор принимает строку с доменом
    def __init__(self, domain):
        self.domain = domain
        if not self.is_valid_domain(domain):
            raise DomainException('Недопустимый домен, url или email')

    # Метод для проверки корректности домена
    def is_valid_domain(self, domain):
        return bool(re.match(r'^[a-zA-Z]+\.[a-zA-Z]+$', domain))

    # Метод для создания экземпляра на основе URL
    @classmethod
    def from_url(cls, url):
        match = re.match(r'https?://([a-zA-Z]+\.[a-zA-Z]+)', url)
        if match:
            return cls(match.group(1))
        else:
            raise DomainException('Недопустимый домен, url или email')

    # Метод для создания экземпляра на основе email
    @classmethod
    def from_email(cls, email):
        match = re.match(r'[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+', email)
        if match:
            domain = email.split('@')[1]
            return cls(domain)
        else:
            raise DomainException('Недопустимый домен, url или email')

    # Метод для строкового представления
    def __str__(self):
        return self.domain



emails = ['anan,i86@example.org', 'konovalovkondrat@@example.net', 'efimmaksimov@example..net', 'marfa_.04@example.com',
          'vlasovstanimir@example.org.', '.anikita_04@example.net', '@loginovroman@example.org', 'abc@@mail.ru',
          'novikovasinklitikija@example.net@', 'elizar_1978@example@.com', 'kasjan_1972@example.org', '@a.ru', 'abc@.ru']

for email in emails:
    try:
        domain = Domain.from_email(email)
    except DomainException as e:
        print(e)
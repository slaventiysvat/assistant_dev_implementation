import re
from datetime import datetime
from typing import Optional


class Field:
    """Базовий клас для всіх полів з базовою валідацією"""
    
    def __init__(self, value: str):
        """
        Ініціалізує поле з валідацією
        
        Args:
            value (str): Значення поля
            
        Raises:
            ValueError: Якщо значення не пройшло валідацію
        """
        self.value = self.validate(value)

    def validate(self, value: str) -> str:
        """
        Базова валідація - перевіряє, що значення не порожнє
        
        Args:
            value (str): Значення для валідації
            
        Returns:
            str: Валідоване значення
            
        Raises:
            ValueError: Якщо значення порожнє
        """
        if not value or not value.strip():
            raise ValueError("Поле не може бути порожнім")
        return value.strip()

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.value}')"


class Name(Field):
    """Клас для валідації імен"""
    
    def validate(self, value: str) -> str:
        """
        Валідація імені - має містити тільки літери та пробіли
        
        Args:
            value (str): Ім'я для валідації
            
        Returns:
            str: Валідоване ім'я
            
        Raises:
            ValueError: Якщо ім'я містить недопустимі символи
        """
        value = super().validate(value)
        
        # Перевіряємо, що ім'я містить тільки літери, пробіли, дефіси та апострофи
        if not re.match(r"^[a-zA-Zа-яА-ЯіІїЇєЄ'\s\-]+$", value):
            raise ValueError("Ім'я може містити тільки літери, пробіли, дефіси та апострофи")
        
        return value.title()  # Приводимо до формату Title Case

class Phone(Field):
    """Клас для валідації телефонних номерів"""
    
    def validate(self, value: str) -> str:
        """
        Валідація телефонного номера
        Підтримує формати: +380XXXXXXXXX, 380XXXXXXXXX, 0XXXXXXXXX
        
        Args:
            value (str): Номер телефону для валідації
            
        Returns:
            str: Нормалізований номер телефону
            
        Raises:
            ValueError: Якщо номер телефону має неправильний формат
        """
        value = super().validate(value)
        
        # Видаляємо всі не-цифрові символи крім +
        cleaned = re.sub(r'[^\d+]', '', value)
        
        # Різні формати українських номерів
        patterns = [
            r'^\+380\d{9}$',      # +380XXXXXXXXX
            r'^380\d{9}$',        # 380XXXXXXXXX  
            r'^0\d{9}$'           # 0XXXXXXXXX
        ]
        
        if not any(re.match(pattern, cleaned) for pattern in patterns):
            raise ValueError("Неправильний формат номера телефону. Використовуйте: +380XXXXXXXXX, 380XXXXXXXXX або 0XXXXXXXXX")
        
        # Нормалізуємо до формату +380XXXXXXXXX
        if cleaned.startswith('0'):
            cleaned = '+38' + cleaned
        elif cleaned.startswith('380'):
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+380'):
            cleaned = '+380' + cleaned
            
        return cleaned


class Email(Field):
    """Клас для валідації email адрес"""
    
    def validate(self, value: str) -> str:
        """
        Валідація email адреси
        
        Args:
            value (str): Email для валідації
            
        Returns:
            str: Валідований email (у нижньому регістрі)
            
        Raises:
            ValueError: Якщо email має неправильний формат
        """
        value = super().validate(value)
        
        # Базова перевірка email за допомогою regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError("Неправильний формат email адреси")
            
        return value.lower()


class Birthday(Field):
    """Клас для валідації дат народження"""
    
    def validate(self, value: str) -> str:
        """
        Валідація дати народження
        Підтримує формати: DD.MM.YYYY, DD-MM-YYYY, DD/MM/YYYY
        
        Args:
            value (str): Дата народження для валідації
            
        Returns:
            str: Нормалізована дата у форматі DD.MM.YYYY
            
        Raises:
            ValueError: Якщо дата має неправильний формат або є у майбутньому
        """
        value = super().validate(value)
        
        # Список підтримуваних форматів
        date_formats = ['%d.%m.%Y', '%d-%m-%Y', '%d/%m/%Y']
        
        parsed_date = None
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(value, date_format)
                break
            except ValueError:
                continue
        
        if parsed_date is None:
            raise ValueError("Неправильний формат дати. Використовуйте DD.MM.YYYY, DD-MM-YYYY або DD/MM/YYYY")
        
        # Перевіряємо, що дата не у майбутньому
        if parsed_date.date() > datetime.now().date():
            raise ValueError("Дата народження не може бути у майбутньому")
        
        # Перевіряємо, що дата не занадто давня (наприклад, не більше 150 років тому)
        if (datetime.now() - parsed_date).days > 150 * 365:
            raise ValueError("Дата народження занадто давня")
        
        return parsed_date.strftime('%d.%m.%Y')

    def to_date(self) -> datetime:
        """
        Конвертує дату з рядка у datetime об'єкт
        
        Returns:
            datetime: Дата як datetime об'єкт
        """
        return datetime.strptime(self.value, '%d.%m.%Y')


class Address(Field):
    """Клас для валідації адрес"""
    
    def validate(self, value: str) -> str:
        """
        Валідація адреси - базова перевірка на мінімальну довжину
        
        Args:
            value (str): Адреса для валідації
            
        Returns:
            str: Валідована адреса
            
        Raises:
            ValueError: Якщо адреса занадто коротка
        """
        value = super().validate(value)
        
        if len(value) < 5:
            raise ValueError("Адреса занадто коротка (мінімум 5 символів)")
            
        return value
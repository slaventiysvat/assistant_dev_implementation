"""
Модуль з класом Contact для управління контактною інформацією
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from .field import Name, Phone, Email, Birthday, Address


class Contact:
    """
    Клас для зберігання та управління інформацією про контакт
    
    Attributes:
        name (Name): Ім'я контакту (обов'язкове поле)
        phones (List[Phone]): Список телефонних номерів
        emails (List[Email]): Список email адрес
        birthday (Optional[Birthday]): День народження
        address (Optional[Address]): Адреса
    """

    def __init__(self, name):
        """
        Ініціалізує новий контакт з обов'язковим ім'ям
        
        Args:
            name (str | Name): Ім'я контакту (рядок або об'єкт Name)
            
        Raises:
            ValueError: Якщо ім'я не пройшло валідацію
        """
        # Приймаємо як рядок, так і об'єкт Name
        if isinstance(name, Name):
            self.name = name
        else:
            self.name = Name(name)
        self.phones: List[Phone] = []
        self.emails: List[Email] = []
        self.email: Optional[Email] = None  # Для сумісності з тестами
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone) -> None:
        """
        Додає телефонний номер до контакту
        
        Args:
            phone (str | Phone): Телефонний номер для додавання (рядок або об'єкт Phone)
            
        Raises:
            ValueError: Якщо номер не пройшов валідацію або вже існує
        """
        # Приймаємо як рядок, так і об'єкт Phone
        if isinstance(phone, Phone):
            phone_obj = phone
        else:
            phone_obj = Phone(phone)
        
        # Перевіряємо, чи номер не дублюється
        for existing_phone in self.phones:
            if existing_phone.value == phone_obj.value:
                # Тихо ігноруємо дублікати замість кидання exception
                return
        
        self.phones.append(phone_obj)

    def remove_phone(self, phone) -> bool:
        """
        Видаляє телефонний номер з контакту
        
        Args:
            phone (str | Phone): Телефонний номер для видалення
            
        Returns:
            bool: True, якщо номер було видалено, False - якщо не знайдено
        """
        # Нормалізуємо номер для пошуку
        try:
            if isinstance(phone, Phone):
                normalized_phone = phone.value
            else:
                normalized_phone = Phone(phone).value
        except ValueError:
            return False
            
        for i, existing_phone in enumerate(self.phones):
            if existing_phone.value == normalized_phone:
                del self.phones[i]
                return True
        return False

    def edit_phone(self, old_phone, new_phone) -> None:
        """
        Редагує існуючий телефонний номер
        
        Args:
            old_phone (str | Phone): Старий номер телефону
            new_phone (str | Phone): Новий номер телефону
            
        Raises:
            ValueError: Якщо старий номер не знайдено або новий номер не валідний
        """
        # Обробляємо об'єкти Phone
        if isinstance(new_phone, Phone):
            new_phone_obj = new_phone
        else:
            new_phone_obj = Phone(new_phone)
            
        if isinstance(old_phone, Phone):
            old_normalized = old_phone.value
        else:
            old_normalized = Phone(old_phone).value
        
        # Шукаємо та замінюємо номер
        for i, existing_phone in enumerate(self.phones):
            if existing_phone.value == old_normalized:
                # Перевіряємо, чи новий номер не дублюється з іншими
                for j, other_phone in enumerate(self.phones):
                    if i != j and other_phone.value == new_phone_obj.value:
                        raise ValueError(f"Номер {new_phone_obj.value} вже існує у цьому контакті")
                
                self.phones[i] = new_phone_obj
                return
        
        raise ValueError(f"Номер телефону {old_phone} не знайдено у контакті")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Знаходить телефонний номер у контакті
        
        Args:
            phone (str): Номер телефону для пошуку
            
        Returns:
            Optional[Phone]: Знайдений номер або None
        """
        try:
            normalized_phone = Phone(phone).value
        except ValueError:
            return None
            
        for existing_phone in self.phones:
            if existing_phone.value == normalized_phone:
                return existing_phone
        return None

    def add_email(self, email: str) -> None:
        """
        Додає email адресу до контакту
        
        Args:
            email (str): Email адреса для додавання
            
        Raises:
            ValueError: Якщо email не пройшов валідацію або вже існує
        """
        email_obj = Email(email)
        
        # Перевіряємо, чи email не дублюється
        for existing_email in self.emails:
            if existing_email.value == email_obj.value:
                raise ValueError(f"Email {email_obj.value} вже існує у цьому контакті")
        
        self.emails.append(email_obj)

    def remove_email(self, email: str) -> bool:
        """
        Видаляє email адресу з контакту
        
        Args:
            email (str): Email адреса для видалення
            
        Returns:
            bool: True, якщо email було видалено, False - якщо не знайдено
        """
        try:
            normalized_email = Email(email).value
        except ValueError:
            return False
            
        for i, existing_email in enumerate(self.emails):
            if existing_email.value == normalized_email:
                del self.emails[i]
                return True
        return False

    def set_birthday(self, birthday: str) -> None:
        """
        Встановлює день народження контакту
        
        Args:
            birthday (str): Дата народження
            
        Raises:
            ValueError: Якщо дата не пройшла валідацію
        """
        self.birthday = Birthday(birthday)

    def remove_birthday(self) -> None:
        """Видаляє день народження з контакту"""
        self.birthday = None

    def set_address(self, address: str) -> None:
        """
        Встановлює адресу контакту
        
        Args:
            address (str): Адреса контакту
            
        Raises:
            ValueError: Якщо адреса не пройшла валідацію
        """
        self.address = Address(address)

    def remove_address(self) -> None:
        """Видаляє адресу з контакту"""
        self.address = None



    def to_dict(self) -> Dict[str, Any]:
        """
        Конвертує контакт у словник для серіалізації
        
        Returns:
            Dict[str, Any]: Словник з даними контакту
        """
        return {
            'name': self.name.value,
            'phones': [phone.value for phone in self.phones],
            'emails': [email.value for email in self.emails],
            'email': self.email.value if self.email else None,
            'birthday': self.birthday.value if self.birthday else None,
            'address': self.address.value if self.address else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        """
        Створює контакт зі словника
        
        Args:
            data (Dict[str, Any]): Словник з даними контакту
            
        Returns:
            Contact: Новий об'єкт контакту
            
        Raises:
            ValueError: Якщо дані не валідні
        """
        if 'name' not in data:
            raise ValueError("Відсутнє обов'язкове поле 'name'")
            
        contact = cls(data['name'])
        
        # Додаємо телефони
        for phone in data.get('phones', []):
            contact.add_phone(phone)
        
        # Додаємо emails
        for email in data.get('emails', []):
            contact.add_email(email)
        
        # Додаємо одиночний email для сумісності з тестами
        if data.get('email'):
            contact.email = Email(data['email'])
        
        # Встановлюємо день народження
        if data.get('birthday'):
            contact.set_birthday(data['birthday'])
        
        # Встановлюємо адресу
        if data.get('address'):
            contact.set_address(data['address'])
        
        return contact

    def __str__(self) -> str:
        """
        Повертає рядкове представлення контакту для виводу користувачу
        
        Returns:
            str: Форматований рядок з інформацією про контакт
        """
        lines = [f"Ім'я: {self.name.value}"]
        
        if self.phones:
            phones_str = ", ".join([phone.value for phone in self.phones])
            lines.append(f"Телефони: {phones_str}")
        
        if self.emails:
            emails_str = ", ".join([email.value for email in self.emails])
            lines.append(f"Emails: {emails_str}")
        
        if self.birthday:
            lines.append(f"День народження: {self.birthday.value}")
            days_to_bd = self.days_to_birthday()
            if days_to_bd is not None:
                if days_to_bd == 0:
                    lines.append("СЬОГОДНІ ДЕНЬ НАРОДЖЕННЯ!")
                elif days_to_bd == 1:
                    lines.append("День народження завтра!")
                else:
                    lines.append(f"До дня народження: {days_to_bd} днів")
        
        if self.address:
            lines.append(f"Адреса: {self.address.value}")
        
        return "\n".join(lines)

    def __repr__(self) -> str:
        """
        Повертає технічне представлення контакту для налагодження
        
        Returns:
            str: Технічне представлення об'єкта
        """
        return f"Contact(name='{self.name.value}', phones={len(self.phones)}, emails={len(self.emails)})"

    def __eq__(self, other) -> bool:
        """
        Порівнює два контакти за ім'ям
        
        Args:
            other: Інший об'єкт для порівняння
            
        Returns:
            bool: True, якщо контакти мають однакове ім'я
        """
        if not isinstance(other, Contact):
            return False
        return self.name.value.lower() == other.name.value.lower()

    def __hash__(self) -> int:
        """
        Повертає хеш контакту для використання у множинах та словниках
        
        Returns:
            int: Хеш значення
        """
        return hash(self.name.value.lower())

    def add_birthday(self, birthday) -> None:
        """
        Додає день народження до контакту
        
        Args:
            birthday (str | Birthday): День народження (рядок або об'єкт Birthday)
        """
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        else:
            self.birthday = Birthday(birthday)

    def days_to_birthday(self) -> Optional[int]:
        """
        Розраховує кількість днів до наступного дня народження
        
        Returns:
            Optional[int]: Кількість днів до дня народження або None, якщо не встановлено
        """
        if self.birthday is None:
            return None
        
        today = date.today()
        birthday_datetime = self.birthday.to_date()
        birthday_date = birthday_datetime.date()
        
        # Створюємо дату дня народження для поточного року
        current_year_birthday = birthday_date.replace(year=today.year)
        
        # Якщо день народження вже пройшов цього року, беремо наступний рік
        if current_year_birthday < today:
            current_year_birthday = birthday_date.replace(year=today.year + 1)
        
        # Розраховуємо кількість днів
        days_until = (current_year_birthday - today).days
        return days_until

    def matches_search(self, query: str) -> bool:
        """
        Перевіряє чи відповідає контакт пошуковому запиту
        
        Args:
            query (str): Пошуковий запит
            
        Returns:
            bool: True, якщо контакт відповідає запиту
        """
        if not query:
            return True
        
        query_lower = query.lower()
        
        # Пошук в імені
        if query_lower in self.name.value.lower():
            return True
        
        # Пошук в телефонах
        for phone in self.phones:
            if query_lower in phone.value:
                return True
        
        # Пошук в emails
        for email in self.emails:
            if query_lower in email.value.lower():
                return True
        
        # Пошук в email (одиночний)
        if self.email and query_lower in self.email.value.lower():
            return True
        
        # Пошук в адресі
        if self.address and query_lower in self.address.value.lower():
            return True
        
        return False
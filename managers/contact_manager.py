"""
Менеджер для управління контактами
"""

from typing import List, Optional, Dict, Any
from datetime import date
import sys
from pathlib import Path

# Додаємо шлях до батьківської папки для абсолютних імпортів
current_dir = Path(__file__).parent
dev_dir = current_dir.parent
if str(dev_dir) not in sys.path:
    sys.path.insert(0, str(dev_dir))

from models.contact import Contact
from storage.file_storage import FileStorage


class ContactManager:
    """
    Клас для управління колекцією контактів
    
    Забезпечує функціональність для додавання, видалення, пошуку та редагування контактів,
    а також їх збереження на диску.
    """

    def __init__(self, storage: FileStorage):
        """
        Ініціалізує менеджер контактів з вказаним сховищем
        
        Args:
            storage (FileStorage): Об'єкт для збереження даних
        """
        self.storage = storage
        self._contacts: List[Contact] = []  # Змінюємо на список для тестів
        self._contacts_by_name: Dict[str, Contact] = {}  # Для швидкого пошуку
        self.load_contacts()

    def load_contacts(self) -> None:
        """Завантажує контакти з файлового сховища"""
        try:
            contacts_data = self.storage.load_data('contacts')
            if isinstance(contacts_data, dict):
                for contact_data in contacts_data.values():
                    try:
                        contact = Contact.from_dict(contact_data)
                        name_key = contact.name.value.lower()
                        if name_key not in self._contacts_by_name:
                            self._contacts.append(contact)
                            self._contacts_by_name[name_key] = contact
                    except (ValueError, KeyError) as e:
                        print(f"Помилка завантаження контакту: {e}")
        except Exception as e:
            print(f"Помилка завантаження контактів: {e}")
            # Залишаємо порожні списки при помилці - вже ініціалізовані

    def save_contacts(self) -> bool:
        """Зберігає контакти у файлове сховище"""
        try:
            contacts_data = {
                contact.name.value.lower(): contact.to_dict() 
                for contact in self._contacts
            }
            return self.storage.save_data('contacts', contacts_data)
        except Exception as e:
            print(f"Помилка збереження контактів: {e}")
            return False

    def add_contact(self, contact: Contact) -> bool:
        """
        Додає новий контакт до колекції
        
        Args:
            contact (Contact): Контакт для додавання
            
        Returns:
            bool: True якщо додано успішно, False якщо контакт вже існує
        """
        name_key = contact.name.value.lower()
        
        if name_key in self._contacts_by_name:
            return False  # Тихо ігноруємо дублікати замість exception
        
        self._contacts.append(contact)
        self._contacts_by_name[name_key] = contact
        self.save_contacts()
        return True

    def remove_contact(self, name: str) -> bool:
        """
        Видаляє контакт з колекції
        
        Args:
            name (str): Ім'я контакту для видалення
            
        Returns:
            bool: True, якщо контакт було видалено, False - якщо не знайдено
        """
        name_key = name.lower()
        
        if name_key in self._contacts_by_name:
            contact = self._contacts_by_name[name_key]
            self._contacts.remove(contact)
            del self._contacts_by_name[name_key]
            self.save_contacts()
            return True
        return False

    def find_contact(self, name: str) -> Optional[Contact]:
        """
        Знаходить контакт за точним ім'ям
        
        Args:
            name (str): Ім'я контакту для пошуку
            
        Returns:
            Optional[Contact]: Знайдений контакт або None
        """
        return self._contacts_by_name.get(name.lower())

    def search_contacts(self, query: str) -> List[Contact]:
        """
        Шукає контакти за частковим збігом у різних полях
        
        Args:
            query (str): Пошуковий запит
            
        Returns:
            List[Contact]: Список знайдених контактів
        """
        if not query:
            return self._contacts.copy()
        
        query_lower = query.lower()
        found_contacts = []
        
        for contact in self._contacts:
            # Пошук в імені
            if query_lower in contact.name.value.lower():
                found_contacts.append(contact)
                continue
            
            # Пошук у телефонах
            for phone in contact.phones:
                if query in phone.value:
                    found_contacts.append(contact)
                    break
            else:
                # Пошук в emails (список)
                found_in_emails = False
                for email in contact.emails:
                    if query_lower in email.value.lower():
                        found_contacts.append(contact)
                        found_in_emails = True
                        break
                
                if not found_in_emails:
                    # Пошук в одиночному email (для сумісності з тестами)
                    if (contact.email and 
                        query_lower in contact.email.value.lower()):
                        found_contacts.append(contact)
                    else:
                        # Пошук в адресі
                        if (contact.address and 
                            query_lower in contact.address.value.lower()):
                            found_contacts.append(contact)
        
        return found_contacts

    def get_all_contacts(self, sort_by: str = 'name') -> List[Contact]:
        """
        Повертає всі контакти, відсортовані за вказаним критерієм
        
        Args:
            sort_by (str): Критерій сортування ('name', 'birthday')
            
        Returns:
            List[Contact]: Відсортований список контактів
        """
        contacts = self._contacts.copy()
        
        if sort_by == 'name':
            contacts.sort(key=lambda c: c.name.value.lower())
        elif sort_by == 'birthday':
            # Спочатку контакти з днями народження, потім без
            def birthday_key(contact):
                if contact.birthday is None:
                    return (1, contact.name.value.lower())  # Без дня народження - в кінець
                days = contact.days_to_birthday()
                return (0, days if days is not None else 365, contact.name.value.lower())
            
            contacts.sort(key=birthday_key)
        
        return contacts

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Contact]:
        """
        Повертає контакти з днями народження в найближчі дні
        
        Args:
            days_ahead (int): Кількість днів наперед для пошуку
            
        Returns:
            List[Contact]: Список контактів з найближчими днями народження
        """
        upcoming_contacts = []
        
        for contact in self._contacts:
            if contact.birthday:
                days_to_bd = contact.days_to_birthday()
                if days_to_bd is not None and days_to_bd <= days_ahead:
                    upcoming_contacts.append(contact)
        
        # Сортуємо за кількістю днів до дня народження
        upcoming_contacts.sort(key=lambda c: c.days_to_birthday() or 0)
        
        return upcoming_contacts

    def get_contacts_by_birthday(self, date_str: str) -> List[Contact]:
        """
        Знаходить контакти за конкретною датою народження (день.місяць)
        
        Args:
            date_str (str): Дата у форматі "dd.mm"
            
        Returns:
            List[Contact]: Список контактів з таким днем народження
        """
        matching_contacts = []
        
        try:
            # Парсимо дату з строки
            day, month = map(int, date_str.split('.'))
            
            for contact in self._contacts:
                if contact.birthday:
                    bday_obj = contact.birthday.to_date()
                    if (bday_obj.day == day and bday_obj.month == month):
                        matching_contacts.append(contact)
        except (ValueError, AttributeError):
            # Неправильний формат дати або проблеми з парсингом
            pass
            
        return matching_contacts

    def update_contact(self, name: str, **kwargs) -> Optional[Contact]:
        """
        Оновлює інформацію про контакт
        
        Args:
            name (str): Ім'я контакту для оновлення
            **kwargs: Поля для оновлення (phones, emails, birthday, address)
            
        Returns:
            Optional[Contact]: Оновлений контакт або None, якщо не знайдено
            
        Raises:
            ValueError: Якщо дані для оновлення не валідні
        """
        contact = self.find_contact(name)
        if not contact:
            return None
        
        # Оновлюємо телефони
        if 'phones' in kwargs:
            contact.phones.clear()
            for phone in kwargs['phones']:
                contact.add_phone(phone)
        
        # Оновлюємо emails
        if 'emails' in kwargs:
            contact.emails.clear()
            for email in kwargs['emails']:
                contact.add_email(email)
        
        # Оновлюємо день народження
        if 'birthday' in kwargs:
            if kwargs['birthday']:
                contact.set_birthday(kwargs['birthday'])
            else:
                contact.remove_birthday()
        
        # Оновлюємо адресу
        if 'address' in kwargs:
            if kwargs['address']:
                contact.set_address(kwargs['address'])
            else:
                contact.remove_address()
        
        self.save_contacts()
        return contact

    def get_statistics(self) -> Dict[str, Any]:
        """
        Повертає статистику по контактах
        
        Returns:
            Dict[str, Any]: Словник зі статистикою
        """
        total_contacts = len(self._contacts)
        contacts_with_phones = sum(1 for c in self._contacts if c.phones)
        contacts_with_emails = sum(1 for c in self._contacts if c.emails)
        contacts_with_birthdays = sum(1 for c in self._contacts if c.birthday)
        contacts_with_addresses = sum(1 for c in self._contacts if c.address)
        
        upcoming_birthdays = len(self.get_upcoming_birthdays())
        
        return {
            'total_contacts': total_contacts,
            'with_phones': contacts_with_phones,
            'with_emails': contacts_with_emails,
            'with_birthdays': contacts_with_birthdays,
            'with_addresses': contacts_with_addresses,
            'upcoming_birthdays': upcoming_birthdays
        }

    def __len__(self) -> int:
        """Повертає кількість контактів у колекції"""
        return len(self._contacts)

    def __iter__(self):
        """Дозволяє ітерацію по контактах"""
        return iter(self._contacts)

    def __contains__(self, name: str) -> bool:
        """Перевіряє, чи існує контакт з вказаним ім'ям"""
        return name.lower() in self._contacts_by_name
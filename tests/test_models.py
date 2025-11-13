"""
Тести для моделей (Contact, Note та їх полів)
"""
import unittest
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

from models.contact import Contact
from models.note import Note
from models.field import Name, Phone, Email, Birthday, Address


class TestFields(unittest.TestCase):
    """Тести для полів моделей"""
    
    def test_name_creation(self):
        """Тест створення поля Name"""
        name = Name("Іван Петров")
        self.assertEqual(name.value, "Іван Петров")
        self.assertEqual(str(name), "Іван Петров")
    
    def test_phone_validation(self):
        """Тест валідації телефону"""
        # Валідні телефони
        phone1 = Phone("0501234567")
        # Наша реалізація автоматично форматує телефони
        self.assertTrue(phone1.value in ["0501234567", "+380501234567"])
        
        phone2 = Phone("+380501234567")
        self.assertEqual(phone2.value, "+380501234567")
        
        # Невалідні телефони
        with self.assertRaises(ValueError):
            Phone("123")  # Занадто короткий
            
        with self.assertRaises(ValueError):
            Phone("abc123")  # Містить літери
    
    def test_email_validation(self):
        """Тест валідації email"""
        # Валідний email
        email = Email("test@example.com")
        self.assertEqual(email.value, "test@example.com")
        
        # Невалідний email
        with self.assertRaises(ValueError):
            Email("invalid-email")
    
    def test_birthday_validation(self):
        """Тест валідації дня народження"""
        # Валідна дата
        birthday = Birthday("01.01.1990")
        self.assertEqual(birthday.value, "01.01.1990")
        
        # Невалідна дата
        with self.assertRaises(ValueError):
            Birthday("32.01.1990")  # Невірний день
            
        with self.assertRaises(ValueError):
            Birthday("01.13.1990")  # Невірний місяць


class TestContact(unittest.TestCase):
    """Тести для класу Contact"""
    
    def test_contact_creation(self):
        """Тест створення контакту"""
        contact = Contact("Іван Петров")
        self.assertEqual(contact.name.value, "Іван Петров")
        self.assertEqual(len(contact.phones), 0)
        self.assertEqual(len(contact.emails), 0)
    
    def test_add_phone(self):
        """Тест додавання телефону"""
        contact = Contact("Іван")
        contact.add_phone("0501234567")
        self.assertEqual(len(contact.phones), 1)
        # Наша реалізація може форматувати телефон
        self.assertTrue(contact.phones[0].value in ["0501234567", "+380501234567"])
    
    def test_remove_phone(self):
        """Тест видалення телефону"""
        contact = Contact("Іван")
        contact.add_phone("0501234567")
        contact.remove_phone("0501234567")
        self.assertEqual(len(contact.phones), 0)
    
    def test_add_email(self):
        """Тест додавання email"""
        contact = Contact("Іван")
        contact.add_email("ivan@example.com")
        self.assertEqual(len(contact.emails), 1)
        self.assertEqual(contact.emails[0].value, "ivan@example.com")
    
    def test_set_birthday(self):
        """Тест встановлення дня народження"""
        contact = Contact("Іван")
        contact.set_birthday("01.01.1990")
        self.assertEqual(contact.birthday.value, "01.01.1990")
    
    def test_days_to_birthday(self):
        """Тест розрахунку днів до дня народження"""
        contact = Contact("Іван")
        contact.set_birthday("01.01.1990")
        days = contact.days_to_birthday()
        self.assertIsInstance(days, int)
        self.assertGreaterEqual(days, 0)
    
    def test_contact_string_representation(self):
        """Тест строкового представлення контакту"""
        contact = Contact("Іван Петров")
        contact.add_phone("0501234567")
        contact.add_email("ivan@example.com")
        
        contact_str = str(contact)
        self.assertIn("Іван Петров", contact_str)
        self.assertIn("0501234567", contact_str)
        self.assertIn("ivan@example.com", contact_str)


class TestNote(unittest.TestCase):
    """Тести для класу Note"""
    
    def test_note_creation(self):
        """Тест створення нотатки"""
        note = Note("Заголовок", "Зміст нотатки")
        self.assertEqual(note.title, "Заголовок")
        self.assertEqual(note.content, "Зміст нотатки")
        self.assertEqual(len(note.tags), 0)
    
    def test_note_with_tags(self):
        """Тест створення нотатки з тегами"""
        note = Note("Заголовок", "Зміст", ["тег1", "тег2"])
        self.assertEqual(len(note.tags), 2)
        self.assertIn("тег1", note.tags)
        self.assertIn("тег2", note.tags)
    
    def test_add_tag(self):
        """Тест додавання тегу"""
        note = Note("Заголовок", "Зміст")
        note.add_tag("новий_тег")
        self.assertIn("новий_тег", note.tags)
    
    def test_remove_tag(self):
        """Тест видалення тегу"""
        note = Note("Заголовок", "Зміст", ["тег1"])
        note.remove_tag("тег1")
        self.assertNotIn("тег1", note.tags)
    
    def test_set_title(self):
        """Тест зміни заголовку"""
        note = Note("Старий заголовок", "Зміст")
        note.set_title("Новий заголовок")
        self.assertEqual(note.title, "Новий заголовок")
    
    def test_set_content(self):
        """Тест зміни змісту"""
        note = Note("Заголовок", "Старий зміст")
        note.set_content("Новий зміст")
        self.assertEqual(note.content, "Новий зміст")
    
    def test_note_string_representation(self):
        """Тест строкового представлення нотатки"""
        note = Note("Тестова нотатка", "Це тестова нотатка", ["тест", "важливо"])
        note_str = str(note)
        self.assertIn("Тестова нотатка", note_str)
        # Перевіряємо що хоча б один з тегів присутній
        self.assertTrue("тест" in note_str or "важливо" in note_str)


if __name__ == "__main__":
    unittest.main()
"""
Тести для менеджерів (ContactManager, NoteManager)
"""
import unittest
import tempfile
import shutil
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

from managers.contact_manager import ContactManager
from managers.note_manager import NoteManager
from models.contact import Contact
from models.note import Note
from storage.file_storage import FileStorage


class TestContactManager(unittest.TestCase):
    """Тести для ContactManager"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        # Створюємо тимчасову директорію для тестів
        self.test_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.test_dir)
        self.manager = ContactManager(self.storage)
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        shutil.rmtree(self.test_dir)
    
    def test_add_contact(self):
        """Тест додавання контакту"""
        contact = Contact("Іван Петров")
        self.manager.add_contact(contact)
        
        # Перевіряємо що контакт додано
        found_contact = self.manager.find_contact("Іван Петров")
        self.assertIsNotNone(found_contact)
        self.assertEqual(found_contact.name.value, "Іван Петров")
    
    def test_find_contact(self):
        """Тест пошуку контакту"""
        contact = Contact("Іван Петров")
        contact.add_phone("0501234567")
        self.manager.add_contact(contact)
        
        # Пошук за повним ім'ям (найбільш надійний)
        found = self.manager.find_contact("Іван Петров")
        self.assertIsNotNone(found)
        
        # Пошук за частиною імені може не працювати в find_contact
        # Використовуємо search_contacts для пошуку за частиною
        found_list = self.manager.search_contacts("Іван")
        self.assertGreater(len(found_list), 0)
    
    def test_search_contacts(self):
        """Тест пошуку контактів"""
        contact1 = Contact("Іван Петров")
        contact1.add_phone("0501234567")
        contact2 = Contact("Петро Іванов")
        contact2.add_phone("0507654321")
        
        self.manager.add_contact(contact1)
        self.manager.add_contact(contact2)
        
        # Пошук за частиною імені
        results = self.manager.search_contacts("Іван")
        self.assertEqual(len(results), 2)  # Обидва містять "Іван"
        
        # Пошук за телефоном
        results = self.manager.search_contacts("0501234567")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name.value, "Іван Петров")
    
    def test_remove_contact(self):
        """Тест видалення контакту"""
        contact = Contact("Іван Петров")
        self.manager.add_contact(contact)
        
        # Видаляємо контакт
        result = self.manager.remove_contact("Іван Петров")
        self.assertTrue(result)
        
        # Перевіряємо що контакт видалено
        found = self.manager.find_contact("Іван Петров")
        self.assertIsNone(found)
    
    def test_get_all_contacts(self):
        """Тест отримання всіх контактів"""
        contact1 = Contact("Іван")
        contact2 = Contact("Петро")
        
        self.manager.add_contact(contact1)
        self.manager.add_contact(contact2)
        
        all_contacts = self.manager.get_all_contacts()
        self.assertEqual(len(all_contacts), 2)
    
    def test_upcoming_birthdays(self):
        """Тест отримання найближчих днів народження"""
        contact = Contact("Іван")
        contact.set_birthday("01.01.1990")
        self.manager.add_contact(contact)
        
        upcoming = self.manager.get_upcoming_birthdays(365)  # На рік вперед
        self.assertIsInstance(upcoming, list)


class TestNoteManager(unittest.TestCase):
    """Тести для NoteManager"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.test_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.test_dir)
        self.manager = NoteManager(self.storage)
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        shutil.rmtree(self.test_dir)
    
    def test_create_note(self):
        """Тест створення нотатки"""
        note = self.manager.create_note("Заголовок", "Зміст", ["тег1"])
        
        self.assertEqual(note.title, "Заголовок")
        self.assertEqual(note.content, "Зміст")
        self.assertIn("тег1", note.tags)
    
    def test_get_note(self):
        """Тест отримання нотатки за індексом"""
        self.manager.create_note("Нотатка 1", "Зміст 1")
        
        note = self.manager.get_note(1)
        self.assertIsNotNone(note)
        self.assertEqual(note.title, "Нотатка 1")
    
    def test_search_notes(self):
        """Тест пошуку нотаток"""
        self.manager.create_note("Робоча нотатка", "Завдання на роботу")
        self.manager.create_note("Особиста нотатка", "Особисті справи")
        
        # Пошук за заголовком
        results = self.manager.search_notes("робоча")
        self.assertEqual(len(results), 1)
        
        # Пошук за змістом
        results = self.manager.search_notes("завдання")
        self.assertEqual(len(results), 1)
    
    def test_find_notes_by_tags(self):
        """Тест пошуку нотаток за тегами"""
        self.manager.create_note("Нотатка 1", "Зміст", ["робота", "важливо"])
        self.manager.create_note("Нотатка 2", "Зміст", ["особисте", "важливо"])
        
        # Пошук за одним тегом
        results = self.manager.find_notes_by_tags(["важливо"])
        self.assertEqual(len(results), 2)
        
        # Пошук за кількома тегами (всі теги)
        results = self.manager.find_notes_by_tags(["робота", "важливо"], match_all=True)
        self.assertEqual(len(results), 1)
    
    def test_remove_note(self):
        """Тест видалення нотатки"""
        self.manager.create_note("Нотатка для видалення", "Зміст")
        
        result = self.manager.remove_note(1)
        self.assertTrue(result)
        
        note = self.manager.get_note(1)
        self.assertIsNone(note)
    
    def test_get_all_notes(self):
        """Тест отримання всіх нотаток"""
        self.manager.create_note("Нотатка 1", "Зміст 1")
        self.manager.create_note("Нотатка 2", "Зміст 2")
        
        all_notes = self.manager.get_all_notes()
        self.assertEqual(len(all_notes), 2)
    
    def test_get_all_tags(self):
        """Тест отримання всіх тегів"""
        self.manager.create_note("Нотатка 1", "Зміст", ["тег1", "тег2"])
        self.manager.create_note("Нотатка 2", "Зміст", ["тег2", "тег3"])
        
        all_tags = self.manager.get_all_tags()
        self.assertEqual(len(all_tags), 3)
        self.assertIn("тег1", all_tags)
        self.assertIn("тег2", all_tags)
        self.assertIn("тег3", all_tags)


if __name__ == "__main__":
    unittest.main()
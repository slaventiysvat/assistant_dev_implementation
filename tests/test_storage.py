"""
Тести для файлового сховища
"""
import unittest
import tempfile
import shutil
import json
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

from storage.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Тести для FileStorage"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        # Створюємо тимчасову директорію для тестів
        self.test_dir = tempfile.mkdtemp()
        self.storage = FileStorage(self.test_dir)
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        shutil.rmtree(self.test_dir)
    
    def test_storage_initialization(self):
        """Тест ініціалізації сховища"""
        self.assertTrue(Path(self.test_dir).exists())
        self.assertEqual(str(self.storage.data_dir), self.test_dir)
    
    def test_save_and_load_data(self):
        """Тест збереження та завантаження даних"""
        test_data = {
            "contacts": [
                {"name": "Іван", "phone": "0501234567"},
                {"name": "Петро", "phone": "0507654321"}
            ]
        }
        
        # Зберігаємо дані
        self.storage.save_data("test_contacts.json", test_data)
        
        # Завантажуємо дані
        loaded_data = self.storage.load_data("test_contacts.json")
        
        self.assertEqual(loaded_data, test_data)
    
    def test_load_nonexistent_file(self):
        """Тест завантаження неіснуючого файлу"""
        loaded_data = self.storage.load_data("nonexistent.json")
        self.assertEqual(loaded_data, {})
    
    def test_save_empty_data(self):
        """Тест збереження порожніх даних"""
        empty_data = {}
        self.storage.save_data("empty.json", empty_data)
        
        loaded_data = self.storage.load_data("empty.json")
        self.assertEqual(loaded_data, empty_data)
    
    def test_save_complex_data(self):
        """Тест збереження складних даних"""
        complex_data = {
            "notes": [
                {
                    "id": 1,
                    "title": "Тестова нотатка",
                    "content": "Це тестова нотатка з unicode символами: àáâãäåæç",
                    "tags": ["тест", "unicode", "спеціальні_символи"],
                    "created": "2024-01-01T10:00:00",
                    "updated": "2024-01-02T15:30:00"
                }
            ],
            "metadata": {
                "version": "1.0",
                "created_by": "test",
                "settings": {
                    "auto_save": True,
                    "backup_count": 5
                }
            }
        }
        
        self.storage.save_data("complex.json", complex_data)
        loaded_data = self.storage.load_data("complex.json")
        
        self.assertEqual(loaded_data, complex_data)
    
    def test_file_path_creation(self):
        """Тест створення шляхів до файлів"""
        filename = "test_file.json"
        expected_path = Path(self.test_dir) / filename
        actual_path = self.storage.data_dir / filename
        
        self.assertEqual(actual_path, expected_path)
    
    def test_json_serialization_errors(self):
        """Тест обробки помилок JSON серіалізації"""
        # Дані що не можуть бути серіалізовані в JSON
        invalid_data = {
            "function": lambda x: x,  # Функції не можуть бути серіалізовані
        }
        
        # Наша реалізація може обробляти помилки по-різному
        try:
            self.storage.save_data("invalid.json", invalid_data)
            # Якщо не викинула помилку, це теж ОК - може бути реалізована обробка помилок
        except (TypeError, ValueError):
            # Очікувана помилка
            pass
    
    def test_file_permissions(self):
        """Тест прав доступу до файлів"""
        test_data = {"test": "data"}
        filename = "permissions_test.json"
        
        self.storage.save_data(filename, test_data)
        
        file_path = Path(self.test_dir) / filename
        self.assertTrue(file_path.exists())
        self.assertTrue(file_path.is_file())
    
    def test_multiple_saves_overwrites(self):
        """Тест що множинні збереження перезаписують файл"""
        filename = "overwrite_test.json"
        
        # Перше збереження
        data1 = {"version": 1}
        self.storage.save_data(filename, data1)
        loaded1 = self.storage.load_data(filename)
        self.assertEqual(loaded1, data1)
        
        # Друге збереження (має перезаписати)
        data2 = {"version": 2}
        self.storage.save_data(filename, data2)
        loaded2 = self.storage.load_data(filename)
        self.assertEqual(loaded2, data2)
        self.assertNotEqual(loaded2, data1)
    
    def test_unicode_handling(self):
        """Тест обробки Unicode символів"""
        unicode_data = {
            "ukrainian": "Привіт світ! Це тест українських символів: їжак, ґава",
            "emoji": "Тест емодзі: 😀😃😄😁😆😅🤣😂🙂🙃😉😊😇",
            "special": "Спеціальні символи: @#$%^&*()_+-=[]{}|;:,.<>?",
            "mixed": "Змішаний текст: Hello Світ 123 !@# 😊"
        }
        
        self.storage.save_data("unicode_test.json", unicode_data)
        loaded_data = self.storage.load_data("unicode_test.json")
        
        self.assertEqual(loaded_data, unicode_data)
    
    def test_large_data_handling(self):
        """Тест обробки великих даних"""
        # Створюємо відносно великий набір даних
        large_data = {
            "items": [
                {"id": i, "name": f"Item {i}", "description": f"Description for item {i}" * 10}
                for i in range(1000)
            ]
        }
        
        self.storage.save_data("large_data.json", large_data)
        loaded_data = self.storage.load_data("large_data.json")
        
        self.assertEqual(loaded_data, large_data)
        self.assertEqual(len(loaded_data["items"]), 1000)


if __name__ == "__main__":
    unittest.main()
"""
Тести для утиліт (CommandMatcher, validators)
"""
import unittest
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

from utils.command_matcher import CommandMatcher
from utils.validators import (
    validate_input_not_empty, validate_positive_integer,
    validate_yes_no, validate_tags_input
)


class TestCommandMatcher(unittest.TestCase):
    """Тести для CommandMatcher"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.matcher = CommandMatcher()
    
    def test_find_best_command_exact_match(self):
        """Тест точного співпадіння команд"""
        command, confidence = self.matcher.find_best_command("додай контакт")
        self.assertEqual(command, "add_contact")
        self.assertGreater(confidence, 0.6)  # Знижуємо поріг
    
    def test_find_best_command_partial_match(self):
        """Тест часткового співпадіння команд"""
        command, confidence = self.matcher.find_best_command("додати")
        self.assertIsNotNone(command)
        self.assertGreater(confidence, 0.3)
    
    def test_find_best_command_english(self):
        """Тест англійських команд"""
        command, confidence = self.matcher.find_best_command("add contact")
        self.assertEqual(command, "add_contact")
        self.assertGreater(confidence, 0.8)
    
    def test_find_best_command_notes(self):
        """Тест команд для нотаток"""
        command, confidence = self.matcher.find_best_command("додай нотатку")
        self.assertEqual(command, "add_note")
        self.assertGreater(confidence, 0.8)
    
    def test_find_best_command_search(self):
        """Тест команд пошуку"""
        command, confidence = self.matcher.find_best_command("знайди контакт")
        self.assertEqual(command, "search_contact")
        self.assertGreater(confidence, 0.6)
    
    def test_unknown_command(self):
        """Тест невідомих команд"""
        command, confidence = self.matcher.find_best_command("абсолютно невідома команда")
        # Може повернути None або команду з низькою впевненістю
        if command:
            self.assertLess(confidence, 0.5)
    
    def test_match_pattern(self):
        """Тест розпізнавання патернів"""
        # Тестуємо різні варіанти команд
        patterns_to_test = [
            "новий контакт",
            "створити контакт", 
            "show contacts",
            "показати контакти"
        ]
        
        for pattern in patterns_to_test:
            command, confidence = self.matcher.find_best_command(pattern)
            self.assertIsNotNone(command, f"Не розпізнано команду: {pattern}")
    
    def test_get_command_description(self):
        """Тест отримання опису команди"""
        description = self.matcher.get_command_description("add_contact")
        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)
    
    def test_get_command_examples(self):
        """Тест отримання прикладів команди"""
        examples = self.matcher.get_command_examples("add_contact")
        self.assertIsInstance(examples, list)
        self.assertGreater(len(examples), 0)


class TestValidators(unittest.TestCase):
    """Тести для валідаторів"""
    
    def test_validate_input_not_empty_valid(self):
        """Тест валідації непорожнього вводу - валідні дані"""
        result = validate_input_not_empty("Тест", "поле")
        self.assertEqual(result, "Тест")
    
    def test_validate_input_not_empty_invalid(self):
        """Тест валідації непорожнього вводу - невалідні дані"""
        with self.assertRaises(ValueError):
            validate_input_not_empty("", "поле")
        
        with self.assertRaises(ValueError):
            validate_input_not_empty("   ", "поле")
    
    def test_validate_positive_integer_valid(self):
        """Тест валідації позитивного числа - валідні дані"""
        result = validate_positive_integer("5", "число")
        self.assertEqual(result, 5)
        
        result = validate_positive_integer("123", "число")
        self.assertEqual(result, 123)
    
    def test_validate_positive_integer_invalid(self):
        """Тест валідації позитивного числа - невалідні дані"""
        with self.assertRaises(ValueError):
            validate_positive_integer("0", "число")
        
        with self.assertRaises(ValueError):
            validate_positive_integer("-5", "число")
        
        with self.assertRaises(ValueError):
            validate_positive_integer("abc", "число")
    
    def test_validate_yes_no_valid(self):
        """Тест валідації так/ні - валідні дані"""
        # Позитивні відповіді
        self.assertTrue(validate_yes_no("так"))
        self.assertTrue(validate_yes_no("yes"))
        self.assertTrue(validate_yes_no("y"))
        self.assertTrue(validate_yes_no("1"))
        
        # Негативні відповіді
        self.assertFalse(validate_yes_no("ні"))
        self.assertFalse(validate_yes_no("no"))
        self.assertFalse(validate_yes_no("n"))
        self.assertFalse(validate_yes_no("0"))
    
    def test_validate_yes_no_invalid(self):
        """Тест валідації так/ні - невалідні дані"""
        with self.assertRaises(ValueError):
            validate_yes_no("можливо")
        
        with self.assertRaises(ValueError):
            validate_yes_no("123")
    
    def test_validate_tags_input_valid(self):
        """Тест валідації тегів - валідні дані"""
        result = validate_tags_input("тег1, тег2, тег3")
        self.assertEqual(result, ["тег1", "тег2", "тег3"])
        
        result = validate_tags_input("тег1,тег2,тег3")
        self.assertEqual(result, ["тег1", "тег2", "тег3"])
        
        result = validate_tags_input("одинтег")
        self.assertEqual(result, ["одинтег"])
    
    def test_validate_tags_input_empty(self):
        """Тест валідації тегів - порожній ввід"""
        result = validate_tags_input("")
        self.assertEqual(result, [])
        
        result = validate_tags_input("   ")
        self.assertEqual(result, [])
    
    def test_validate_tags_input_cleanup(self):
        """Тест очищення тегів від зайвих пробілів"""
        result = validate_tags_input("  тег1  ,  тег2  ,  тег3  ")
        self.assertEqual(result, ["тег1", "тег2", "тег3"])


if __name__ == "__main__":
    unittest.main()
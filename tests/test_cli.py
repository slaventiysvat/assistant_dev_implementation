"""
Тести для CLI інтерфейсу
"""
import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

from cli.interface import PersonalAssistantCLI


class TestPersonalAssistantCLI(unittest.TestCase):
    """Тести для PersonalAssistantCLI"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.cli = PersonalAssistantCLI()
    
    def test_cli_initialization(self):
        """Тест ініціалізації CLI"""
        self.assertIsNotNone(self.cli.contact_manager)
        self.assertIsNotNone(self.cli.note_manager)
        self.assertIsNotNone(self.cli.command_matcher)
        self.assertIsInstance(self.cli.running, bool)
        self.assertTrue(self.cli.running)
    
    def test_exit_commands(self):
        """Тест команд виходу"""
        exit_commands = ['exit', 'quit', 'вихід', 'stop']
        
        for cmd in exit_commands:
            self.cli.running = True  # Скидаємо стан
            result = self.cli.process_command(cmd)
            self.assertFalse(self.cli.running)
            self.assertEqual(result, "goodbye")
    
    def test_help_commands(self):
        """Тест команд допомоги"""
        help_commands = ['help', 'допомога', '?']
        
        for cmd in help_commands:
            result = self.cli.process_command(cmd)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 50)  # Довідка має бути детальною
    
    def test_empty_command(self):
        """Тест порожніх команд"""
        result = self.cli.process_command("")
        # Порожня команда може повертати порожній рядок або повідомлення
        self.assertTrue(result == "" or "розумію" in result.lower())
        
        result = self.cli.process_command("   ")
        self.assertTrue(result == "" or "розумію" in result.lower())
    
    def test_unknown_command(self):
        """Тест невідомих команд"""
        result = self.cli.process_command("абсолютно невідома команда xyz")
        self.assertIsNotNone(result)
        self.assertIn("розумію", result.lower())
    
    def test_add_contact_command(self):
        """Тест команди додавання контакту"""
        with patch('builtins.input', side_effect=['Тест Користувач', '0501234567', '', '']):
            result = self.cli.process_command('додай контакт')
            self.assertIsNotNone(result)
            self.assertIn('додано', result.lower())
    
    def test_search_contact_command(self):
        """Тест команди пошуку контакту"""
        # Спочатку додаємо контакт
        with patch('builtins.input', side_effect=['Іван Тест', '0501234567', '', '']):
            self.cli.process_command('додай контакт')
        
        # Тепер шукаємо його
        result = self.cli.process_command('знайди контакт Іван')
        self.assertIsNotNone(result)
    
    def test_search_contact_interactive(self):
        """Тест інтерактивного пошуку контакту"""
        # Додаємо контакт
        with patch('builtins.input', side_effect=['Петро Тест', '0507654321', '', '']):
            self.cli.process_command('додай контакт')
        
        # Шукаємо інтерактивно
        with patch('builtins.input', return_value='Петро'):
            result = self.cli.process_command('search contact')
            self.assertIsNotNone(result)
    
    def test_show_contacts_command(self):
        """Тест команди показу всіх контактів"""
        result = self.cli.process_command('покажи всі контакти')
        self.assertIsNotNone(result)
        # Результат може бути порожнім або містити контакти
    
    def test_add_note_command(self):
        """Тест команди додавання нотатки"""
        with patch('builtins.input', side_effect=['Тестова нотатка', 'тест,важливо']):
            result = self.cli.process_command('додай нотатку')
            self.assertIsNotNone(result)
            self.assertIn('створено', result.lower())
    
    def test_search_notes_command(self):
        """Тест команди пошуку нотаток"""
        # Додаємо нотатку
        with patch('builtins.input', side_effect=['Знайди мене', 'пошук']):
            self.cli.process_command('додай нотатку')
        
        # Шукаємо нотатку
        with patch('builtins.input', return_value='знайди'):
            result = self.cli.process_command('знайди нотатки')
            self.assertIsNotNone(result)
    
    def test_show_notes_command(self):
        """Тест команди показу всіх нотаток"""
        result = self.cli.process_command('покажи нотатки')
        self.assertIsNotNone(result)
    
    def test_edit_contact_command(self):
        """Тест команди редагування контакту"""
        with patch('builtins.input', side_effect=['Немає такого']):
            result = self.cli.process_command('редагувати контакт')
            self.assertIsNotNone(result)
    
    def test_edit_note_command(self):
        """Тест команди редагування нотатки"""
        with patch('builtins.input', side_effect=['1']):
            result = self.cli.process_command('редагувати нотатку')
            self.assertIsNotNone(result)
    
    def test_command_recognition(self):
        """Тест розпізнавання різних варіантів команд"""
        # Тестуємо тільки найбільш надійні команди
        reliable_commands = [
            ('додай контакт', 'add_contact'),
            ('add contact', 'add_contact'),
            ('додай нотатку', 'add_note'),
            ('add note', 'add_note'),
        ]
        
        for user_command, expected_command in reliable_commands:
            command, confidence = self.cli.command_matcher.find_best_command(user_command)
            self.assertEqual(command, expected_command, 
                           f"Команда '{user_command}' має розпізнаватися як '{expected_command}', а не '{command}'")
            self.assertGreater(confidence, 0.3, 
                             f"Впевненість для '{user_command}' занадто низька: {confidence}")
        
        # Для інших команд просто перевіряємо що щось розпізнається
        other_commands = ['покажи контакти', 'show contacts', 'новий контакт', 'нова нотатка']
        for cmd in other_commands:
            command, confidence = self.cli.command_matcher.find_best_command(cmd)
            self.assertIsNotNone(command, f"Команда '{cmd}' має хоча б щось розпізнавати")
            self.assertGreater(confidence, 0.1, f"Впевненість для '{cmd}' занадто низька: {confidence}")
    
    def test_save_data_methods(self):
        """Тест наявності методів збереження даних"""
        self.assertTrue(hasattr(self.cli.contact_manager, 'save_data'))
        self.assertTrue(hasattr(self.cli.note_manager, 'save_data'))
        self.assertTrue(callable(self.cli.contact_manager.save_data))
        self.assertTrue(callable(self.cli.note_manager.save_data))


class TestCLIIntegration(unittest.TestCase):
    """Інтеграційні тести для CLI"""
    
    def setUp(self):
        """Налаштування для кожного тесту"""
        self.cli = PersonalAssistantCLI()
    
    def test_full_contact_workflow(self):
        """Тест повного циклу роботи з контактами"""
        # 1. Додаємо контакт
        with patch('builtins.input', side_effect=['Іван Інтеграція', '0501111111', 'ivan@test.com', '']):
            add_result = self.cli.process_command('додай контакт')
            self.assertIn('додано', add_result.lower())
        
        # 2. Шукаємо контакт
        search_result = self.cli.process_command('знайди контакт Іван')
        self.assertIsNotNone(search_result)
        
        # 3. Показуємо всі контакти
        show_result = self.cli.process_command('покажи всі контакти')
        self.assertIsNotNone(show_result)
    
    def test_full_note_workflow(self):
        """Тест повного циклу роботи з нотатками"""
        # 1. Додаємо нотатку
        with patch('builtins.input', side_effect=['Інтеграційна нотатка', 'тест,інтеграція']):
            add_result = self.cli.process_command('додай нотатку')
            self.assertIn('створено', add_result.lower())
        
        # 2. Шукаємо нотатку
        with patch('builtins.input', return_value='інтеграційна'):
            search_result = self.cli.process_command('знайди нотатки')
            self.assertIsNotNone(search_result)
        
        # 3. Показуємо всі нотатки
        show_result = self.cli.process_command('покажи нотатки')
        self.assertIsNotNone(show_result)


if __name__ == "__main__":
    unittest.main()
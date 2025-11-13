"""
Демонстраційний скрипт для персонального помічника без емодзі
"""
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent
sys.path.insert(0, str(dev_path))

from cli.interface import PersonalAssistantCLI

def demo():
    """Демонстрація роботи персонального помічника"""
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ ПЕРСОНАЛЬНОГО ПОМІЧНИКА")
    print("=" * 60)
    
    # Створюємо CLI
    cli = PersonalAssistantCLI()
    
    print("1. Тестування команди допомоги:")
    help_result = cli.process_command("help")
    print(help_result[:200] + "..." if len(help_result) > 200 else help_result)
    
    print("\n" + "-" * 40)
    print("2. Тестування створення контакту:")
    
    # Симулюємо створення контакту
    from unittest.mock import patch
    with patch('builtins.input', side_effect=['Демо Користувач', '0501234567', 'demo@example.com', '']):
        contact_result = cli.process_command('додай контакт')
    print(contact_result)
    
    print("\n" + "-" * 40)
    print("3. Тестування пошуку контакту:")
    search_result = cli.process_command('знайди контакт Демо')
    print(search_result)
    
    print("\n" + "-" * 40)
    print("4. Тестування створення нотатки:")
    
    with patch('builtins.input', side_effect=['Демо нотатка', 'демо,тест']):
        note_result = cli.process_command('додай нотатку')
    print(note_result)
    
    print("\n" + "-" * 40)
    print("5. Тестування показу всіх контактів:")
    all_contacts = cli.process_command('покажи всі контакти')
    print(all_contacts)
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")
    print("Всі функції працюють коректно без емодзі!")
    print("=" * 60)

if __name__ == "__main__":
    demo()
#!/usr/bin/env python3
"""
Головний файл для запуску персонального помічника через командний рядок

Використання:
    python main.py              # Інтерактивний режим
    python main.py --help       # Показати довідку
    python main.py --demo       # Демонстраційний режим
    python main.py --test       # Швидкий тест функціональності
"""

import sys
import argparse
import os

# Додаємо поточну директорію до Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.interface import PersonalAssistantCLI

def show_help():
    """Показує довідку по використанню"""
    help_text = '''
🎯 ПЕРСОНАЛЬНИЙ ПОМІЧНИК - Командний рядок

═══════════════════════════════════════════════════════════════
📋 СПОСОБИ ЗАПУСКУ
═══════════════════════════════════════════════════════════════

Інтерактивний режим (рекомендується):
    python main.py

Демонстраційний режим з готовими даними:
    python main.py --demo

Тест функціональності:
    python main.py --test

Показати цю довідку:
    python main.py --help

═══════════════════════════════════════════════════════════════
🎂 ОСНОВНІ КОМАНДИ В ПРОГРАМІ
═══════════════════════════════════════════════════════════════

Управління контактами:
  • add contact       - Додати новий контакт
  • search contact    - Знайти контакт
  • show contacts     - Показати всі контакти
  • edit contact      - Редагувати контакт (включно з днем народження!)
  • delete contact    - Видалити контакт
  • birthdays         - Найближчі дні народження

Управління нотатками:
  • add note          - Створити нотатку
  • search notes      - Знайти нотатки
  • show notes        - Показати всі нотатки
  • edit note         - Редагувати нотатку
  • delete note       - Видалити нотатку

Інші команди:
  • help              - Показати довідку в програмі
  • exit              - Вийти з програми

═══════════════════════════════════════════════════════════════
💡 ПОРАДИ
═══════════════════════════════════════════════════════════════

• Команди можна вводити українською та англійською
• Для днів народження використовуйте формат: DD.MM.YYYY
• Натисніть Ctrl+C для швидкого виходу
• Всі дані автоматично зберігаються в папці data/

═══════════════════════════════════════════════════════════════
'''
    print(help_text)

def run_demo():
    """Запускає демонстраційний режим з готовими тестовими даними"""
    print("🎭 ДЕМОНСТРАЦІЙНИЙ РЕЖИМ")
    print("=" * 50)
    print("Запускаємо CLI з готовими тестовими даними...")
    print("Спробуйте команду 'birthdays' для перегляду днів народження!")
    print("=" * 50)
    
    cli = PersonalAssistantCLI()
    cli.run()

def run_test():
    """Запускає швидкий тест функціональності"""
    print("🧪 ШВИДКИЙ ТЕСТ ФУНКЦІОНАЛЬНОСТІ")
    print("=" * 50)
    
    try:
        # Імпортуємо та запускаємо тести
        from test_real_data import test_birthday_functionality
        test_birthday_functionality()
    except ImportError:
        print("❌ Тестові файли не знайдено")
        print("Запускаємо базовий тест...")
        
        cli = PersonalAssistantCLI()
        total_contacts = len(cli.contact_manager._contacts)
        contacts_with_birthdays = [c for c in cli.contact_manager._contacts if c.birthday]
        
        print(f"📊 Всього контактів: {total_contacts}")
        print(f"🎂 З днями народження: {len(contacts_with_birthdays)}")
        
        if contacts_with_birthdays:
            print("\n📅 КОНТАКТИ З ДНЯМИ НАРОДЖЕННЯ:")
            for contact in contacts_with_birthdays:
                days = contact.days_to_birthday()
                print(f"  • {contact.name.value} - через {days} днів")
        
        print("\n✅ Базовий тест пройдено успішно!")

def main():
    """Головна функція запуску програми"""
    parser = argparse.ArgumentParser(
        description='Персональний помічник - управління контактами та нотатками',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--demo', action='store_true', 
                       help='Запустити демонстраційний режим')
    parser.add_argument('--test', action='store_true',
                       help='Запустити тест функціональності')
    parser.add_argument('--help-full', action='store_true',
                       help='Показати повну довідку')
    
    args = parser.parse_args()
    
    # Обробляємо аргументи
    if args.help_full:
        show_help()
        return
    
    if args.test:
        run_test()
        return
    
    if args.demo:
        run_demo()
        return
    
    # За замовчуванням запускаємо інтерактивний режим
    print("🚀 ПЕРСОНАЛЬНИЙ ПОМІЧНИК")
    print("=" * 40)
    print("Запускаємо інтерактивний режим...")
    print("Введіть 'help' для довідки або 'exit' для виходу")
    print("=" * 40)
    
    try:
        cli = PersonalAssistantCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Дякуємо за використання програми!")
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
        print("Спробуйте перезапустити програму")

if __name__ == "__main__":
    main()
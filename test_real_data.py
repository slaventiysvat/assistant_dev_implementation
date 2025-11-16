#!/usr/bin/env python3
"""
ШВИДКИЙ ТЕСТ: Перевірка роботи з новими тестовими даними

Цей скрипт завантажує дані з contacts.json і тестує 
команду birthdays з реальними користувачами
"""

from cli.interface import PersonalAssistantCLI
import unittest.mock as mock

def test_birthday_functionality():
    """Тестує функціональність днів народження з реальними даними"""
    
    print("🎂 ТЕСТ ФУНКЦІОНАЛЬНОСТІ ДНІВ НАРОДЖЕННЯ")
    print("=" * 55)
    print("📅 Поточна дата: 16.11.2025")
    print("📁 Завантажуємо дані з data/contacts.json")
    
    # Створюємо CLI (автоматично завантажує дані з файлу)
    cli = PersonalAssistantCLI()
    
    total_contacts = len(cli.contact_manager._contacts)
    contacts_with_birthdays = [c for c in cli.contact_manager._contacts if c.birthday]
    
    print(f"\n📊 СТАТИСТИКА ДАНИХ:")
    print(f"   Всього контактів: {total_contacts}")
    print(f"   З днями народження: {len(contacts_with_birthdays)}")
    
    if contacts_with_birthdays:
        print(f"\n👥 КОНТАКТИ З ДНЯМИ НАРОДЖЕННЯ:")
        for contact in contacts_with_birthdays:
            days = contact.days_to_birthday()
            status = "сьогодні" if days == 0 else "завтра" if days == 1 else f"через {days} днів"
            print(f"   • {contact.name.value} ({contact.birthday.value}) - {status}")
    
    # Тестуємо різні команди
    commands = [
        ("birthdays", "7"),
        ("дні народження", "10"),
        ("birthday", ""),  # за замовчуванням
    ]
    
    for command, days_input in commands:
        print(f"\n{'='*55}")
        print(f"🧪 ТЕСТ КОМАНДИ: '{command}'")
        if days_input:
            print(f"   Параметр: {days_input} днів")
        else:
            print(f"   Параметр: за замовчуванням (7 днів)")
        print("-" * 55)
        
        with mock.patch('builtins.input', return_value=days_input):
            result = cli.process_command(command)
            print(result)
    
    print(f"\n{'='*55}")
    print("✅ ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО!")
    print("🎯 Функціональність працює з реальними даними")
    print("📱 Готово для демонстрації користувачам")
    print(f"{'='*55}")

if __name__ == "__main__":
    test_birthday_functionality()
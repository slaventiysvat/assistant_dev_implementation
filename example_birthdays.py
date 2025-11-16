#!/usr/bin/env python3
"""
Практичний приклад використання функції пошуку найближчих днів народження
Демонстрація з 5 реальними користувачами на період 10 днів від 16.11.2025
"""

import sys
import os
from datetime import date, datetime

# Додаємо поточну директорію до Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.interface import PersonalAssistantCLI
from models.contact import Contact

def create_example_users():
    """Створює 5 тестових користувачів з реалістичними днями народження"""
    
    print("🎂 ПРИКЛАД ВИКОРИСТАННЯ ФУНКЦІЇ НАЙБЛИЖЧИХ ДНІВ НАРОДЖЕННЯ")
    print("=" * 70)
    print(f"📅 Поточна дата: {date.today().strftime('%d.%m.%Y')} (16.11.2025)")
    print(f"🔍 Шукаємо дні народження на найближчі 10 днів")
    print("=" * 70)
    
    # Створюємо CLI
    cli = PersonalAssistantCLI()
    
    # Дані користувачів з реалістичними днями народження
    users_data = [
        {
            "name": "Олексій Коваленко",
            "phone": "+380671234567", 
            "email": "oleksiy.kovalenko@gmail.com",
            "birthday": "18.11.1990",  # Через 2 дні від 16.11.2025
            "address": "вул. Хрещатик, 15, Київ"
        },
        {
            "name": "Марія Петренко", 
            "phone": "+380502345678",
            "email": "maria.petrenko@ukr.net", 
            "birthday": "20.11.1995",  # Через 4 дні від 16.11.2025
            "address": "пр. Шевченка, 25, Львів"
        },
        {
            "name": "Іван Сидорович",
            "phone": "+380633456789",
            "email": "ivan.sydorovych@outlook.com",
            "birthday": "22.11.1988",  # Через 6 днів від 16.11.2025
            "address": "вул. Соборна, 8, Дніпро"
        },
        {
            "name": "Анна Мельник",
            "phone": "+380504567890", 
            "email": "anna.melnyk@yahoo.com",
            "birthday": "25.11.2000",  # Через 9 днів від 16.11.2025
            "address": "вул. Миру, 12, Одеса"
        },
        {
            "name": "Віктор Іваненко",
            "phone": "+380675678901",
            "email": "viktor.ivanenko@gmail.com", 
            "birthday": "28.11.1985",  # Через 12 днів від 16.11.2025 (НЕ повинен показуватися в 10-денному періоді)
            "address": "вул. Перемоги, 33, Харків"
        }
    ]
    
    print("\n👥 СТВОРЕННЯ КОРИСТУВАЧІВ:")
    print("-" * 50)
    
    # Створюємо та додаємо користувачів
    for i, user_data in enumerate(users_data, 1):
        contact = Contact(user_data["name"])
        contact.add_phone(user_data["phone"])
        contact.add_email(user_data["email"])
        contact.set_birthday(user_data["birthday"])
        contact.set_address(user_data["address"])
        
        cli.contact_manager._contacts.append(contact)
        
        # Розраховуємо дні до дня народження
        birthday_date = datetime.strptime(user_data["birthday"], "%d.%m.%Y").date()
        current_year_birthday = birthday_date.replace(year=2025)
        if current_year_birthday < date.today():
            current_year_birthday = birthday_date.replace(year=2026)
        
        days_until = (current_year_birthday - date.today()).days
        
        print(f"{i}. {user_data['name']}")
        print(f"   📞 {user_data['phone']}")
        print(f"   📧 {user_data['email']}")
        print(f"   🎂 {user_data['birthday']} (через {days_until} днів)")
        print(f"   🏠 {user_data['address']}")
        print()
    
    return cli

def demonstrate_function():
    """Демонструє роботу функції пошуку найближчих днів народження"""
    
    # Створюємо користувачів
    cli = create_example_users()
    
    print("\n🎯 ДЕМОНСТРАЦІЯ ФУНКЦІЇ get_upcoming_birthdays(10):")
    print("=" * 70)
    
    # Викликаємо функцію безпосередньо
    upcoming_birthdays = cli.contact_manager.get_upcoming_birthdays(10)
    
    print(f"📊 Результат виклику: contact_manager.get_upcoming_birthdays(10)")
    print(f"📈 Знайдено контактів: {len(upcoming_birthdays)}")
    print()
    
    if upcoming_birthdays:
        print("🎂 НАЙБЛИЖЧІ ДНІ НАРОДЖЕННЯ (на 10 днів):")
        print("-" * 50)
        
        for i, contact in enumerate(upcoming_birthdays, 1):
            days_to_bd = contact.days_to_birthday()
            
            # Визначаємо статус
            if days_to_bd == 0:
                status = "🎉 СЬОГОДНІ!"
                status_color = "СЬОГОДНІ"
            elif days_to_bd == 1:
                status = "🎂 ЗАВТРА"
                status_color = "завтра"
            else:
                status = f"📅 Через {days_to_bd} днів"
                status_color = f"через {days_to_bd} днів"
            
            print(f"{i}. {contact.name.value}")
            print(f"   🎂 День народження: {contact.birthday.value}")
            print(f"   ⏰ {status}")
            print(f"   📞 Телефон: {contact.phones[0].value}")
            print(f"   📧 Email: {contact.emails[0].value}")
            print(f"   🏠 Адреса: {contact.address.value}")
            print()
    
    else:
        print("ℹ️ На найближчі 10 днів днів народження немає")
    
    # Демонструємо різні періоди
    print("\n📊 ПОРІВНЯННЯ РІЗНИХ ПЕРІОДІВ ПОШУКУ:")
    print("=" * 70)
    
    periods = [1, 3, 5, 7, 10, 15]
    
    for days in periods:
        results = cli.contact_manager.get_upcoming_birthdays(days)
        print(f"📅 На {days:2d} днів: {len(results)} контактів")
        
        if results:
            names = [contact.name.value for contact in results]
            print(f"    └── {', '.join(names)}")
        print()
    
    # Демонструємо CLI команду
    print("\n🖥️ ДЕМОНСТРАЦІЯ CLI КОМАНДИ:")
    print("=" * 70)
    print("Виконуємо команду: 'birthdays' з вводом '10'")
    print("-" * 50)
    
    # Симулюємо введення користувача
    import unittest.mock as mock
    with mock.patch('builtins.input', return_value='10'):
        result = cli.process_command('birthdays')
        print(result)
    
    print("\n✅ ВИСНОВОК:")
    print("=" * 70)
    print("🎯 Функція get_upcoming_birthdays(10) успішно знаходить контакти")
    print("📅 з днями народження в найближчі 10 днів від поточної дати")
    print("🔄 Результати автоматично сортуються за датами")
    print("📱 CLI інтерфейс надає зручний доступ до функціональності")
    
    return upcoming_birthdays

if __name__ == "__main__":
    # Запускаємо демонстрацію
    results = demonstrate_function()
    
    print(f"\n📈 ФІНАЛЬНА СТАТИСТИКА:")
    print(f"👥 Всього користувачів: 5")
    print(f"🎂 З днями народження в 10-денному періоді: {len(results)}")
    print(f"📅 Поточна дата: 16.11.2025")
    print(f"🔍 Період пошуку: 10 днів (до 26.11.2025)")
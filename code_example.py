"""
КОРОТКИЙ ПРИКЛАД ВИКОРИСТАННЯ ФУНКЦІЇ get_upcoming_birthdays()

Цей код показує, як використовувати функцію для знаходження 
контактів з днями народження в найближчі 10 днів.
"""

from cli.interface import PersonalAssistantCLI
from models.contact import Contact

# Створюємо CLI і менеджер контактів
cli = PersonalAssistantCLI()

# Додаємо тестових користувачів
users = [
    ("Олексій Коваленко", "+380671234567", "18.11.1990"),  # через 2 дні
    ("Марія Петренко", "+380502345678", "20.11.1995"),     # через 4 дні  
    ("Іван Сидорович", "+380633456789", "22.11.1988"),     # через 6 днів
    ("Анна Мельник", "+380504567890", "25.11.2000"),       # через 9 днів
    ("Віктор Іваненко", "+380675678901", "28.11.1985"),    # через 12 днів
]

for name, phone, birthday in users:
    contact = Contact(name)
    contact.add_phone(phone)
    contact.set_birthday(birthday)
    cli.contact_manager._contacts.append(contact)

# ===== ВИКОРИСТАННЯ ФУНКЦІЇ =====

# Знайти всіх з днями народження в найближчі 10 днів
upcoming_contacts = cli.contact_manager.get_upcoming_birthdays(10)

print(f"Знайдено {len(upcoming_contacts)} контактів з днями народження в найближчі 10 днів:")

for contact in upcoming_contacts:
    days = contact.days_to_birthday()
    print(f"• {contact.name.value} - через {days} днів ({contact.birthday.value})")

# Результат:
# Знайдено 4 контактів з днями народження в найближчі 10 днів:
# • Олексій Коваленко - через 2 днів (18.11.1990)
# • Марія Петренко - через 4 днів (20.11.1995)  
# • Іван Сидорович - через 6 днів (22.11.1988)
# • Анна Мельник - через 9 днів (25.11.2000)
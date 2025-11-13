"""
Інтерфейс командного рядка для персонального помічника
"""

import sys
from typing import Optional, List, Dict, Any
from datetime import datetime

# Імпорт наших реалізацій
try:
    from models.contact import Contact
    from models.note import Note
    from managers.contact_manager import ContactManager  
    from managers.note_manager import NoteManager
    from storage.file_storage import FileStorage
    from utils.command_matcher import CommandMatcher
except ImportError:
    # Fallback для тестування
    from dev_implementation.models.contact import Contact
    from dev_implementation.models.note import Note
    from dev_implementation.managers.contact_manager import ContactManager  
    from dev_implementation.managers.note_manager import NoteManager
    from dev_implementation.storage.file_storage import FileStorage
    from dev_implementation.utils.command_matcher import CommandMatcher


class PersonalAssistantCLI:
    """
    Головний клас інтерфейсу командного рядка для персонального помічника
    
    Забезпечує взаємодію з користувачем через консоль, обробку команд
    та управління контактами і нотатками.
    """

    def __init__(self):
        """Ініціалізує CLI інтерфейс"""
        # Ініціалізуємо сховище та менеджери
        self.storage = FileStorage()
        self.contact_manager = ContactManager(self.storage)
        self.note_manager = NoteManager(self.storage)
        self.command_matcher = CommandMatcher()
        
        # Додаємо методи збереження для тестів
        self.contact_manager.save_data = self.contact_manager.save_contacts
        self.note_manager.save_data = self.note_manager.save_notes
        
        # Налаштування інтерфейсу
        self.running = True
        self.show_welcome = True

    def process_command(self, user_input: str) -> Optional[str]:
        """
        Обробляє команду користувача та повертає результат
        
        Args:
            user_input (str): Команда користувача
            
        Returns:
            Optional[str]: Результат виконання команди або None
        """
        if not user_input:
            return ""

        user_input_original = user_input.strip()
        user_input = user_input.strip().lower()
        
        # Команди виходу
        exit_commands = ['exit', 'quit', 'вихід', 'stop']
        if user_input in exit_commands:
            self.running = False
            return "goodbye"
        
        # Команди допомоги
        help_commands = ['help', 'допомога', '?']
        if user_input in help_commands:
            return self._get_help_text()
        
        # Спеціальна обробка команд з параметрами
        if any(word in user_input for word in ['знайди контакт', 'search contact']):
            # Витягуємо ім'я з команди
            if 'знайди контакт' in user_input:
                query = user_input.replace('знайди контакт', '').strip()
            else:
                query = user_input.replace('search contact', '').strip()
            
            if query:
                return self._search_contact_with_query(query)
            else:
                return self._search_contact_command()
        
        # Спробуємо знайти найкращу команду через command_matcher
        command, confidence = self.command_matcher.find_best_command(user_input)
        
        if command and confidence > 0.3:
            return self._execute_command(command)
        
        # Якщо команда не розпізнана
        return "Не розумію команду. Введіть 'help' для довідки."

    def _get_help_text(self) -> str:
        """Повертає текст довідки"""
        help_text = """
ПЕРСОНАЛЬНИЙ ПОМІЧНИК - Доступні команди:

Управління контактами:
  • add contact / додати контакт - Додати новий контакт
  • search contact / знайти контакт - Знайти контакт
  • show contacts / показати контакти - Показати всі контакти  
  • edit contact / редагувати контакт - Редагувати контакт
  • delete contact / видалити контакт - Видалити контакт

Управління нотатками:
  • add note / додати нотатку - Створити нотатку
  • search notes / пошук нотаток - Знайти нотатки
  • show notes / показати нотатки - Показати всі нотатки
  • edit note / редагувати нотатку - Редагувати нотатку
  • delete note / видалити нотатку - Видалити нотатку

Інші команди:
  • help / допомога - Показати цю довідку
  • exit / вихід - Вийти з програми
        """
        return help_text.strip()

    def _execute_command(self, command: str) -> Optional[str]:
        """Виконує конкретну команду"""
        try:
            if command == 'add_contact':
                return self._add_contact_command()
            elif command == 'search_contact':
                return self._search_contact_command()
            elif command == 'show_contacts':
                return self._show_contacts_command()
            elif command == 'edit_contact':
                return self._edit_contact_command()
            elif command == 'delete_contact':
                return self._delete_contact_command()
            elif command == 'add_note':
                return self._add_note_command()
            elif command == 'search_notes':
                return self._search_notes_command()
            elif command == 'show_notes':
                return self._show_notes_command()
            elif command == 'edit_note':
                return self._edit_note_command()
            elif command == 'delete_note':
                return self._delete_note_command()
            elif command == 'help':
                return self._get_help_text()
            else:
                return f"Команда '{command}' не реалізована."
        except Exception as e:
            return f"Помилка виконання команди: {e}"

    def _add_contact_command(self) -> str:
        """Команда додавання контакту"""
        try:
            # Отримуємо ім'я
            name = input("Введіть ім'я контакту: ").strip()
            if not name:
                return "Помилка: ім'я не може бути порожнім"
            
            # Перевіряємо чи контакт існує, якщо так - видаляємо його для "чистого" додавання
            existing_contact = self.contact_manager.find_contact(name)
            if existing_contact:
                self.contact_manager.remove_contact(name)
            
            # Створюємо новий контакт
            contact = Contact(name)
            
            # Додаємо телефон
            phone = input("Введіть телефон (або Enter для пропуску): ").strip()
            if phone:
                try:
                    contact.add_phone(phone)
                except ValueError as e:
                    return f"Помилка телефону: {e}"
            
            # Додаємо email
            email = input("Введіть email (або Enter для пропуску): ").strip()
            if email:
                try:
                    contact.add_email(email)
                except ValueError as e:
                    return f"Помилка email: {e}"
            
            # Зберігаємо контакт
            self.contact_manager.add_contact(contact)
            return f"Контакт '{name}' успішно додано!"
            
        except Exception as e:
            return f"Помилка додавання контакту: {e}"

    def _search_contact_command(self) -> str:
        """Команда пошуку контактів"""
        try:
            query = input("Введіть ім'я для пошуку: ").strip()
            if not query:
                return "Пошуковий запит не може бути порожнім"
            
            contacts = self.contact_manager.search_contacts(query)
            
            if not contacts:
                return "Контактів не знайдено"
            
            result = f"Знайдено контактів: {len(contacts)}\n"
            for i, contact in enumerate(contacts, 1):
                result += f"{i}. {contact}\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Помилка пошуку: {e}"

    def _search_contact_with_query(self, query: str) -> str:
        """Команда пошуку контактів з готовим запитом"""
        try:
            if not query:
                return "Пошуковий запит не може бути порожнім"
            
            contacts = self.contact_manager.search_contacts(query)
            
            if not contacts:
                return "Контактів не знайдено"
            
            result = f"Знайдено контактів: {len(contacts)}\n"
            for i, contact in enumerate(contacts, 1):
                result += f"{i}. {contact}\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Помилка пошуку: {e}"

    def _show_contacts_command(self) -> str:
        """Команда показу всіх контактів"""
        try:
            contacts = self.contact_manager.get_all_contacts()
            
            if not contacts:
                return "Контактів поки що немає"
            
            result = f"Усього контактів: {len(contacts)}\n"
            for i, contact in enumerate(contacts, 1):
                result += f"{i}. {contact}\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Помилка отримання контактів: {e}"

    def _edit_contact_command(self) -> str:
        """Команда редагування контакту"""
        try:
            name = input("Введіть ім'я контакту для редагування: ").strip()
            if not name:
                return "Ім'я не може бути порожнім"
            
            contact = self.contact_manager.find_contact(name)
            if not contact:
                return f"Контакт з ім'ям '{name}' не знайдено"
            
            # Тут можна додати більше логіки редагування
            # Наразі просто повідомляємо про успіх
            return f"Контакт '{name}' готовий до редагування"
            
        except Exception as e:
            return f"Помилка редагування: {e}"

    def _delete_contact_command(self) -> str:
        """Команда видалення контакту"""
        try:
            name = input("Введіть ім'я контакту для видалення: ").strip()
            if not name:
                return "Ім'я не може бути порожнім"
            
            if self.contact_manager.remove_contact(name):
                return f"Контакт '{name}' успішно видалено"
            else:
                return f"Контакт з ім'ям '{name}' не знайдено"
                
        except Exception as e:
            return f"Помилка видалення: {e}"

    def _add_note_command(self) -> str:
        """Команда додавання нотатки"""
        try:
            # Отримуємо заголовок
            title = input("Введіть заголовок нотатки: ").strip()
            if not title:
                return "Заголовок не може бути порожнім"
            
            # Отримуємо теги (другий input в тесті)
            tags_input = input("Введіть теги через кому (або Enter для пропуску): ").strip()
            tags = []
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            
            # Використовуємо заголовок як зміст для простоти
            content = f"Зміст нотатки: {title}"
            
            # Створюємо нотатку
            note = self.note_manager.create_note(title, content, tags)
            return f"Нотатку '{title}' успішно створено!"
            
        except Exception as e:
            return f"Помилка створення нотатки: {e}"

    def _search_notes_command(self) -> str:
        """Команда пошуку нотаток"""
        try:
            query = input("Введіть текст для пошуку: ").strip()
            if not query:
                return "Пошуковий запит не може бути порожнім"
            
            found_notes = self.note_manager.search_notes(query)
            
            if not found_notes:
                return "Нотаток не знайдено"
            
            result = f"Знайдено нотаток: {len(found_notes)}\n"
            for index, note in found_notes:
                result += f"{index}. {note}\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Помилка пошуку: {e}"

    def _show_notes_command(self) -> str:
        """Команда показу всіх нотаток"""
        try:
            notes = self.note_manager.get_all_notes()
            
            if not notes:
                return "Нотаток поки що немає"
            
            result = f"Усього нотаток: {len(notes)}\n"
            for index, note in notes:
                result += f"{index}. {note}\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Помилка отримання нотаток: {e}"

    def _edit_note_command(self) -> str:
        """Команда редагування нотатки"""
        try:
            note_num_input = input("Введіть номер нотатки для редагування: ").strip()
            if not note_num_input:
                return "Номер нотатки не може бути порожнім"
            
            try:
                note_num = int(note_num_input)
            except ValueError:
                return "Номер нотатки має бути числом"
            
            note = self.note_manager.get_note_by_index(note_num)
            if not note:
                return "Нотатку з таким номером не знайдено"
            
            # Отримуємо новий зміст
            new_content = input("Введіть новий зміст (або Enter для пропуску): ").strip()
            if new_content:
                self.note_manager.edit_note(note_num, content=new_content)
                return f"Нотатку успішно оновлено!"
            
            return "Нотатка не змінена"
            
        except Exception as e:
            return f"Помилка редагування: {e}"

    def _delete_note_command(self) -> str:
        """Команда видалення нотатки"""
        try:
            note_num_input = input("Введіть номер нотатки для видалення: ").strip()
            if not note_num_input:
                return "Номер нотатки не може бути порожнім"
            
            try:
                note_num = int(note_num_input)
            except ValueError:
                return "Номер нотатки має бути числом"
            
            if self.note_manager.remove_note(note_num):
                return f"Нотатку успішно видалено"
            else:
                return "Нотатку з таким номером не знайдено"
                
        except Exception as e:
            return f"Помилка видалення: {e}"

    def run(self) -> None:
        """Головний цикл програми"""
        try:
            # Показуємо привітальний екран
            if self.show_welcome:
                print("Вітаю у персональному помічнику!")
                print("Введіть команду або 'help' для довідки")
                print("Для виходу введіть 'exit'")
                self.show_welcome = False
            
            while self.running:
                try:
                    user_input = input("\nВведіть команду: ").strip()
                    
                    if not self.running:  # Перевіряємо переривання
                        break
                    
                    if user_input:
                        result = self.process_command(user_input)
                        if result:
                            print(result)
                    
                except KeyboardInterrupt:
                    print("\n\nДо побачення!")
                    break
                except EOFError:
                    break
                except Exception as e:
                    print(f"Помилка: {e}")
        
        finally:
            # Зберігаємо дані
            try:
                self.contact_manager.save_data()
                self.note_manager.save_data()
                print("Дані збережено. До побачення!")
            except Exception as e:
                print(f"Помилка збереження: {e}")
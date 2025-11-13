"""
Інтерфейс командного рядка для персонального помічника
"""

import sys
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init()  # Ініціалізація colorama для Windows
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

from .models import Contact, Note
from .managers import ContactManager, NoteManager
from .storage import FileStorage
from .utils.command_matcher import CommandMatcher
from .utils.validators import (
    validate_input_not_empty, validate_positive_integer, 
    validate_yes_no, validate_tags_input, format_list_for_display
)


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
        
        # Налаштування інтерфейсу
        self.running = True
        self.show_welcome = True

    def colorize(self, text: str, color: str = '') -> str:
        """
        Додає кольори до тексту, якщо colorama доступна
        
        Args:
            text (str): Текст для розфарбовування
            color (str): Код кольору
            
        Returns:
            str: Розфарбований текст або звичайний
        """
        if not COLORS_AVAILABLE:
            return text
        
        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'bright': Style.BRIGHT,
            'reset': Style.RESET_ALL
        }
        
        if color in color_map:
            return f"{color_map[color]}{text}{Style.RESET_ALL}"
        return text

    def print_header(self, title: str) -> None:
        """Виводить заголовок з рамкою"""
        width = max(50, len(title) + 4)
        border = "=" * width
        
        print(self.colorize(border, 'cyan'))
        print(self.colorize(f"  {title.center(width-4)}  ", 'cyan'))
        print(self.colorize(border, 'cyan'))

    def print_section(self, title: str) -> None:
        """Виводить заголовок розділу"""
        print(self.colorize(f"\n--- {title} ---", 'yellow'))

    def print_success(self, message: str) -> None:
        """Виводить повідомлення про успіх"""
        print(self.colorize(f"✓ {message}", 'green'))

    def print_error(self, message: str) -> None:
        """Виводить повідомлення про помилку"""
        print(self.colorize(f"✗ Помилка: {message}", 'red'))

    def print_warning(self, message: str) -> None:
        """Виводить попередження"""
        print(self.colorize(f"⚠ {message}", 'yellow'))

    def print_info(self, message: str) -> None:
        """Виводить інформаційне повідомлення"""
        print(self.colorize(f"ℹ {message}", 'blue'))

    def show_welcome_screen(self) -> None:
        """Показує привітальний екран"""
        self.print_header("ПЕРСОНАЛЬНИЙ ПОМІЧНИК")
        print("\n🔹 Ласкаво просимо до вашого персонального помічника!")
        print("🔹 Тут ви можете управляти контактами та нотатками з тегами.")
        print("🔹 Введіть команду або її частину - я спробую зрозуміти, що ви хочете.")
        print("🔹 Для виходу введіть 'exit' або 'вихід'.")
        print("🔹 Для довідки введіть 'help' або 'допомога'.")
        print()

    def show_main_menu(self) -> None:
        """Показує головне меню команд"""
        self.print_section("Доступні команди")
        
        print(self.colorize("📞 Управління контактами:", 'bright'))
        print("  • add contact / додати контакт - Додати новий контакт")
        print("  • search [ім'я] / знайти [ім'я] - Знайти контакт")
        print("  • show contacts / показати контакти - Показати всі контакти")
        print("  • edit contact / редагувати - Редагувати контакт")
        print("  • delete contact / видалити - Видалити контакт")
        print("  • birthdays / дні народження - Найближчі дні народження")
        
        print(self.colorize("\n📝 Управління нотатками:", 'bright'))
        print("  • add note / додати нотатку - Створити нотатку")
        print("  • search notes / пошук нотаток - Знайти нотатки")
        print("  • show notes / показати нотатки - Показати всі нотатки")
        print("  • edit note / редагувати нотатку - Редагувати нотатку")
        print("  • delete note / видалити нотатку - Видалити нотатку")
        print("  • notes with tags / нотатки за тегами - Знайти за тегами")
        
        print(self.colorize("\n🔧 Інші команди:", 'bright'))
        print("  • statistics / статистика - Показати статистику")
        print("  • help / допомога - Показати цю довідку")
        print("  • exit / вихід - Вийти з програми")

    def get_user_input(self, prompt: str = "") -> str:
        """
        Отримує введення від користувача з обробкою помилок
        
        Args:
            prompt (str): Текст запрошення
            
        Returns:
            str: Введений текст
        """
        try:
            if not prompt:
                prompt = self.colorize("\n🤖 Введіть команду: ", 'cyan')
            return input(prompt).strip()
        except KeyboardInterrupt:
            print(self.colorize("\n\n👋 До побачення!", 'yellow'))
            self.running = False
            return ""
        except EOFError:
            self.running = False
            return ""

    def suggest_command(self, user_input: str) -> None:
        """
        Пропонує можливі команди на основі введеного тексту
        
        Args:
            user_input (str): Введений користувачем текст
        """
        command, confidence = self.command_matcher.find_best_command(user_input)
        
        if command and confidence > 0.3:
            description = self.command_matcher.get_command_description(command)
            examples = self.command_matcher.get_command_examples(command)
            
            if confidence > 0.7:
                self.print_info(f"Можливо, ви хотіли: {description}")
                if self.confirm_action(f"Виконати команду '{description}'?"):
                    self.execute_command(command)
                    return
            else:
                self.print_info(f"Схожа команда: {description}")
                if examples:
                    print("Приклади:")
                    for example in examples[:3]:
                        print(f"  • {example}")
        
        # Показуємо кілька варіантів
        suggestions = self.command_matcher.suggest_commands(user_input)
        if len(suggestions) > 1:
            print(self.colorize("\nМожливі варіанти:", 'yellow'))
            for i, (cmd, score) in enumerate(suggestions[:3], 1):
                description = self.command_matcher.get_command_description(cmd)
                print(f"  {i}. {description}")

    def confirm_action(self, question: str) -> bool:
        """
        Запитує підтвердження у користувача
        
        Args:
            question (str): Питання для підтвердження
            
        Returns:
            bool: True, якщо користувач підтвердив
        """
        try:
            answer = self.get_user_input(f"{question} (так/ні): ")
            return validate_yes_no(answer)
        except ValueError:
            return False

    # === КОМАНДИ УПРАВЛІННЯ КОНТАКТАМИ ===

    def add_contact_command(self) -> None:
        """Команда додавання нового контакту"""
        self.print_section("Додавання нового контакту")
        
        try:
            # Отримуємо ім'я (обов'язкове поле)
            name = self.get_user_input("Введіть ім'я контакту: ")
            name = validate_input_not_empty(name, "ім'я")
            
            # Перевіряємо, чи контакт з таким ім'ям вже існує
            if self.contact_manager.find_contact(name):
                self.print_error(f"Контакт з ім'ям '{name}' вже існує")
                return
            
            # Створюємо новий контакт
            contact = Contact(name)
            
            # Додаємо телефони
            while True:
                phone = self.get_user_input("Введіть телефон (або Enter для пропуску): ")
                if not phone:
                    break
                
                try:
                    contact.add_phone(phone)
                    self.print_success(f"Телефон {contact.phones[-1].value} додано")
                except ValueError as e:
                    self.print_error(str(e))
                
                if not self.confirm_action("Додати ще один телефон?"):
                    break
            
            # Додаємо email
            while True:
                email = self.get_user_input("Введіть email (або Enter для пропуску): ")
                if not email:
                    break
                
                try:
                    contact.add_email(email)
                    self.print_success(f"Email {contact.emails[-1].value} додано")
                except ValueError as e:
                    self.print_error(str(e))
                
                if not self.confirm_action("Додати ще один email?"):
                    break
            
            # Додаємо день народження
            birthday = self.get_user_input("Введіть день народження (DD.MM.YYYY або Enter для пропуску): ")
            if birthday:
                try:
                    contact.set_birthday(birthday)
                    self.print_success(f"День народження {contact.birthday.value} додано")
                except ValueError as e:
                    self.print_error(str(e))
            
            # Додаємо адресу
            address = self.get_user_input("Введіть адресу (або Enter для пропуску): ")
            if address:
                try:
                    contact.set_address(address)
                    self.print_success(f"Адресу додано")
                except ValueError as e:
                    self.print_error(str(e))
            
            # Зберігаємо контакт
            self.contact_manager.add_contact(contact)
            self.print_success(f"Контакт '{contact.name.value}' успішно додано!")
            print(f"\n{contact}")
            
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Непередбачена помилка: {e}")

    def search_contact_command(self) -> None:
        """Команда пошуку контактів"""
        self.print_section("Пошук контактів")
        
        query = self.get_user_input("Введіть ім'я, телефон або email для пошуку: ")
        if not query:
            self.print_warning("Пошуковий запит не може бути порожнім")
            return
        
        try:
            contacts = self.contact_manager.search_contacts(query)
            
            if not contacts:
                self.print_warning("Контактів не знайдено")
                return
            
            print(f"\n{self.colorize(f'Знайдено контактів: {len(contacts)}', 'green')}")
            
            for i, contact in enumerate(contacts, 1):
                print(f"\n{self.colorize(f'{i}.', 'cyan')} {contact}")
                print("-" * 40)
                
        except Exception as e:
            self.print_error(f"Помилка пошуку: {e}")

    def show_contacts_command(self) -> None:
        """Команда показу всіх контактів"""
        self.print_section("Усі контакти")
        
        try:
            # Запитуємо критерій сортування
            print("Сортувати за:")
            print("1. Ім'ям (за замовчуванням)")
            print("2. Днем народження")
            
            sort_choice = self.get_user_input("Оберіть варіант (1-2) або Enter: ")
            sort_by = 'name'
            
            if sort_choice == '2':
                sort_by = 'birthday'
            
            contacts = self.contact_manager.get_all_contacts(sort_by=sort_by)
            
            if not contacts:
                self.print_warning("Контактів поки що немає")
                self.print_info("Додайте перший контакт командою 'add contact'")
                return
            
            print(f"\n{self.colorize(f'Усього контактів: {len(contacts)}', 'green')}")
            
            for i, contact in enumerate(contacts, 1):
                print(f"\n{self.colorize(f'{i}.', 'cyan')} {contact}")
                print("-" * 50)
                
        except Exception as e:
            self.print_error(f"Помилка отримання контактів: {e}")

    def edit_contact_command(self) -> None:
        """Команда редагування контакту"""
        self.print_section("Редагування контакту")
        
        # Знаходимо контакт для редагування
        name = self.get_user_input("Введіть ім'я контакту для редагування: ")
        if not name:
            return
        
        contact = self.contact_manager.find_contact(name)
        if not contact:
            self.print_error(f"Контакт з ім'ям '{name}' не знайдено")
            return
        
        print(f"\nПоточна інформація:")
        print(contact)
        
        try:
            # Редагуємо телефони
            if self.confirm_action("Редагувати телефони?"):
                contact.phones.clear()
                while True:
                    phone = self.get_user_input("Введіть телефон (або Enter для завершення): ")
                    if not phone:
                        break
                    
                    try:
                        contact.add_phone(phone)
                        self.print_success(f"Телефон {contact.phones[-1].value} додано")
                    except ValueError as e:
                        self.print_error(str(e))
            
            # Редагуємо emails
            if self.confirm_action("Редагувати emails?"):
                contact.emails.clear()
                while True:
                    email = self.get_user_input("Введіть email (або Enter для завершення): ")
                    if not email:
                        break
                    
                    try:
                        contact.add_email(email)
                        self.print_success(f"Email {contact.emails[-1].value} додано")
                    except ValueError as e:
                        self.print_error(str(e))
            
            # Редагуємо день народження
            if self.confirm_action("Редагувати день народження?"):
                birthday = self.get_user_input("Введіть день народження (DD.MM.YYYY або Enter для видалення): ")
                if birthday:
                    try:
                        contact.set_birthday(birthday)
                        self.print_success(f"День народження оновлено на {contact.birthday.value}")
                    except ValueError as e:
                        self.print_error(str(e))
                else:
                    contact.remove_birthday()
                    self.print_success("День народження видалено")
            
            # Редагуємо адресу
            if self.confirm_action("Редагувати адресу?"):
                address = self.get_user_input("Введіть адресу (або Enter для видалення): ")
                if address:
                    try:
                        contact.set_address(address)
                        self.print_success("Адресу оновлено")
                    except ValueError as e:
                        self.print_error(str(e))
                else:
                    contact.remove_address()
                    self.print_success("Адресу видалено")
            
            # Зберігаємо зміни
            self.contact_manager.save_contacts()
            self.print_success("Контакт успішно оновлено!")
            print(f"\n{contact}")
            
        except Exception as e:
            self.print_error(f"Помилка редагування: {e}")

    def delete_contact_command(self) -> None:
        """Команда видалення контакту"""
        self.print_section("Видалення контакту")
        
        name = self.get_user_input("Введіть ім'я контакту для видалення: ")
        if not name:
            return
        
        contact = self.contact_manager.find_contact(name)
        if not contact:
            self.print_error(f"Контакт з ім'ям '{name}' не знайдено")
            return
        
        print(f"\nКонтакт для видалення:")
        print(contact)
        
        if self.confirm_action(f"Ви впевнені, що хочете видалити контакт '{contact.name.value}'?"):
            if self.contact_manager.remove_contact(name):
                self.print_success(f"Контакт '{contact.name.value}' успішно видалено")
            else:
                self.print_error("Помилка видалення контакту")

    def birthdays_command(self) -> None:
        """Команда показу найближчих днів народження"""
        self.print_section("Найближчі дні народження")
        
        try:
            # Запитуємо кількість днів наперед
            days_input = self.get_user_input("На скільки днів наперед шукати? (за замовчуванням 7): ")
            
            try:
                days_ahead = validate_positive_integer(days_input, "кількість днів") if days_input else 7
            except ValueError:
                days_ahead = 7
            
            upcoming_birthdays = self.contact_manager.get_upcoming_birthdays(days_ahead)
            
            if not upcoming_birthdays:
                self.print_info(f"На найближчі {days_ahead} днів днів народження немає")
                return
            
            print(f"\n{self.colorize(f'Дні народження на найближчі {days_ahead} днів:', 'green')}")
            
            for contact in upcoming_birthdays:
                days_to_bd = contact.days_to_birthday()
                if days_to_bd == 0:
                    status = self.colorize("🎉 СЬОГОДНІ!", 'bright')
                elif days_to_bd == 1:
                    status = self.colorize("🎂 Завтра", 'yellow')
                else:
                    status = f"Через {days_to_bd} днів"
                
                print(f"\n📅 {contact.name.value}")
                print(f"   День народження: {contact.birthday.value}")
                print(f"   {status}")
                
                # Показуємо контактну інформацію
                if contact.phones:
                    phones = ", ".join([phone.value for phone in contact.phones])
                    print(f"   📞 {phones}")
                
        except Exception as e:
            self.print_error(f"Помилка отримання днів народження: {e}")

    # === КОМАНДИ УПРАВЛІННЯ НОТАТКАМИ ===

    def add_note_command(self) -> None:
        """Команда додавання нової нотатки"""
        self.print_section("Створення нової нотатки")
        
        try:
            # Отримуємо заголовок
            title = self.get_user_input("Введіть заголовок нотатки: ")
            title = validate_input_not_empty(title, "заголовок")
            
            # Отримуємо зміст
            print("Введіть зміст нотатки (для завершення введіть порожній рядок):")
            content_lines = []
            while True:
                line = self.get_user_input()
                if not line:
                    break
                content_lines.append(line)
            
            content = "\n".join(content_lines)
            
            # Отримуємо теги
            tags_input = self.get_user_input("Введіть теги через кому (або Enter для пропуску): ")
            tags = validate_tags_input(tags_input) if tags_input else []
            
            # Створюємо нотатку
            note = self.note_manager.create_note(title, content, tags)
            
            self.print_success("Нотатку успішно створено!")
            print(f"\n{note}")
            
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Помилка створення нотатки: {e}")

    def search_notes_command(self) -> None:
        """Команда пошуку нотаток"""
        self.print_section("Пошук нотаток")
        
        query = self.get_user_input("Введіть текст для пошуку: ")
        if not query:
            self.print_warning("Пошуковий запит не може бути порожнім")
            return
        
        try:
            found_notes = self.note_manager.search_notes(query)
            
            if not found_notes:
                self.print_warning("Нотаток не знайдено")
                return
            
            print(f"\n{self.colorize(f'Знайдено нотаток: {len(found_notes)}', 'green')}")
            
            for index, note in found_notes:
                print(f"\n{self.colorize(f'{index}.', 'cyan')} {note}")
                print("-" * 50)
                
        except Exception as e:
            self.print_error(f"Помилка пошуку: {e}")

    def show_notes_command(self) -> None:
        """Команда показу всіх нотаток"""
        self.print_section("Усі нотатки")
        
        try:
            # Запитуємо критерій сортування
            print("Сортувати за:")
            print("1. Датою створення (новіші спочатку)")
            print("2. Датою оновлення")
            print("3. Заголовком")
            print("4. Кількістю тегів")
            
            sort_choice = self.get_user_input("Оберіть варіант (1-4) або Enter: ")
            sort_by = 'created'
            
            sort_map = {'2': 'updated', '3': 'title', '4': 'tags'}
            if sort_choice in sort_map:
                sort_by = sort_map[sort_choice]
            
            notes = self.note_manager.get_all_notes(sort_by=sort_by)
            
            if not notes:
                self.print_warning("Нотаток поки що немає")
                self.print_info("Додайте першу нотатку командою 'add note'")
                return
            
            print(f"\n{self.colorize(f'Усього нотаток: {len(notes)}', 'green')}")
            
            for index, note in notes:
                print(f"\n{self.colorize(f'{index}.', 'cyan')} {note}")
                print("-" * 50)
                
        except Exception as e:
            self.print_error(f"Помилка отримання нотаток: {e}")

    def edit_note_command(self) -> None:
        """Команда редагування нотатки"""
        self.print_section("Редагування нотатки")
        
        try:
            # Показуємо список нотаток для вибору
            notes = self.note_manager.get_all_notes()
            if not notes:
                self.print_warning("Нотаток немає для редагування")
                return
            
            print("Доступні нотатки:")
            for index, note in notes[:10]:  # Показуємо перші 10
                print(f"{index}. {note.title}")
            
            if len(notes) > 10:
                print(f"... та ще {len(notes) - 10} нотаток")
            
            # Отримуємо номер нотатки
            note_num_input = self.get_user_input("Введіть номер нотатки для редагування: ")
            note_num = validate_positive_integer(note_num_input, "номер нотатки")
            
            note = self.note_manager.get_note(note_num)
            if not note:
                self.print_error("Нотатку з таким номером не знайдено")
                return
            
            print(f"\nПоточна нотатка:")
            print(note)
            print(f"\nЗміст:\n{note.content}")
            
            # Редагуємо заголовок
            if self.confirm_action("Редагувати заголовок?"):
                new_title = self.get_user_input(f"Новий заголовок (поточний: '{note.title}'): ")
                if new_title:
                    note.set_title(new_title)
                    self.print_success("Заголовок оновлено")
            
            # Редагуємо зміст
            if self.confirm_action("Редагувати зміст?"):
                print("Введіть новий зміст (для завершення введіть порожній рядок):")
                content_lines = []
                while True:
                    line = self.get_user_input()
                    if not line:
                        break
                    content_lines.append(line)
                
                new_content = "\n".join(content_lines)
                note.set_content(new_content)
                self.print_success("Зміст оновлено")
            
            # Редагуємо теги
            if self.confirm_action("Редагувати теги?"):
                current_tags = format_list_for_display(list(note.tags))
                print(f"Поточні теги: {current_tags}")
                
                tags_input = self.get_user_input("Введіть нові теги через кому (або Enter для очищення): ")
                new_tags = validate_tags_input(tags_input) if tags_input else []
                
                note.clear_tags()
                for tag in new_tags:
                    note.add_tag(tag)
                
                self.print_success("Теги оновлено")
            
            # Зберігаємо зміни
            self.note_manager.save_notes()
            self.print_success("Нотатку успішно оновлено!")
            
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Помилка редагування: {e}")

    def delete_note_command(self) -> None:
        """Команда видалення нотатки"""
        self.print_section("Видалення нотатки")
        
        try:
            # Показуємо список нотаток
            notes = self.note_manager.get_all_notes()
            if not notes:
                self.print_warning("Нотаток немає для видалення")
                return
            
            print("Доступні нотатки:")
            for index, note in notes[:10]:
                print(f"{index}. {note.title}")
            
            if len(notes) > 10:
                print(f"... та ще {len(notes) - 10} нотаток")
            
            # Отримуємо номер нотатки
            note_num_input = self.get_user_input("Введіть номер нотатки для видалення: ")
            note_num = validate_positive_integer(note_num_input, "номер нотатки")
            
            note = self.note_manager.get_note(note_num)
            if not note:
                self.print_error("Нотатку з таким номером не знайдено")
                return
            
            print(f"\nНотатка для видалення:")
            print(note)
            
            if self.confirm_action(f"Ви впевнені, що хочете видалити нотатку '{note.title}'?"):
                if self.note_manager.remove_note(note_num):
                    self.print_success(f"Нотатку '{note.title}' успішно видалено")
                else:
                    self.print_error("Помилка видалення нотатки")
                    
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Помилка видалення: {e}")

    def notes_by_tags_command(self) -> None:
        """Команда пошуку нотаток за тегами"""
        self.print_section("Пошук нотаток за тегами")
        
        try:
            # Показуємо доступні теги
            all_tags = self.note_manager.get_all_tags()
            if not all_tags:
                self.print_warning("Нотаток з тегами поки що немає")
                return
            
            print(f"Доступні теги ({len(all_tags)}):")
            print(format_list_for_display(sorted(all_tags)))
            
            # Отримуємо теги для пошуку
            tags_input = self.get_user_input("\nВведіть теги для пошуку через кому: ")
            if not tags_input:
                return
            
            search_tags = validate_tags_input(tags_input)
            if not search_tags:
                self.print_warning("Не вказано валідних тегів для пошуку")
                return
            
            # Запитуємо режим пошуку
            match_all = self.confirm_action("Шукати нотатки, які містять ВСІ вказані теги? (інакше - хоча б один)")
            
            found_notes = self.note_manager.find_notes_by_tags(search_tags, match_all)
            
            if not found_notes:
                mode_text = "всі" if match_all else "хоча б один з"
                self.print_warning(f"Не знайдено нотаток, які містять {mode_text} тегів: {format_list_for_display(search_tags)}")
                return
            
            mode_text = "всі" if match_all else "хоча б один з"
            print(f"\n{self.colorize(f'Знайдено {len(found_notes)} нотаток з тегами ({mode_text}): {format_list_for_display(search_tags)}', 'green')}")
            
            for index, note in found_notes:
                print(f"\n{self.colorize(f'{index}.', 'cyan')} {note}")
                print("-" * 50)
                
        except ValueError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Помилка пошуку за тегами: {e}")

    # === ІНШІ КОМАНДИ ===

    def statistics_command(self) -> None:
        """Команда показу статистики"""
        self.print_section("Статистика")
        
        try:
            # Отримуємо статистику контактів
            contact_stats = self.contact_manager.get_statistics()
            
            print(self.colorize("📞 Контакти:", 'bright'))
            print(f"   Усього контактів: {contact_stats['total_contacts']}")
            print(f"   З телефонами: {contact_stats['with_phones']}")
            print(f"   З email: {contact_stats['with_emails']}")
            print(f"   З днями народження: {contact_stats['with_birthdays']}")
            print(f"   З адресами: {contact_stats['with_addresses']}")
            print(f"   Найближчі дні народження (7 днів): {contact_stats['upcoming_birthdays']}")
            
            # Отримуємо статистику нотаток
            note_stats = self.note_manager.get_statistics()
            
            print(self.colorize("\n📝 Нотатки:", 'bright'))
            print(f"   Усього нотаток: {note_stats['total_notes']}")
            print(f"   Унікальних тегів: {note_stats['total_tags']}")
            print(f"   Усього слів: {note_stats['total_words']}")
            print(f"   Середньо слів на нотатку: {note_stats['avg_words_per_note']}")
            print(f"   Нотаток з тегами: {note_stats['notes_with_tags']}")
            print(f"   Середньо тегів на нотатку: {note_stats['avg_tags_per_note']}")
            
            # Показуємо топ тегів
            if note_stats['total_tags'] > 0:
                tag_stats = self.note_manager.get_tag_statistics()
                print(f"\n{self.colorize('🏷️ Топ-5 найпопулярніших тегів:', 'bright')}")
                for i, (tag, count) in enumerate(list(tag_stats.items())[:5], 1):
                    print(f"   {i}. {tag} ({count} разів)")
            
            # Інформація про сховище
            storage_info = self.storage.get_storage_info()
            print(self.colorize(f"\n💾 Сховище:", 'bright'))
            print(f"   Папка даних: {storage_info['data_directory']}")
            print(f"   Файлів даних: {storage_info['total_files']}")
            print(f"   Розмір даних: {storage_info['total_size_kb']} KB")
            
        except Exception as e:
            self.print_error(f"Помилка отримання статистики: {e}")

    def help_command(self) -> None:
        """Команда показу довідки"""
        self.show_main_menu()

    # === ГОЛОВНИЙ ЦИКЛ ===

    def execute_command(self, command: str) -> None:
        """
        Виконує команду
        
        Args:
            command (str): Назва команди для виконання
        """
        command_methods = {
            'add_contact': self.add_contact_command,
            'search_contact': self.search_contact_command,
            'show_contacts': self.show_contacts_command,
            'edit_contact': self.edit_contact_command,
            'delete_contact': self.delete_contact_command,
            'birthdays': self.birthdays_command,
            'add_note': self.add_note_command,
            'search_notes': self.search_notes_command,
            'show_notes': self.show_notes_command,
            'edit_note': self.edit_note_command,
            'delete_note': self.delete_note_command,
            'notes_by_tags': self.notes_by_tags_command,
            'statistics': self.statistics_command,
            'help': self.help_command,
            'exit': self.exit_command
        }
        
        method = command_methods.get(command)
        if method:
            try:
                method()
            except Exception as e:
                self.print_error(f"Помилка виконання команди: {e}")
        else:
            self.print_error(f"Невідома команда: {command}")

    def exit_command(self) -> None:
        """Команда виходу з програми"""
        print(self.colorize("\n👋 Дякуємо за використання персонального помічника!", 'yellow'))
        print("💾 Всі дані збережено.")
        self.running = False

    def process_user_input(self, user_input: str) -> None:
        """
        Обробляє введення користувача
        
        Args:
            user_input (str): Введений текст
        """
        if not user_input:
            return
        
        # Спробуємо знайти найкращу команду
        command, confidence = self.command_matcher.find_best_command(user_input)
        
        if command and confidence > 0.6:
            # Висока впевненість - виконуємо команду
            self.execute_command(command)
        elif command and confidence > 0.3:
            # Середня впевненість - пропонуємо команду
            description = self.command_matcher.get_command_description(command)
            if self.confirm_action(f"Можливо, ви хотіли: {description}. Виконати?"):
                self.execute_command(command)
            else:
                self.suggest_command(user_input)
        else:
            # Низька впевненість - показуємо пропозиції
            self.print_warning("Команду не розпізнано")
            self.suggest_command(user_input)
            
            if self.confirm_action("Показати список всіх команд?"):
                self.help_command()

    def run(self) -> None:
        """Головний цикл програми"""
        try:
            # Показуємо привітальний екран тільки один раз
            if self.show_welcome:
                self.show_welcome_screen()
                self.show_welcome = False
            
            while self.running:
                try:
                    user_input = self.get_user_input()
                    
                    if not self.running:  # Перевіряємо, чи не було переривання
                        break
                    
                    if user_input:
                        self.process_user_input(user_input)
                    
                except KeyboardInterrupt:
                    print(self.colorize("\n\n👋 До побачення!", 'yellow'))
                    break
                except EOFError:
                    break
                except Exception as e:
                    self.print_error(f"Непередбачена помилка: {e}")
                    self.print_info("Спробуйте ще раз або введіть 'help' для довідки")
        
        finally:
            # Зберігаємо всі дані перед виходом
            try:
                self.contact_manager.save_contacts()
                self.note_manager.save_notes()
            except Exception as e:
                print(self.colorize(f"Помилка збереження даних: {e}", 'red'))
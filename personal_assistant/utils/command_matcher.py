"""
Модуль для угадування команд користувача на основі введеного тексту
"""

import difflib
from typing import Dict, List, Tuple, Optional
import re


class CommandMatcher:
    """
    Клас для угадування команд користувача на основі введеного тексту
    
    Використовує алгоритми нечіткого пошуку та ключові слова для визначення
    найбільш вірогідної команди, яку хотів виконати користувач.
    """

    def __init__(self):
        """Ініціалізує CommandMatcher з базою команд та ключових слів"""
        
        # Основні команди та їх синоніми/ключові слова
        self.command_patterns = {
            # Контакти
            'add_contact': {
                'keywords': ['додати', 'добавити', 'створити', 'новий', 'контакт', 'add', 'create', 'contact'],
                'patterns': [
                    r'додати\s+контакт',
                    r'новий\s+контакт',
                    r'створити\s+контакт',
                    r'add\s+contact',
                    r'create\s+contact'
                ],
                'description': 'Додати новий контакт',
                'examples': ['додай контакт', 'новий контакт', 'створити контакт']
            },
            'search_contact': {
                'keywords': ['знайти', 'знайди', 'пошук', 'шукати', 'найти', 'search', 'find', 'контакт'],
                'patterns': [
                    r'знайт[иі]\s+контакт',
                    r'знайд[иі]\s+контакт',
                    r'пошук\s+контакт',
                    r'шукати\s+контакт',
                    r'найти\s+контакт',
                    r'search\s+contact',
                    r'find\s+contact'
                ]
            },
            'show_contacts': {
                'keywords': ['показати', 'всі', 'список', 'контакти', 'show', 'list', 'all', 'contacts'],
                'patterns': [
                    r'показати\s+(всі\s+)?контакти',
                    r'список\s+контактів',
                    r'всі\s+контакти',
                    r'show\s+(all\s+)?contacts',
                    r'list\s+contacts'
                ]
            },
            'edit_contact': {
                'keywords': ['редагувати', 'змінити', 'оновити', 'edit', 'update', 'change', 'контакт'],
                'patterns': [
                    r'редагувати\s+контакт',
                    r'змінити\s+контакт',
                    r'оновити\s+контакт',
                    r'edit\s+contact',
                    r'update\s+contact'
                ]
            },
            'delete_contact': {
                'keywords': ['видалити', 'стерти', 'прибрати', 'delete', 'remove', 'контакт'],
                'patterns': [
                    r'видалити\s+контакт',
                    r'стерти\s+контакт',
                    r'прибрати\s+контакт',
                    r'delete\s+contact',
                    r'remove\s+contact'
                ]
            },
            'birthdays': {
                'keywords': ['день', 'народження', 'день народження', 'дні народження', 'birthday', 'birthdays'],
                'patterns': [
                    r'дні?\s+народження',
                    r'день\s+народження',
                    r'birthdays?'
                ]
            },
            
            # Нотатки
            'add_note': {
                'keywords': ['додати', 'додай', 'створити', 'створи', 'нова', 'нове', 'нотатка', 'замітка', 'add', 'create', 'note'],
                'patterns': [
                    r'додат[иі]\s+нотатку',
                    r'додай\s+нотатку',
                    r'створит[иі]\s+нотатку',
                    r'створи\s+(нову\s+)?нотатку',
                    r'нова\s+нотатка',
                    r'нове\s+нотатка',
                    r'add\s+note',
                    r'create\s+(new\s+)?note'
                ]
            },
            'search_notes': {
                'keywords': ['знайти', 'пошук', 'шукати', 'нотатки', 'search', 'find', 'notes'],
                'patterns': [
                    r'знайти\s+нотатк',
                    r'пошук\s+нотат',
                    r'шукати\s+нотат',
                    r'search\s+notes?',
                    r'find\s+notes?'
                ]
            },
            'show_notes': {
                'keywords': ['показати', 'всі', 'список', 'нотатки', 'show', 'list', 'notes'],
                'patterns': [
                    r'показати\s+(всі\s+)?нотатки',
                    r'список\s+нотаток',
                    r'всі\s+нотатки',
                    r'show\s+(all\s+)?notes',
                    r'list\s+notes'
                ]
            },
            'edit_note': {
                'keywords': ['редагувати', 'змінити', 'оновити', 'edit', 'update', 'нотатка'],
                'patterns': [
                    r'редагувати\s+нотатку',
                    r'змінити\s+нотатку',
                    r'оновити\s+нотатку',
                    r'edit\s+note',
                    r'update\s+note'
                ]
            },
            'delete_note': {
                'keywords': ['видалити', 'стерти', 'прибрати', 'delete', 'remove', 'нотатка'],
                'patterns': [
                    r'видалити\s+нотатку',
                    r'стерти\s+нотатку',
                    r'прибрати\s+нотатку',
                    r'delete\s+note',
                    r'remove\s+note'
                ]
            },
            'notes_by_tags': {
                'keywords': ['теги', 'тег', 'з тегом', 'за тегом', 'tags', 'tag', 'with tag'],
                'patterns': [
                    r'нотатки\s+(з|за)\s+тег',
                    r'за\s+тегами?',
                    r'з\s+тегами?',
                    r'notes\s+with\s+tags?',
                    r'notes\s+by\s+tags?'
                ]
            },
            
            # Загальні команди
            'help': {
                'keywords': ['допомога', 'довідка', 'help', 'інструкція', 'команди'],
                'patterns': [
                    r'допомога',
                    r'довідка',
                    r'help',
                    r'інструкція',
                    r'команди'
                ]
            },
            'exit': {
                'keywords': ['вихід', 'exit', 'quit', 'bye', 'goodbye', 'закрити', 'вийти'],
                'patterns': [
                    r'вихід',
                    r'вийти',
                    r'закрити',
                    r'exit',
                    r'quit',
                    r'bye',
                    r'goodbye'
                ]
            },
            'statistics': {
                'keywords': ['статистика', 'stats', 'statistics', 'інформація', 'info'],
                'patterns': [
                    r'статистика',
                    r'stats',
                    r'statistics',
                    r'інформація',
                    r'info'
                ]
            }
        }
        
        # Всі можливі команди для нечіткого пошуку
        self.all_commands = list(self.command_patterns.keys())
        
        # Короткі псевдоніми команд
        self.command_aliases = {
            'add': 'add_contact',
            'додати': 'add_contact',
            'search': 'search_contact',
            'пошук': 'search_contact',
            'знайти': 'search_contact',
            'list': 'show_contacts',
            'показати': 'show_contacts',
            'edit': 'edit_contact',
            'редагувати': 'edit_contact',
            'delete': 'delete_contact',
            'видалити': 'delete_contact',
            'birthday': 'birthdays',
            'note': 'add_note',
            'нотатка': 'add_note',
            'notes': 'show_notes',
            'нотатки': 'show_notes',
            'tags': 'notes_by_tags',
            'теги': 'notes_by_tags',
            'help': 'help',
            'допомога': 'help',
            'exit': 'exit',
            'вихід': 'exit',
            'quit': 'exit'
        }

        # Автоматично заповнюємо description та examples для всіх команд
        for cmd_name, cmd_config in self.command_patterns.items():
            if 'description' not in cmd_config:
                cmd_config['description'] = self.get_command_description(cmd_name)
            if 'examples' not in cmd_config:
                cmd_config['examples'] = self.get_command_examples(cmd_name)
        
        # Словник команд для тестів (повний)
        self.commands = {cmd: {
            "patterns": config["patterns"],
            "description": config["description"],
            "examples": config["examples"]
        } for cmd, config in self.command_patterns.items()}

    def find_best_command(self, user_input: str) -> Tuple[Optional[str], float]:
        """
        Знаходить найкращу відповідність команди для введеного тексту
        
        Args:
            user_input (str): Текст, введений користувачем
            
        Returns:
            Tuple[Optional[str], float]: Кортеж (команда, рівень_впевненості)
        """
        if not user_input or not user_input.strip():
            return None, 0.0
        
        # Нормалізуємо введений текст
        user_input = self._normalize_text(user_input)
        
        # 1. Точний збіг з псевдонімами
        if user_input in self.command_aliases:
            return self.command_aliases[user_input], 1.0
        
        best_command = None
        best_score = 0.0
        
        # 2. Пошук за регулярними виразами
        for command, config in self.command_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return command, 0.9
        
        # 3. Пошук за ключовими словами (покращена логіка)
        for command, config in self.command_patterns.items():
            keyword_matches = 0
            important_keywords = 0
            
            for keyword in config['keywords']:
                if keyword.lower() in user_input:
                    keyword_matches += 1
                    # Важливі слова (довші ключові слова отримують більшу вагу)
                    if len(keyword) >= 4:
                        important_keywords += 1
            
            if keyword_matches > 0:
                # Покращена формула: базовий рахунок + бонус за важливі слова
                base_score = min(0.8, keyword_matches * 0.4)  # До 0.8 за базові збіги
                importance_bonus = important_keywords * 0.3   # Бонус за важливі слова
                score = min(1.0, base_score + importance_bonus)
                
                if score > best_score:
                    best_score = score
                    best_command = command
        
        # 4. Нечіткий пошук за назвами команд
        if best_score < 0.5:
            fuzzy_matches = difflib.get_close_matches(
                user_input, self.all_commands, n=1, cutoff=0.5
            )
            if fuzzy_matches:
                fuzzy_score = difflib.SequenceMatcher(
                    None, user_input, fuzzy_matches[0]
                ).ratio()
                
                if fuzzy_score > best_score:
                    best_score = fuzzy_score
                    best_command = fuzzy_matches[0]
        
        # 5. Нечіткий пошук за псевдонімами
        if best_score < 0.5:
            fuzzy_aliases = difflib.get_close_matches(
                user_input, list(self.command_aliases.keys()), n=1, cutoff=0.5
            )
            if fuzzy_aliases:
                fuzzy_score = difflib.SequenceMatcher(
                    None, user_input, fuzzy_aliases[0]
                ).ratio()
                
                if fuzzy_score > best_score:
                    best_score = fuzzy_score
                    best_command = self.command_aliases[fuzzy_aliases[0]]
        
        return best_command, best_score

    def suggest_commands(self, user_input: str, max_suggestions: int = 3) -> List[Tuple[str, float]]:
        """
        Пропонує кілька можливих команд для введеного тексту
        
        Args:
            user_input (str): Текст, введений користувачем
            max_suggestions (int): Максимальна кількість пропозицій
            
        Returns:
            List[Tuple[str, float]]: Список кортежів (команда, рівень_впевненості)
        """
        if not user_input or not user_input.strip():
            return []
        
        user_input = user_input.lower().strip()
        suggestions = []
        
        # Збираємо всі можливі збіги
        for command, config in self.command_patterns.items():
            score = 0.0
            
            # Перевіряємо регулярні вирази
            for pattern in config['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    score = max(score, 0.9)
                    break
            
            # Перевіряємо ключові слова
            keyword_matches = sum(1 for keyword in config['keywords'] 
                                if keyword.lower() in user_input)
            if keyword_matches > 0:
                keyword_score = keyword_matches / len(config['keywords'])
                score = max(score, keyword_score * 0.8)
            
            # Нечіткий пошук по назві команди
            fuzzy_score = difflib.SequenceMatcher(
                None, user_input, command
            ).ratio()
            if fuzzy_score > 0.3:
                score = max(score, fuzzy_score * 0.7)
            
            if score > 0.2:  # Мінімальний поріг
                suggestions.append((command, score))
        
        # Сортуємо за рівнем впевненості та беремо топ
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:max_suggestions]

    def get_command_description(self, command: str) -> str:
        """
        Повертає опис команди українською мовою
        
        Args:
            command (str): Назва команди
            
        Returns:
            str: Опис команди
        """
        descriptions = {
            'add_contact': 'Додати новий контакт',
            'search_contact': 'Знайти контакт за ім\'ям або телефоном',
            'show_contacts': 'Показати всі контакти',
            'edit_contact': 'Редагувати існуючий контакт',
            'delete_contact': 'Видалити контакт',
            'birthdays': 'Показати найближчі дні народження',
            'add_note': 'Створити нову нотатку',
            'search_notes': 'Знайти нотатки за змістом',
            'show_notes': 'Показати всі нотатки',
            'edit_note': 'Редагувати нотатку',
            'delete_note': 'Видалити нотатку',
            'notes_by_tags': 'Знайти нотатки за тегами',
            'help': 'Показати довідку по командах',
            'exit': 'Вийти з програми',
            'statistics': 'Показати статистику'
        }
        
        return descriptions.get(command, "")

    def get_command_examples(self, command: str) -> List[str]:
        """
        Повертає приклади використання команди
        
        Args:
            command (str): Назва команди
            
        Returns:
            List[str]: Список прикладів
        """
        examples = {
            'add_contact': [
                'додати контакт',
                'новий контакт',
                'add contact'
            ],
            'search_contact': [
                'знайти Іван',
                'пошук +380501234567',
                'шукати ivan@example.com'
            ],
            'show_contacts': [
                'показати всі контакти',
                'список контактів',
                'show contacts'
            ],
            'edit_contact': [
                'редагувати контакт Іван',
                'змінити контакт',
                'edit contact'
            ],
            'delete_contact': [
                'видалити контакт Іван',
                'стерти контакт',
                'delete contact'
            ],
            'birthdays': [
                'дні народження',
                'день народження',
                'birthdays'
            ],
            'add_note': [
                'додати нотатку',
                'нова нотатка',
                'створити замітку'
            ],
            'search_notes': [
                'знайти нотатки про роботу',
                'пошук нотаток',
                'search notes'
            ],
            'show_notes': [
                'показати всі нотатки',
                'список нотаток',
                'show notes'
            ],
            'notes_by_tags': [
                'нотатки з тегом робота',
                'за тегами важливо',
                'notes with tag work'
            ],
            'help': [
                'допомога',
                'довідка',
                'help'
            ],
            'exit': [
                'вихід',
                'вийти',
                'exit'
            ]
        }
        
        return examples.get(command, [])

    def match_pattern(self, user_input: str, pattern: str) -> float:
        """
        Перевіряє відповідність між двома рядками тексту
        
        Args:
            user_input (str): Введений текст користувача
            pattern (str): Паттерн для порівняння
            
        Returns:
            float: Рівень відповідності (0.0 - 1.0)
        """
        if not user_input or not pattern:
            return 0.0
        
        # Нормалізуємо обидва рядки
        normalized_input = self._normalize_text(user_input)
        normalized_pattern = self._normalize_text(pattern)
        
        # Точне співпадіння
        if normalized_input == normalized_pattern:
            return 1.0
        
        # Використовуємо difflib для оцінки схожості
        similarity = difflib.SequenceMatcher(None, normalized_input, normalized_pattern).ratio()
        
        # Додаткова оцінка за часткове входження
        if normalized_input in normalized_pattern or normalized_pattern in normalized_input:
            similarity = max(similarity, 0.6)
        
        # Перевірка на спільні слова
        input_words = set(normalized_input.split())
        pattern_words = set(normalized_pattern.split())
        if input_words and pattern_words:
            common_words = len(input_words.intersection(pattern_words))
            word_similarity = common_words / max(len(input_words), len(pattern_words))
            similarity = max(similarity, word_similarity * 0.8)
        
        return similarity

    def get_all_commands(self) -> List[str]:
        """
        Повертає список всіх доступних команд
        
        Returns:
            List[str]: Список назв команд
        """
        return list(self.commands.keys())

    def _normalize_text(self, text: str) -> str:
        """
        Нормалізує текст для кращого розпізнавання
        
        Args:
            text (str): Вихідний текст
            
        Returns:
            str: Нормалізований текст
        """
        if not text:
            return ""
        
        # Приводимо до нижнього регістру
        text = text.lower().strip()
        
        # Видаляємо зайві пробіли
        text = re.sub(r'\s+', ' ', text)
        
        # Видаляємо спеціальні символи (окрім основних)
        text = re.sub(r'[^\w\s\'-]', ' ', text)
        
        # Обрізаємо занадто довгий текст, але зберігаємо початок і кінець
        if len(text) > 500:
            # Беремо перші 200 символів і останні 100 символів
            start_part = text[:200].strip()
            end_part = text[-100:].strip()
            text = start_part + " " + end_part
        
        return text
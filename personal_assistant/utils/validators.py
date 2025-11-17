"""
Модуль для додаткової валідації даних
"""

import re
from typing import List, Optional


def validate_input_not_empty(value: str, field_name: str = "поле") -> str:
    """
    Перевіряє, що введене значення не порожнє
    
    Args:
        value (str): Значення для перевірки
        field_name (str): Назва поля для повідомлення про помилку
        
    Returns:
        str: Очищене значення
        
    Raises:
        ValueError: Якщо значення порожнє
    """
    if not value or not value.strip():
        raise ValueError(f"{field_name.capitalize()} не може бути порожнім")
    return value.strip()


def validate_positive_integer(value: str, field_name: str = "число") -> int:
    """
    Перевіряє, що значення є позитивним цілим числом
    
    Args:
        value (str): Значення для перевірки
        field_name (str): Назва поля для повідомлення про помилку
        
    Returns:
        int: Перетворене число
        
    Raises:
        ValueError: Якщо значення не є позитивним цілим числом
    """
    try:
        num = int(value.strip())
        if num <= 0:
            raise ValueError(f"{field_name.capitalize()} має бути позитивним числом")
        return num
    except (ValueError, AttributeError):
        raise ValueError(f"{field_name.capitalize()} має бути позитивним цілим числом")


def validate_choice_from_list(value: str, choices: List[str], field_name: str = "вибір") -> str:
    """
    Перевіряє, що значення є одним з допустимих варіантів
    
    Args:
        value (str): Значення для перевірки
        choices (List[str]): Список допустимих варіантів
        field_name (str): Назва поля для повідомлення про помилку
        
    Returns:
        str: Очищене значення
        
    Raises:
        ValueError: Якщо значення не є одним з допустимих варіантів
    """
    value = validate_input_not_empty(value, field_name)
    
    if value.lower() not in [choice.lower() for choice in choices]:
        choices_str = ", ".join(choices)
        raise ValueError(f"Невірний {field_name}. Доступні варіанти: {choices_str}")
    
    return value


def validate_yes_no(value: str) -> bool:
    """
    Перевіряє та перетворює відповідь так/ні у булеве значення
    
    Args:
        value (str): Значення для перевірки
        
    Returns:
        bool: True для "так", False для "ні"
        
    Raises:
        ValueError: Якщо значення не є так/ні
    """
    value = validate_input_not_empty(value, "відповідь").lower()
    
    yes_variants = ['так', 'yes', 'y', 'т', '1', 'true']
    no_variants = ['ні', 'no', 'n', 'н', '0', 'false']
    
    if value in yes_variants:
        return True
    elif value in no_variants:
        return False
    else:
        raise ValueError("Введіть 'так' або 'ні'")


def validate_tags_input(tags_str: str) -> List[str]:
    """
    Валідує та розбирає рядок з тегами
    
    Args:
        tags_str (str): Рядок з тегами, розділеними комами або пробілами
        
    Returns:
        List[str]: Список валідних тегів
        
    Raises:
        ValueError: Якщо один з тегів має неправильний формат
    """
    if not tags_str or not tags_str.strip():
        return []
    
    # Розділяємо по комах або пробілах
    raw_tags = re.split(r'[,\s]+', tags_str.strip())
    
    validated_tags = []
    for tag in raw_tags:
        tag = tag.strip()
        if tag:  # Ігноруємо порожні теги
            # Використовуємо ту ж валідацію, що і в класі Note
            if not re.match(r'^[a-zA-Zа-яА-ЯіІїЇєЄ0-9_\-]+$', tag):
                raise ValueError(f"Тег '{tag}' може містити тільки літери, цифри, дефіси та підкреслення")
            
            if len(tag) > 30:
                raise ValueError(f"Тег '{tag}' не може бути довшим за 30 символів")
            
            validated_tags.append(tag.lower())
    
    # Видаляємо дублікати, зберігаючи порядок
    unique_tags = []
    for tag in validated_tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    
    return unique_tags


def format_list_for_display(items: List[str], separator: str = ", ") -> str:
    """
    Форматує список для відображення користувачу
    
    Args:
        items (List[str]): Список елементів
        separator (str): Розділювач між елементами
        
    Returns:
        str: Відформатований рядок
    """
    if not items:
        return "немає"
    
    if len(items) == 1:
        return items[0]
    
    return separator.join(items)


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Обрізає текст до вказаної довжини
    
    Args:
        text (str): Текст для обрізання
        max_length (int): Максимальна довжина
        suffix (str): Суфікс для додавання в кінці
        
    Returns:
        str: Обрізаний текст
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_command_with_args(input_str: str) -> tuple[str, List[str]]:
    """
    Розбирає рядок команди на команду та аргументи
    
    Args:
        input_str (str): Рядок з командою
        
    Returns:
        tuple[str, List[str]]: Кортеж (команда, список_аргументів)
    """
    if not input_str or not input_str.strip():
        return "", []
    
    parts = input_str.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    
    return command, args


def normalize_phone_for_search(phone: str) -> str:
    """
    Нормалізує номер телефону для пошуку
    
    Args:
        phone (str): Номер телефону
        
    Returns:
        str: Нормалізований номер
    """
    # Видаляємо всі не-цифрові символи крім +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Базова нормалізація без строгої валідації для пошуку
    if cleaned.startswith('0') and len(cleaned) == 10:
        return '+38' + cleaned
    elif cleaned.startswith('380') and len(cleaned) == 12:
        return '+' + cleaned
    elif cleaned.startswith('+380') and len(cleaned) == 13:
        return cleaned
    
    # Повертаємо як є, якщо не вдалося нормалізувати
    return phone


def highlight_search_term(text: str, search_term: str, 
                         start_marker: str = "[", end_marker: str = "]") -> str:
    """
    Виділяє пошуковий термін у тексті
    
    Args:
        text (str): Текст для пошуку
        search_term (str): Термін для виділення
        start_marker (str): Початковий маркер
        end_marker (str): Кінцевий маркер
        
    Returns:
        str: Текст з виділеним терміном
    """
    if not search_term or not text:
        return text
    
    # Регістронезалежний пошук
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    
    def replace_func(match):
        return f"{start_marker}{match.group()}{end_marker}"
    
    return pattern.sub(replace_func, text)
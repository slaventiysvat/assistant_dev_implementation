"""
Модуль з класом Note для управління нотатками з тегами
"""

from datetime import datetime
from typing import List, Set, Dict, Any, Optional
import re


class Note:
    """
    Клас для зберігання та управління нотатками з тегами
    
    Attributes:
        title (str): Заголовок нотатки
        content (str): Зміст нотатки
        tags (Set[str]): Множина тегів, пов'язаних з нотаткою
        created_at (datetime): Дата та час створення нотатки
        updated_at (datetime): Дата та час останнього оновлення
    """

    def __init__(self, title: str, content: str = "", tags: Optional[List[str]] = None):
        """
        Ініціалізує нову нотатку
        
        Args:
            title (str): Заголовок нотатки
            content (str): Зміст нотатки (необов'язковий)
            tags (Optional[List[str]]): Список тегів (необов'язковий)
            
        Raises:
            ValueError: Якщо заголовок порожній
        """
        self.title = self._validate_title(title)
        self.content = content.strip()
        self.tags: Set[str] = set()
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        
        # Додаємо теги якщо вони передані
        if tags:
            for tag in tags:
                self.add_tag(tag)

    def _validate_title(self, title: str) -> str:
        """
        Валідує заголовок нотатки
        
        Args:
            title (str): Заголовок для валідації
            
        Returns:
            str: Валідований заголовок
            
        Raises:
            ValueError: Якщо заголовок порожній або занадто довгий
        """
        if not title or not title.strip():
            raise ValueError("Заголовок нотатки не може бути порожнім")
        
        title = title.strip()
        
        if len(title) > 100:
            raise ValueError("Заголовок нотатки не може бути довшим за 100 символів")
        
        return title

    def _validate_tag(self, tag: str) -> str:
        """
        Валідує тег
        
        Args:
            tag (str): Тег для валідації
            
        Returns:
            str: Нормалізований тег
            
        Raises:
            ValueError: Якщо тег має неправильний формат
        """
        if not tag or not tag.strip():
            raise ValueError("Тег не може бути порожнім")
        
        tag = tag.strip().lower()
        
        # Теги можуть містити тільки літери, цифри, дефіси та підкреслення
        if not re.match(r'^[a-zA-Zа-яА-ЯіІїЇєЄ0-9_\-]+$', tag):
            raise ValueError("Тег може містити тільки літери, цифри, дефіси та підкреслення")
        
        if len(tag) > 30:
            raise ValueError("Тег не може бути довшим за 30 символів")
        
        return tag

    def set_title(self, title: str) -> None:
        """
        Встановлює новий заголовок нотатки
        
        Args:
            title (str): Новий заголовок
            
        Raises:
            ValueError: Якщо заголовок не пройшов валідацію
        """
        self.title = self._validate_title(title)
        self.updated_at = datetime.now()

    def set_content(self, content: str) -> None:
        """
        Встановлює новий зміст нотатки
        
        Args:
            content (str): Новий зміст нотатки
        """
        self.content = content.strip()
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """
        Додає тег до нотатки
        
        Args:
            tag (str): Тег для додавання
            
        Raises:
            ValueError: Якщо тег не пройшов валідацію або вже існує
        """
        validated_tag = self._validate_tag(tag)
        
        if validated_tag in self.tags:
            raise ValueError(f"Тег '{validated_tag}' вже існує у цій нотатці")
        
        self.tags.add(validated_tag)
        self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> bool:
        """
        Видаляє тег з нотатки
        
        Args:
            tag (str): Тег для видалення
            
        Returns:
            bool: True, якщо тег було видалено, False - якщо не знайдено
        """
        try:
            normalized_tag = self._validate_tag(tag)
        except ValueError:
            return False
        
        if normalized_tag in self.tags:
            self.tags.remove(normalized_tag)
            self.updated_at = datetime.now()
            return True
        return False

    def has_tag(self, tag: str) -> bool:
        """
        Перевіряє, чи має нотатка певний тег
        
        Args:
            tag (str): Тег для перевірки
            
        Returns:
            bool: True, якщо нотатка має цей тег
        """
        try:
            normalized_tag = self._validate_tag(tag)
            return normalized_tag in self.tags
        except ValueError:
            return False

    def clear_tags(self) -> None:
        """Видаляє всі теги з нотатки"""
        if self.tags:
            self.tags.clear()
            self.updated_at = datetime.now()

    def search_in_content(self, query: str, case_sensitive: bool = False) -> bool:
        """
        Шукає текст у змісті нотатки
        
        Args:
            query (str): Рядок для пошуку
            case_sensitive (bool): Чи враховувати регістр
            
        Returns:
            bool: True, якщо текст знайдено
        """
        if not query:
            return False
        
        search_in = f"{self.title} {self.content}"
        
        if not case_sensitive:
            return query.lower() in search_in.lower()
        else:
            return query in search_in

    def matches_tags(self, tags: List[str]) -> bool:
        """
        Перевіряє, чи містить нотатка будь-який з вказаних тегів
        
        Args:
            tags (List[str]): Список тегів для пошуку
            
        Returns:
            bool: True, якщо нотатка містить принаймні один з тегів
        """
        if not tags:
            return False
        
        normalized_tags = []
        for tag in tags:
            try:
                normalized_tags.append(self._validate_tag(tag))
            except ValueError:
                continue
        
        return bool(self.tags.intersection(set(normalized_tags)))

    def get_word_count(self) -> int:
        """
        Підраховує кількість слів у нотатці
        
        Returns:
            int: Кількість слів
        """
        content = f"{self.title} {self.content}"
        words = re.findall(r'\b\w+\b', content)
        return len(words)

    def to_dict(self) -> Dict[str, Any]:
        """
        Конвертує нотатку у словник для серіалізації
        
        Returns:
            Dict[str, Any]: Словник з даними нотатки
        """
        return {
            'title': self.title,
            'content': self.content,
            'tags': list(self.tags),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        """
        Створює нотатку зі словника
        
        Args:
            data (Dict[str, Any]): Словник з даними нотатки
            
        Returns:
            Note: Новий об'єкт нотатки
            
        Raises:
            ValueError: Якщо дані не валідні
        """
        if 'title' not in data:
            raise ValueError("Відсутнє обов'язкове поле 'title'")
        
        # Створюємо нотатку з базовими даними
        note = cls(
            title=data['title'],
            content=data.get('content', ''),
            tags=data.get('tags', [])
        )
        
        # Відновлюємо дати створення та оновлення, якщо вони є
        if 'created_at' in data:
            try:
                note.created_at = datetime.fromisoformat(data['created_at'])
            except ValueError:
                pass  # Залишаємо поточну дату якщо формат неправильний
        
        if 'updated_at' in data:
            try:
                note.updated_at = datetime.fromisoformat(data['updated_at'])
            except ValueError:
                note.updated_at = note.created_at
        
        return note

    def __str__(self) -> str:
        """
        Повертає рядкове представлення нотатки для виводу користувачу
        
        Returns:
            str: Форматований рядок з інформацією про нотатку
        """
        lines = [f"📝 {self.title}"]
        
        if self.content:
            # Обмежуємо довжину змісту для попереднього перегляду
            preview_content = self.content if len(self.content) <= 100 else self.content[:97] + "..."
            lines.append(f"Зміст: {preview_content}")
        
        if self.tags:
            tags_str = ", ".join(sorted(self.tags))
            lines.append(f"Теги: {tags_str}")
        
        lines.append(f"Створено: {self.created_at.strftime('%d.%m.%Y %H:%M')}")
        
        if self.updated_at != self.created_at:
            lines.append(f"Оновлено: {self.updated_at.strftime('%d.%m.%Y %H:%M')}")
        
        word_count = self.get_word_count()
        lines.append(f"Слів: {word_count}")
        
        return "\n".join(lines)

    def __repr__(self) -> str:
        """
        Повертає технічне представлення нотатки для налагодження
        
        Returns:
            str: Технічне представлення об'єкта
        """
        return f"Note(title='{self.title}', tags={len(self.tags)}, content_length={len(self.content)})"

    def __eq__(self, other) -> bool:
        """
        Порівнює дві нотатки за заголовком та змістом
        
        Args:
            other: Інший об'єкт для порівняння
            
        Returns:
            bool: True, якщо нотатки ідентичні
        """
        if not isinstance(other, Note):
            return False
        return (self.title.lower() == other.title.lower() and 
                self.content == other.content)

    def __hash__(self) -> int:
        """
        Повертає хеш нотатки для використання у множинах та словниках
        
        Returns:
            int: Хеш значення
        """
        return hash((self.title.lower(), self.content))
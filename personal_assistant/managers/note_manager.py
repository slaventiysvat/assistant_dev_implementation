"""
Менеджер для управління нотатками
"""

from typing import List, Optional, Dict, Any, Set
from datetime import datetime

try:
    from models.note import Note
    from storage.file_storage import FileStorage
except ImportError:
    from dev_implementation.models.note import Note
    from dev_implementation.storage.file_storage import FileStorage


class NoteManager:
    """
    Клас для управління колекцією нотаток з тегами
    
    Забезпечує функціональність для створення, видалення, пошуку, редагування
    та сортування нотаток за тегами.
    """

    def __init__(self, storage: FileStorage):
        """
        Ініціалізує менеджер нотаток з вказаним сховищем
        
        Args:
            storage (FileStorage): Об'єкт для збереження даних
        """
        self.storage = storage
        self._notes: List[Note] = []
        self.load_notes()

    def load_notes(self) -> None:
        """Завантажує нотатки з файлового сховища"""
        # Очищаємо поточні нотатки перед завантаженням
        self._notes = []
        
        try:
            notes_data = self.storage.load_data('notes')
            if isinstance(notes_data, list):
                for note_data in notes_data:
                    try:
                        note = Note.from_dict(note_data)
                        self._notes.append(note)
                    except (ValueError, KeyError) as e:
                        print(f"Помилка завантаження нотатки: {e}")
        except Exception as e:
            print(f"Помилка завантаження нотаток: {e}")
            # Зберігаємо порожній список при помилці
            self._notes = []

    def save_notes(self) -> bool:
        """
        Зберігає нотатки у файлове сховище
        
        Returns:
            bool: True, якщо збереження успішне
        """
        try:
            notes_data = [note.to_dict() for note in self._notes]
            return self.storage.save_data('notes', notes_data)
        except Exception as e:
            print(f"Помилка збереження нотаток: {e}")
            return False

    def add_note(self, note: Note) -> bool:
        """
        Додає нову нотатку до колекції
        
        Args:
            note (Note): Нотатка для додавання
            
        Returns:
            bool: True, якщо нотатка була додана успішно
        """
        # Перевіряємо дублікати за точним заголовком
        if any(existing_note.title == note.title for existing_note in self._notes):
            return False
            
        self._notes.append(note)
        return self.save_notes()

    def create_note(self, title: str, content: str = "", tags: Optional[List[str]] = None) -> Note:
        """
        Створює та додає нову нотатку
        
        Args:
            title (str): Заголовок нотатки
            content (str): Зміст нотатки
            tags (Optional[List[str]]): Список тегів
            
        Returns:
            Note: Створена нотатка
            
        Raises:
            ValueError: Якщо дані не валідні
        """
        note = Note(title, content, tags)
        self.add_note(note)
        return note

    def remove_note(self, index: int) -> bool:
        """
        Видаляє нотатку за індексом
        
        Args:
            index (int): Індекс нотатки для видалення (починається з 1)
            
        Returns:
            bool: True, якщо нотатку було видалено, False - якщо індекс неправильний
        """
        if 1 <= index <= len(self._notes):
            del self._notes[index - 1]
            self.save_notes()
            return True
        return False

    def remove_note_by_title(self, title: str) -> bool:
        """
        Видаляє першу нотатку з вказаним заголовком
        
        Args:
            title (str): Заголовок нотатки для видалення
            
        Returns:
            bool: True, якщо нотатку було видалено, False - якщо не знайдено
        """
        for i, note in enumerate(self._notes):
            if note.title.lower() == title.lower():
                del self._notes[i]
                self.save_notes()
                return True
        return False

    def edit_note(self, index: int, title: Optional[str] = None, 
                  content: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Редагує нотатку за індексом
        
        Args:
            index (int): Індекс нотатки (починається з 1)
            title (Optional[str]): Новий заголовок (якщо не None)
            content (Optional[str]): Новий контент (якщо не None)
            tags (Optional[List[str]]): Нові теги (якщо не None)
            
        Returns:
            bool: True, якщо нотатка була відредагована успішно
        """
        note = self.get_note(index)
        if note is None:
            return False
        
        # Оновлюємо тільки ті поля, які передані
        if title is not None:
            note.title = title
        if content is not None:
            note.update_content(content)
        if tags is not None:
            note.tags = tags
        
        return self.save_notes()

    def get_note(self, index: int) -> Optional[Note]:
        """
        Повертає нотатку за індексом
        
        Args:
            index (int): Індекс нотатки (починається з 1)
            
        Returns:
            Optional[Note]: Нотатка або None, якщо індекс неправильний
        """
        if 1 <= index <= len(self._notes):
            return self._notes[index - 1]
        return None

    def get_note_by_index(self, index: int) -> Optional[Note]:
        """
        Повертає нотатку за індексом (псевдонім для get_note)
        
        Args:
            index (int): Індекс нотатки (починається з 1)
            
        Returns:
            Optional[Note]: Нотатка або None, якщо індекс неправильний
        """
        return self.get_note(index)

    def find_notes_by_title(self, title: str) -> List[tuple[int, Note]]:
        """
        Знаходить нотатки за заголовком (частковий збіг)
        
        Args:
            title (str): Заголовок для пошуку
            
        Returns:
            List[tuple[int, Note]]: Список кортежів (індекс, нотатка)
        """
        found_notes = []
        title_lower = title.lower()
        
        for i, note in enumerate(self._notes):
            if title_lower in note.title.lower():
                found_notes.append((i + 1, note))
        
        return found_notes

    def search_notes(self, query: str, case_sensitive: bool = False) -> List[tuple[int, Note]]:
        """
        Шукає нотатки за змістом, заголовком або тегами
        
        Args:
            query (str): Пошуковий запит
            case_sensitive (bool): Чи враховувати регістр
            
        Returns:
            List[tuple[int, Note]]: Список кортежів (індекс, нотатка)
        """
        found_notes = []
        
        for i, note in enumerate(self._notes):
            # Шукаємо в змісті та заголовку
            if note.search_in_content(query, case_sensitive):
                found_notes.append((i + 1, note))
                continue
            
            # Шукаємо в тегах
            query_check = query if case_sensitive else query.lower()
            for tag in note.tags:
                tag_check = tag if case_sensitive else tag.lower()
                if query_check in tag_check:
                    found_notes.append((i + 1, note))
                    break
        
        return found_notes

    def find_notes_by_tags(self, tags: List[str], match_all: bool = False) -> List[tuple[int, Note]]:
        """
        Знаходить нотатки за тегами
        
        Args:
            tags (List[str]): Список тегів для пошуку
            match_all (bool): Чи повинні збігатися всі теги (True) або хоча б один (False)
            
        Returns:
            List[tuple[int, Note]]: Список кортежів (індекс, нотатка)
        """
        found_notes = []
        
        if not tags:
            return found_notes
        
        # Нормалізуємо теги для пошуку
        normalized_tags = []
        for tag in tags:
            try:
                normalized_tag = tag.strip().lower()
                if normalized_tag:
                    normalized_tags.append(normalized_tag)
            except:
                continue
        
        if not normalized_tags:
            return found_notes
        
        for i, note in enumerate(self._notes):
            if match_all:
                # Всі теги повинні бути присутні
                if all(tag in note.tags for tag in normalized_tags):
                    found_notes.append((i + 1, note))
            else:
                # Хоча б один тег повинен бути присутній
                if note.matches_tags(normalized_tags):
                    found_notes.append((i + 1, note))
        
        return found_notes

    def get_notes_by_tags(self, tags: List[str], match_all: bool = False) -> List[tuple[int, Note]]:
        """
        Псевдонім для find_notes_by_tags() - для сумісності з тестами
        
        Args:
            tags (List[str]): Список тегів для пошуку
            match_all (bool): Чи повинні збігатися всі теги (True) або хоча б один (False)
            
        Returns:
            List[tuple[int, Note]]: Список кортежів (індекс, нотатка)
        """
        return self.find_notes_by_tags(tags, match_all)

    def get_all_notes(self, sort_by: str = 'created') -> List[tuple[int, Note]]:
        """
        Повертає всі нотатки, відсортовані за вказаним критерієм
        
        Args:
            sort_by (str): Критерій сортування ('created', 'updated', 'title', 'tags')
            
        Returns:
            List[tuple[int, Note]]: Список кортежів (оригінальний_індекс, нотатка)
        """
        indexed_notes = [(i + 1, note) for i, note in enumerate(self._notes)]
        
        if sort_by == 'created':
            indexed_notes.sort(key=lambda x: x[1].created_at, reverse=True)
        elif sort_by == 'updated':
            indexed_notes.sort(key=lambda x: x[1].updated_at, reverse=True)
        elif sort_by == 'title':
            indexed_notes.sort(key=lambda x: x[1].title.lower())
        elif sort_by == 'tags':
            indexed_notes.sort(key=lambda x: len(x[1].tags), reverse=True)
        
        return indexed_notes

    def get_all_tags(self) -> Set[str]:
        """
        Повертає всі унікальні теги з усіх нотаток
        
        Returns:
            Set[str]: Множина всіх тегів
        """
        all_tags = set()
        for note in self._notes:
            all_tags.update(note.tags)
        return all_tags

    def get_tag_statistics(self) -> Dict[str, int]:
        """
        Повертає статистику використання тегів
        
        Returns:
            Dict[str, int]: Словник {тег: кількість_використань}
        """
        tag_counts = {}
        for note in self._notes:
            for tag in note.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Сортуємо за кількістю використань
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True))

    def update_note(self, index: int, title: Optional[str] = None, 
                   content: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Note]:
        """
        Оновлює існуючу нотатку
        
        Args:
            index (int): Індекс нотатки для оновлення (починається з 1)
            title (Optional[str]): Новий заголовок
            content (Optional[str]): Новий зміст
            tags (Optional[List[str]]): Нові теги (замінюють всі існуючі)
            
        Returns:
            Optional[Note]: Оновлена нотатка або None, якщо індекс неправильний
            
        Raises:
            ValueError: Якщо дані не валідні
        """
        note = self.get_note(index)
        if not note:
            return None
        
        if title is not None:
            note.set_title(title)
        
        if content is not None:
            note.set_content(content)
        
        if tags is not None:
            note.clear_tags()
            for tag in tags:
                note.add_tag(tag)
        
        self.save_notes()
        return note

    def add_tag_to_note(self, index: int, tag: str) -> bool:
        """
        Додає тег до існуючої нотатки
        
        Args:
            index (int): Індекс нотатки (починається з 1)
            tag (str): Тег для додавання
            
        Returns:
            bool: True, якщо тег було додано успішно
            
        Raises:
            ValueError: Якщо тег не валідний або вже існує
        """
        note = self.get_note(index)
        if not note:
            return False
        
        note.add_tag(tag)
        self.save_notes()
        return True

    def remove_tag_from_note(self, index: int, tag: str) -> bool:
        """
        Видаляє тег з нотатки
        
        Args:
            index (int): Індекс нотатки (починається з 1)
            tag (str): Тег для видалення
            
        Returns:
            bool: True, якщо тег було видалено
        """
        note = self.get_note(index)
        if not note:
            return False
        
        if note.remove_tag(tag):
            self.save_notes()
            return True
        return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Повертає статистику по нотатках
        
        Returns:
            Dict[str, Any]: Словник зі статистикою
        """
        total_notes = len(self._notes)
        total_tags = len(self.get_all_tags())
        
        if total_notes > 0:
            total_words = sum(note.get_word_count() for note in self._notes)
            avg_words_per_note = total_words / total_notes
            notes_with_tags = sum(1 for note in self._notes if note.tags)
            avg_tags_per_note = sum(len(note.tags) for note in self._notes) / total_notes
        else:
            total_words = 0
            avg_words_per_note = 0
            notes_with_tags = 0
            avg_tags_per_note = 0
        
        return {
            'total_notes': total_notes,
            'total_tags': total_tags,
            'total_words': total_words,
            'avg_words_per_note': round(avg_words_per_note, 1),
            'notes_with_tags': notes_with_tags,
            'avg_tags_per_note': round(avg_tags_per_note, 1),
            'average_tags_per_note': round(avg_tags_per_note, 1)  # Альтернативне ім'я для тестів
        }

    def __len__(self) -> int:
        """Повертає кількість нотаток у колекції"""
        return len(self._notes)

    def __iter__(self):
        """Дозволяє ітерацію по нотатках"""
        return iter(self._notes)

    def __getitem__(self, index: int) -> Note:
        """Дозволяє доступ до нотаток за індексом (починається з 0)"""
        return self._notes[index]
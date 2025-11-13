"""
Модуль для збереження даних у файли
"""

import json
import os
from typing import Any, Dict
from pathlib import Path


class FileStorage:
    """
    Клас для збереження та завантаження даних у файли JSON
    
    Забезпечує персистентність даних між сесіями роботи з програмою.
    """

    def __init__(self, data_dir: str = "data"):
        """
        Ініціалізує файлове сховище
        
        Args:
            data_dir (str): Шлях до папки для збереження даних
        """
        self.data_dir = Path(data_dir)
        self.ensure_data_directory()

    def ensure_data_directory(self) -> None:
        """Створює папку для даних, якщо вона не існує"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Помилка створення папки для даних: {e}")
            # Використовуємо поточну папку як fallback
            self.data_dir = Path(".")

    def get_file_path(self, filename: str) -> Path:
        """
        Повертає повний шлях до файлу даних
        
        Args:
            filename (str): Ім'я файлу
            
        Returns:
            Path: Повний шлях до файлу
        """
        # Додаємо розширення .json, якщо його немає
        if not filename.endswith('.json'):
            filename += '.json'
        
        return self.data_dir / filename

    def save_data(self, filename: str, data: Any) -> bool:
        """
        Зберігає дані у файл JSON
        
        Args:
            filename (str): Ім'я файлу
            data (Any): Дані для збереження
            
        Returns:
            bool: True якщо збереження успішне, False інакше
        """
        file_path = self.get_file_path(filename)
        
        try:
            # Створюємо резервну копію, якщо файл існує
            if file_path.exists():
                backup_path = file_path.with_suffix('.json.backup')
                try:
                    file_path.replace(backup_path)
                except Exception:
                    pass  # Ігноруємо помилки створення резервної копії
            
            # Зберігаємо дані з красивим форматуванням
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            return True  # Успішне збереження
                
        except Exception as e:
            # Відновлюємо з резервної копії, якщо можливо
            backup_path = file_path.with_suffix('.json.backup')
            if backup_path.exists():
                try:
                    backup_path.replace(file_path)
                except Exception:
                    pass
            
            return False  # Помилка збереження

    def load_data(self, filename: str) -> Any:
        """
        Завантажує дані з файлу JSON
        
        Args:
            filename (str): Ім'я файлу
            
        Returns:
            Any: Завантажені дані
            
        Raises:
            FileNotFoundError: Якщо файл не існує
            Exception: Якщо не вдалося завантажити дані
        """
        file_path = self.get_file_path(filename)
        
        if not file_path.exists():
            return {}  # Повертаємо порожній словник для неіснуючих файлів
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        
        except json.JSONDecodeError as e:
            # Спробуємо відновити з резервної копії
            backup_path = file_path.with_suffix('.json.backup')
            if backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    # Відновлюємо основний файл з резервної копії
                    self.save_data(filename, data)
                    return data
                
                except Exception:
                    pass  # Резервна копія також пошкоджена
            
            raise Exception(f"Помилка парсингу JSON у файлі {filename}: {e}")
        
        except Exception as e:
            raise Exception(f"Помилка завантаження даних з файлу {filename}: {e}")

    def file_exists(self, filename: str) -> bool:
        """
        Перевіряє, чи існує файл
        
        Args:
            filename (str): Ім'я файлу
            
        Returns:
            bool: True, якщо файл існує
        """
        file_path = self.get_file_path(filename)
        return file_path.exists()

    def delete_file(self, filename: str) -> bool:
        """
        Видаляє файл даних
        
        Args:
            filename (str): Ім'я файлу
            
        Returns:
            bool: True, якщо файл було видалено успішно
        """
        file_path = self.get_file_path(filename)
        
        try:
            if file_path.exists():
                file_path.unlink()
                
                # Видаляємо також резервну копію, якщо вона є
                backup_path = file_path.with_suffix('.json.backup')
                if backup_path.exists():
                    backup_path.unlink()
                
                return True
            return False
        
        except Exception as e:
            print(f"Помилка видалення файлу {filename}: {e}")
            return False

    def get_file_size(self, filename: str) -> int:
        """
        Повертає розмір файлу в байтах
        
        Args:
            filename (str): Ім'я файлу
            
        Returns:
            int: Розмір файлу в байтах, або 0 якщо файл не існує
        """
        file_path = self.get_file_path(filename)
        
        try:
            if file_path.exists():
                return file_path.stat().st_size
            return 0
        except Exception:
            return 0

    def list_data_files(self) -> list[str]:
        """
        Повертає список всіх файлів даних
        
        Returns:
            list[str]: Список імен файлів без розширення .json
        """
        try:
            json_files = []
            for file_path in self.data_dir.glob("*.json"):
                if not file_path.name.endswith('.backup'):
                    # Зберігаємо повне ім'я з розширенням .json
                    filename = file_path.name
                    json_files.append(filename)
            
            return sorted(json_files)
        
        except Exception:
            return []

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Повертає інформацію про сховище
        
        Returns:
            Dict[str, Any]: Інформація про сховище
        """
        try:
            files = self.list_data_files()
            total_size = sum(self.get_file_size(f) for f in files)
            
            return {
                'data_directory': str(self.data_dir.absolute()),
                'total_files': len(files),
                'files': files,
                'total_size_bytes': total_size,
                'total_size_kb': round(total_size / 1024, 2)
            }
        
        except Exception as e:
            return {
                'error': f"Помилка отримання інформації про сховище: {e}",
                'data_directory': str(self.data_dir.absolute()),
                'total_files': 0,
                'files': [],
                'total_size_bytes': 0,
                'total_size_kb': 0
            }

    def clear_all_data(self) -> bool:
        """
        Видаляє всі файли даних
        
        Returns:
            bool: True, якщо всі файли було видалено успішно
        """
        try:
            files_deleted = 0
            files = self.list_data_files()
            
            for filename in files:
                if self.delete_file(filename):
                    files_deleted += 1
            
            return files_deleted == len(files)
        
        except Exception as e:
            print(f"Помилка очищення всіх даних: {e}")
            return False

    def create_backup(self, filename: str) -> str:
        """
        Створює резервну копію файлу
        
        Args:
            filename (str): Ім'я файлу для резервного копіювання
            
        Returns:
            str: Шлях до створеного backup файлу
        """
        import datetime
        
        # Завантажуємо дані з оригінального файлу
        try:
            data = self.load_data(filename)
        except Exception:
            return ""
        
        # Створюємо унікальне ім'я backup файлу з timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{filename}_backup_{timestamp}.json"
        backup_path = self.data_dir / backup_filename
        
        # Зберігаємо backup
        try:
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return str(backup_path)
        except Exception:
            return ""

    def restore_backup(self, filename: str, backup_file: str) -> bool:
        """
        Відновлює файл з резервної копії
        
        Args:
            filename (str): Ім'я файлу для відновлення
            backup_file (str): Шлях до backup файлу
            
        Returns:
            bool: True якщо відновлення успішне
        """
        try:
            # Завантажуємо дані з backup
            with open(backup_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Зберігаємо в оригінальний файл
            return self.save_data(filename, data)
        except Exception:
            return False

    def list_backups(self, filename: str) -> list:
        """
        Повертає список backup файлів для заданого файлу
        
        Args:
            filename (str): Ім'я файлу для пошуку backup
            
        Returns:
            list: Список шляхів до backup файлів
        """
        try:
            backup_pattern = f"{filename}_backup_*.json"
            backup_files = []
            
            # Шукаємо файли що відповідають паттерну
            for file_path in self.data_dir.glob(backup_pattern):
                if file_path.is_file():
                    backup_files.append(str(file_path))
            
            return sorted(backup_files, reverse=True)  # Новіші backup першими
        except Exception:
            return []

    def __str__(self) -> str:
        """Повертає рядкове представлення сховища"""
        info = self.get_storage_info()
        return f"FileStorage(directory='{info['data_directory']}', files={info['total_files']})"

    def __repr__(self) -> str:
        """Повертає технічне представлення сховища"""
        return f"FileStorage(data_dir='{self.data_dir}')"
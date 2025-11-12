import re
from datetime import datetime
from typing import Optional


class Field:
    """Базовий клас для всіх полів з базовою валідацією"""
    
    def __init__(self, value: str):
        """
        Ініціалізує поле з валідацією
        
        Args:
            value (str): Значення поля
            
        Raises:
            ValueError: Якщо значення не пройшло валідацію
        """
        self.value = self.validate(value)

    def validate(self, value: str) -> str:
        """
        Базова валідація - перевіряє, що значення не порожнє
        
        Args:
            value (str): Значення для валідації
            
        Returns:
            str: Валідоване значення
            
        Raises:
            ValueError: Якщо значення порожнє
        """
        if not value or not value.strip():
            raise ValueError("Поле не може бути порожнім")
        return value.strip()

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.value}')"


class Name(Field):
    """Клас для валідації імен"""
    
    def validate(self, value: str) -> str:
        """
        Валідація імені - має містити тільки літери та пробіли
        
        Args:
            value (str): Ім'я для валідації
            
        Returns:
            str: Валідоване ім'я
            
        Raises:
            ValueError: Якщо ім'я містить недопустимі символи
        """
        value = super().validate(value)
        
        # Перевіряємо, що ім'я містить тільки літери, пробіли, дефіси та апострофи
        if not re.match(r"^[a-zA-Zа-яА-ЯіІїЇєЄ'\s\-]+$", value):
            raise ValueError("Ім'я може містити тільки літери, пробіли, дефіси та апострофи")
        
        return value.title()  # Приводимо до формату Title Case

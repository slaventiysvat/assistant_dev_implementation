#!/usr/bin/env python3
"""
Entry point для personal_assistant пакету
"""

def main():
    """Головна функція для запуску через pip entry point"""
    import sys
    import os
    
    # Додаємо поточну директорію пакету до Python path
    package_dir = os.path.dirname(os.path.abspath(__file__))
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    try:
        # Імпортуємо і запускаємо головну функцію
        from .main import main as main_func
        main_func()
    except (ImportError, ValueError):
        # Fallback для випадку коли відносні імпорти не працюють
        try:
            from main import main as main_func
            main_func()
        except ImportError:
            print("❌ Помилка: Не можу знайти модуль main")
            print("Спробуйте запустити: python -m personal_assistant")
            sys.exit(1)

if __name__ == "__main__":
    main()
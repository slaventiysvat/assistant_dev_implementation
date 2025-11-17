#!/usr/bin/env python3
"""
Entry point для console script
"""

def main():
    """Головна функція для console script entry point"""
    try:
        from personal_assistant.__main__ import main as pkg_main
        pkg_main()
    except ImportError:
        # Fallback якщо пакет не знайдено
        import sys
        import os
        
        # Спробуємо знайти пакет в різних місцях
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'personal_assistant'),
            os.path.dirname(__file__)
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'main.py')):
                sys.path.insert(0, path)
                try:
                    from main import main as main_func
                    main_func()
                    return
                except ImportError:
                    continue
        
        print("❌ Помилка: Не можу знайти модулі personal_assistant")
        print("Спробуйте: python -m personal_assistant")
        sys.exit(1)

if __name__ == "__main__":
    main()
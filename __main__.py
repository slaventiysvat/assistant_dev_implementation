#!/usr/bin/env python3
"""
Точка входу для запуску пакету через python -m personal_assistant
або через команду personal-assistant
"""

import sys
import os

# Додаємо поточну директорію до Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Головна функція для entry point"""
    try:
        from main import main as main_func
        main_func()
    except ImportError:
        # Якщо не можемо імпортувати, спробуємо знайти main.py
        import subprocess
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_py = os.path.join(script_dir, 'main.py')
        if os.path.exists(main_py):
            subprocess.run([sys.executable, main_py] + sys.argv[1:])
        else:
            print("❌ Не можу знайти main.py файл")
            sys.exit(1)

if __name__ == "__main__":
    main()
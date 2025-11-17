#!/usr/bin/env python3
"""
Простий запуск Personal Assistant
"""

import sys
import os
import subprocess

def run_assistant():
    """Запускає персональний помічник різними способами"""
    
    # Спробуємо знайти main.py відносно цього файлу
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(script_dir, 'main.py')
    
    if os.path.exists(main_py):
        # Якщо знайшли main.py, запускаємо його
        try:
            subprocess.run([sys.executable, main_py] + sys.argv[1:])
        except KeyboardInterrupt:
            print("\n\n👋 Дякуємо за використання програми!")
        except Exception as e:
            print(f"\n❌ Помилка запуску: {e}")
    else:
        # Якщо main.py не знайдено, спробуємо імпорт
        try:
            sys.path.insert(0, script_dir)
            from main import main
            main()
        except ImportError as e:
            print(f"❌ Не можу знайти модулі: {e}")
            print("Спробуйте запустити: python main.py")
        except Exception as e:
            print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    run_assistant()
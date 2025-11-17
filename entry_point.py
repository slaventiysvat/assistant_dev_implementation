#!/usr/bin/env python3
"""
Entry point для встановлення через pip
"""

def main():
    """Головна функція для запуску через pip entry point"""
    import sys
    import os
    
    # Знаходимо директорію пакету
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Додаємо до Python path
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    try:
        # Спробуємо імпортувати main
        from main import main as main_func
        main_func()
    except ImportError:
        # Якщо не вдалося, спробуємо знайти main.py
        main_py = os.path.join(package_dir, 'main.py')
        if os.path.exists(main_py):
            import subprocess
            subprocess.run([sys.executable, main_py] + sys.argv[1:])
        else:
            print("❌ Не можу знайти main.py. Спробуйте запустити: python main.py")
            sys.exit(1)

if __name__ == "__main__":
    main()
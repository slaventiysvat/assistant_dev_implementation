#!/bin/bash
# Запуск персонального помічника для Linux/macOS

echo "======================================"
echo "   ПЕРСОНАЛЬНИЙ ПОМІЧНИК"
echo "======================================"
echo

# Перевірка чи встановлений Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ПОМИЛКА: Python не знайдено!"
    echo "Встановіть Python з вашого менеджера пакетів або з https://python.org"
    exit 1
fi

# Використовуємо python3 якщо доступний, інакше python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Переходимо до директорії скрипта
cd "$(dirname "$0")"

# Активуємо віртуальне оточення якщо існує
if [ -f "../.venv/bin/activate" ]; then
    echo "Активація віртуального оточення..."
    source "../.venv/bin/activate"
fi

# Запускаємо програму з переданими аргументами
case "$1" in
    "demo")
        echo "Запуск демонстраційного режиму..."
        $PYTHON_CMD main.py --demo
        ;;
    "test")
        echo "Запуск тестового режиму..."
        $PYTHON_CMD main.py --test
        ;;
    "help")
        $PYTHON_CMD main.py --help-full
        ;;
    *)
        echo "Запуск інтерактивного режиму..."
        echo "Введіть 'help' для довідки або Ctrl+C для виходу"
        echo
        $PYTHON_CMD main.py
        ;;
esac
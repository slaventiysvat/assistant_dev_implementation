@echo off
rem Запуск персонального помічника для Windows

echo ======================================
echo   ПЕРСОНАЛЬНИЙ ПОМІЧНИК
echo ======================================
echo.

rem Перевірка чи встановлений Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ПОМИЛКА: Python не знайдено!
    echo Завантажте та встановіть Python з https://python.org
    pause
    exit /b 1
)

rem Переходимо до директорії скрипта
cd /d "%~dp0"

rem Активуємо віртуальне оточення якщо існує
if exist "..\\.venv\\Scripts\\activate.bat" (
    echo Активація віртуального оточення...
    call "..\\.venv\\Scripts\\activate.bat"
)

rem Запускаємо програму з переданими аргументами
if "%1"=="demo" (
    echo Запуск демонстраційного режиму...
    python main.py --demo
) else if "%1"=="test" (
    echo Запуск тестового режиму...
    python main.py --test
) else if "%1"=="help" (
    python main.py --help-full
) else (
    echo Запуск інтерактивного режиму...
    echo Введіть 'help' для довідки або Ctrl+C для виходу
    echo.
    python main.py
)

pause
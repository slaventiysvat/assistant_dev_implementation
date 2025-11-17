#!/usr/bin/env python3
"""
Тест установки та запуску пакету personal-assistant
"""

import subprocess
import sys
import os

def test_installation():
    """Тестує чи пакет встановлено правильно"""
    print("🧪 Тестування установки personal-assistant...")
    
    tests = [
        ("personal-assistant --help", "Тест консольної команди"),
        ("python -m personal_assistant --help", "Тест Python модуля"),
    ]
    
    results = []
    
    for cmd, desc in tests:
        print(f"\n📋 {desc}: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {desc} - УСПІШНО")
                results.append(True)
            else:
                print(f"❌ {desc} - ПОМИЛКА")
                print(f"Error: {result.stderr}")
                results.append(False)
        except subprocess.TimeoutExpired:
            print(f"⏰ {desc} - TIMEOUT")
            results.append(False)
        except Exception as e:
            print(f"❌ {desc} - ВИНЯТОК: {e}")
            results.append(False)
    
    print(f"\n📊 РЕЗУЛЬТАТИ: {sum(results)}/{len(results)} тестів пройдено")
    
    if all(results):
        print("🎉 Всі тести пройшли успішно! Пакет готовий до використання.")
    else:
        print("⚠️  Деякі тести не пройшли. Перевірте установку.")
    
    return all(results)

if __name__ == "__main__":
    test_installation()
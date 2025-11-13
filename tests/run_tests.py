"""
Головний файл для запуску всіх тестів dev_implementation
"""
import unittest
import sys
from pathlib import Path

# Додаємо dev_implementation до шляху
dev_path = Path(__file__).parent.parent
sys.path.insert(0, str(dev_path))

# Імпортуємо всі тестові класи
from test_models import TestFields, TestContact, TestNote
from test_managers import TestContactManager, TestNoteManager
from test_utils import TestCommandMatcher, TestValidators
from test_cli import TestPersonalAssistantCLI, TestCLIIntegration
from test_storage import TestFileStorage


def create_test_suite():
    """Створює набір всіх тестів"""
    suite = unittest.TestSuite()
    
    # Додаємо тести для моделей
    suite.addTest(unittest.makeSuite(TestFields))
    suite.addTest(unittest.makeSuite(TestContact))
    suite.addTest(unittest.makeSuite(TestNote))
    
    # Додаємо тести для менеджерів
    suite.addTest(unittest.makeSuite(TestContactManager))
    suite.addTest(unittest.makeSuite(TestNoteManager))
    
    # Додаємо тести для утиліт
    suite.addTest(unittest.makeSuite(TestCommandMatcher))
    suite.addTest(unittest.makeSuite(TestValidators))
    
    # Додаємо тести для CLI
    suite.addTest(unittest.makeSuite(TestPersonalAssistantCLI))
    suite.addTest(unittest.makeSuite(TestCLIIntegration))
    
    # Додаємо тести для сховища
    suite.addTest(unittest.makeSuite(TestFileStorage))
    
    return suite


def run_all_tests(verbosity=2):
    """Запускає всі тести з детальним виводом"""
    print("🧪 ЗАПУСК ТЕСТІВ DEV_IMPLEMENTATION")
    print("=" * 60)
    
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Невдалі: {failures}")
    print(f"💥 Помилки: {errors}")
    print(f"📈 Загальний прогрес: {passed}/{total_tests} ({passed/total_tests*100:.1f}%)" if total_tests > 0 else "")
    
    if failures > 0:
        print(f"\n❌ НЕВДАЛІ ТЕСТИ:")
        for test, traceback in result.failures:
            print(f"  • {test}: {traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else 'Невідома помилка'}")
    
    if errors > 0:
        print(f"\n💥 ПОМИЛКИ:")
        for test, traceback in result.errors:
            error_msg = traceback.split('\n')[-2] if traceback.split('\n') else 'Невідома помилка'
            print(f"  • {test}: {error_msg}")
    
    if failures == 0 and errors == 0:
        print(f"\n🎉 ВСІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
    else:
        print(f"\n🔧 Є проблеми що потребують вирішення.")
    
    return result


def run_specific_module(module_name, verbosity=2):
    """Запускає тести для конкретного модуля"""
    module_map = {
        'models': [TestFields, TestContact, TestNote],
        'managers': [TestContactManager, TestNoteManager],
        'utils': [TestCommandMatcher, TestValidators],
        'cli': [TestPersonalAssistantCLI, TestCLIIntegration],
        'storage': [TestFileStorage]
    }
    
    if module_name not in module_map:
        print(f"❌ Невідомий модуль: {module_name}")
        print(f"Доступні модулі: {', '.join(module_map.keys())}")
        return None
    
    print(f"🧪 ЗАПУСК ТЕСТІВ ДЛЯ МОДУЛЯ: {module_name.upper()}")
    print("=" * 60)
    
    suite = unittest.TestSuite()
    for test_class in module_map[module_name]:
        suite.addTest(unittest.makeSuite(test_class))
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Запуск тестів для dev_implementation')
    parser.add_argument('--module', '-m', help='Запустити тести для конкретного модуля (models, managers, utils, cli, storage)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Детальний вивід')
    
    args = parser.parse_args()
    
    verbosity = 2 if args.verbose else 1
    
    if args.module:
        run_specific_module(args.module, verbosity)
    else:
        run_all_tests(verbosity)
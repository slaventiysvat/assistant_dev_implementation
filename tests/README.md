# Тести для dev_implementation

Цей каталог містить комплексні тести для всіх компонентів персонального помічника в dev_implementation.

## Структура тестів

```
tests/
├── __init__.py                 # Ініціалізація пакету тестів
├── test_models.py             # Тести для моделей (Contact, Note, Fields)
├── test_managers.py           # Тести для менеджерів (ContactManager, NoteManager)  
├── test_utils.py              # Тести для утиліт (CommandMatcher, validators)
├── test_cli.py                # Тести для CLI інтерфейсу
├── test_storage.py            # Тести для файлового сховища
├── run_tests.py               # Головний скрипт для запуску тестів
├── pytest.ini                # Конфігурація для pytest
└── README.md                  # Цей файл
```

## Запуск тестів

### Використовуючи власний скрипт (рекомендовано)

1. **Запустити всі тести:**
```bash
cd dev_implementation/tests
python run_tests.py
```

2. **Запустити тести для конкретного модуля:**
```bash
python run_tests.py --module models     # Тести моделей
python run_tests.py --module managers   # Тести менеджерів
python run_tests.py --module utils      # Тести утиліт
python run_tests.py --module cli        # Тести CLI
python run_tests.py --module storage    # Тести сховища
```

3. **Детальний вивід:**
```bash
python run_tests.py --verbose
python run_tests.py -m models -v
```

### Використовуючи unittest

1. **Запустити всі тести:**
```bash
cd dev_implementation
python -m unittest discover tests
```

2. **Запустити конкретний файл тестів:**
```bash
python -m unittest tests.test_models
python -m unittest tests.test_managers
python -m unittest tests.test_cli
```

3. **Запустити конкретний тестовий клас:**
```bash
python -m unittest tests.test_models.TestContact
python -m unittest tests.test_cli.TestPersonalAssistantCLI
```

4. **Запустити конкретний тест:**
```bash
python -m unittest tests.test_models.TestContact.test_add_phone
```

### Використовуючи pytest (якщо встановлено)

```bash
cd dev_implementation
pip install pytest                    # Встановити pytest якщо потрібно
pytest tests/                        # Запустити всі тести
pytest tests/test_models.py         # Запустити конкретний файл
pytest -v                           # Детальний вивід
pytest -k "test_contact"            # Запустити тести що містять "test_contact"
```

## Опис тестів

### test_models.py
- **TestFields**: Тести для полів моделей (Name, Phone, Email, Birthday, Address)
- **TestContact**: Тести для класу Contact (створення, додавання телефонів/emails, дні народження)
- **TestNote**: Тести для класу Note (створення, робота з тегами, редагування)

### test_managers.py
- **TestContactManager**: Тести для управління контактами (додавання, пошук, видалення)
- **TestNoteManager**: Тести для управління нотатками (створення, пошук за текстом/тегами)

### test_utils.py
- **TestCommandMatcher**: Тести для розпізнавання команд користувача
- **TestValidators**: Тести для валідації даних (числа, теги, так/ні відповіді)

### test_cli.py
- **TestPersonalAssistantCLI**: Тести для основної функціональності CLI
- **TestCLIIntegration**: Інтеграційні тести для повних циклів роботи

### test_storage.py
- **TestFileStorage**: Тести для збереження/завантаження даних з файлів

## Тестове покриття

Тести покривають:
- ✅ Створення та валідація всіх моделей
- ✅ CRUD операції для контактів та нотаток  
- ✅ Пошук та фільтрація даних
- ✅ Розпізнавання команд користувача
- ✅ Валідація вхідних даних
- ✅ CLI інтерфейс та обробка команд
- ✅ Збереження/завантаження даних
- ✅ Обробка помилок та крайових випадків
- ✅ Інтеграційні сценарії

## Додавання нових тестів

1. **Для нової функціональності моделей** - додайте до `test_models.py`
2. **Для нових методів менеджерів** - додайте до `test_managers.py`  
3. **Для нових команд CLI** - додайте до `test_cli.py`
4. **Для нових утиліт** - додайте до `test_utils.py`

### Приклад нового тесту:

```python
def test_new_functionality(self):
    """Тест нової функціональності"""
    # Arrange (налаштування)
    test_data = "test_input"
    
    # Act (дія)
    result = some_function(test_data)
    
    # Assert (перевірка)
    self.assertEqual(result, expected_value)
    self.assertIsNotNone(result)
```

## Continuous Integration

Ці тести можна легко інтегрувати в CI/CD pipeline:

```yaml
# Приклад для GitHub Actions
- name: Run tests
  run: |
    cd dev_implementation/tests
    python run_tests.py
```

## Переваги цих тестів

1. **Незалежність від еталону** - тести перевіряють функціональність безпосередньо
2. **Швидкість** - не потребують порівняння з reference implementation
3. **Стабільність** - фіксують поведінку коду для запобігання регресіям
4. **Покриття** - тестують як окремі компоненти, так і їх інтеграцію
5. **Зручність** - прості команди для запуску різних наборів тестів
6. **Масштабованість** - легко додавати нові тести при розширенні функціональності
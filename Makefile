# Makefile для Personal Assistant

.PHONY: help install install-dev test clean build upload run demo

# Показати доступні команди
help:
	@echo "Доступні команди:"
	@echo "  install      - Встановити пакет"
	@echo "  install-dev  - Встановити з залежностями для розробки"
	@echo "  test         - Запустити тести"
	@echo "  clean        - Очистити файли збірки"
	@echo "  build        - Зібрати пакет"
	@echo "  run          - Запустити програму"
	@echo "  demo         - Запустити демонстраційний режим"
	@echo "  format       - Форматувати код"

# Встановити пакет
install:
	pip install -e .

# Встановити з залежностями для розробки  
install-dev:
	pip install -e .[dev]
	pip install -r requirements-dev.txt

# Запустити тести
test:
	python -m pytest tests/ -v

# Очистити файли збірки
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Зібрати пакет
build: clean
	python setup.py sdist bdist_wheel

# Запустити програму
run:
	python main.py

# Запустити демонстраційний режим
demo:
	python main.py --demo

# Форматувати код
format:
	black . --line-length 88
	flake8 . --max-line-length 88

# Перевірити типи
typecheck:
	mypy .
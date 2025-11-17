#!/usr/bin/env python3
"""
Файл встановлення для Personal Assistant
"""

from setuptools import setup, find_packages
import os

# Читаємо README для опису
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Personal Assistant - система управління контактами та нотатками"

# Читаємо версію з __init__.py
def get_version():
    try:
        with open(os.path.join(os.path.dirname(__file__), "__init__.py"), "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except:
        return "1.0.0"

setup(
    name="personal-assistant",
    version=get_version(),
    author="Student",
    author_email="student@example.com",
    description="Personal Assistant для управління контактами та нотатками",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/slaventiysvat/assistant_dev_implementation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Groupware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Основні залежності відсутні - використовуємо тільки стандартну бібліотеку
    ],
    extras_require={
        "colors": ["colorama>=0.4.4"],  # Опціональна залежність для кольорів
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "personal-assistant=personal_assistant.entry_point:main",
        ],
    },
    include_package_data=True,
    package_data={
        "personal_assistant": ["*.json", "*.md", "*.txt", "data/*.json"],
        "": ["*.json", "*.md", "*.txt"],
    },
    zip_safe=False,
    keywords="personal assistant, contacts, notes, cli, birthday tracker",
    project_urls={
        "Bug Reports": "https://github.com/slaventiysvat/assistant_dev_implementation/issues",
        "Source": "https://github.com/slaventiysvat/assistant_dev_implementation",
        "Documentation": "https://github.com/slaventiysvat/assistant_dev_implementation/blob/main/README.md",
    },
)
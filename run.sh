#!/bin/bash

# Проверка наличия виртуального окружения
if [ ! -d ".venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv .venv
fi

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск основного скрипта
python main.py
@echo off

:: Проверка наличия виртуального окружения
if not exist ".venv" (
    echo Создание виртуального окружения...
    python -m venv .venv
)

:: Активация виртуального окружения
call .venv\Scripts\activate

:: Установка зависимостей
pip install -r requirements.txt

:: Запуск основного скрипта
python main.py

pause
@MZOO

call %~dp0venv\scripts\activate

cd %~dp0bot_zoo

set TELEGRAM_TOKEN = 6774150015:AAHFapzDPlNLNxI2JVJQyFU_0zjOv9WAKqw

python start_bot_zoo.py

pause
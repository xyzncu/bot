# INSTALLASI SCRIPT BOT

apt update
python -m pip install --upgrade pip
pip install python-telegram-bot
pip install pyTelegramBotAPI
python -c "import telebot"
pip install python-telegram-bot==13.0.0
npm install pm2 -g
pm2 start f.py --interpreter=python3 --name my_python_bot

import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен бота
MONGO_URI = os.getenv("MONGO_URI")  # Подключение к MongoDB
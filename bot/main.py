from aiogram import Bot, Dispatcher
import asyncio
import logging

from config import BOT_TOKEN
from handlers import router  # Подключаем обработчики команд

# Включаем логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем роутеры
dp.include_router(router)

async def start():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
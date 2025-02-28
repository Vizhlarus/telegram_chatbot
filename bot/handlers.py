from aiogram import Router, types
from aiogram.filters import CommandStart
from database.db import save_user, save_message

router = Router()  # Роутер для обработки команд

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n\n"
        "Я чат-бот, который анализирует статистику, карму, викторины и анекдоты. 🎉\n\n"
        "Доступные команды:\n"
        "/stats — статистика чата 📊\n"
        "/topkarma — топ пользователей по карме 🏆\n"
        "/quiz — начать викторину 🎓\n"
        "/anecdote — случайный анекдот 😂\n"
        "/talk — поговорить с ботом 💬\n"
    )

@router.message()
async def handle_message(message: types.Message):
    # Сохраняем пользователя (если он новый)
    await save_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    # Сохраняем сообщение в базу
    await save_message(
        user_id=message.from_user.id,
        text=message.text
    )
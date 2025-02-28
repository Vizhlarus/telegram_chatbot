from aiogram import Router, types
from aiogram.filters import CommandStart
from database.db import save_user, save_message, users_collection, messages_collection

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

    @router.message(commands=["stats"])
    async def stats_command(message: types.Message):
        chat_id = message.chat.id

        # Считаем общее количество сообщений
        total_messages = await messages_collection.count_documents({})

        # Топ-5 болтунов (самые активные)
        top_chatters = users_collection.find().sort("messages_count", -1).limit(5)
        top_chatters_list = [
            f"🥇 {user['full_name']} (@{user['username']}) — {user['messages_count']} сообщений"
            async for user in top_chatters
        ]

        # Топ-5 молчунов (самые неактивные)
        top_silent = users_collection.find().sort("messages_count", 1).limit(5)
        top_silent_list = [
            f"🔇 {user['full_name']} (@{user['username']}) — {user['messages_count']} сообщений"
            async for user in top_silent
        ]

        # Отправляем сообщение в чат
        stats_message = (
                f"📊 **Статистика чата**:\n\n"
                f"📩 Всего сообщений: {total_messages}\n\n"
                f"💬 **Топ-5 активных**:\n" + "\n".join(top_chatters_list) + "\n\n"
                                                                            f"😶 **Топ-5 молчунов**:\n" + "\n".join(
            top_silent_list)
        )

        await message.answer(stats_message, parse_mode="Markdown")
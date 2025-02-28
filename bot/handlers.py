from aiogram import Router, types
from aiogram.filters import Command
from database.db import users_collection, messages_collection  # ✅ Исправленный импорт

router = Router()  # Роутер для обработки команд

@router.message(Command("stats"))  # ✅ Правильный способ в aiogram 3.x
async def stats_command(message: types.Message):
    # Считаем общее количество сообщений
    total_messages = await messages_collection.count_documents({})

    # Топ-5 активных пользователей (болтуны)
    top_chatters_cursor = users_collection.find().sort("messages_count", -1).limit(5)
    top_chatters_list = [
        f"🥇 {user['full_name']} (@{user['username']}) — {user['messages_count']} сообщений"
        async for user in top_chatters_cursor
    ]

    # Топ-5 молчунов (неактивные)
    top_silent_cursor = users_collection.find().sort("messages_count", 1).limit(5)
    top_silent_list = [
        f"🔇 {user['full_name']} (@{user['username']}) — {user['messages_count']} сообщений"
        async for user in top_silent_cursor
    ]

    # Отправляем сообщение в чат
    stats_message = (
        f"📊 **Статистика чата**:\n\n"
        f"📩 Всего сообщений: {total_messages}\n\n"
        f"💬 **Топ-5 активных**:\n" + "\n".join(top_chatters_list) + "\n\n"
        f"😶 **Топ-5 молчунов**:\n" + "\n".join(top_silent_list)
    )

    await message.answer(stats_message, parse_mode="Markdown")
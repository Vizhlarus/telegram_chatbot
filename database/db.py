from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import MONGO_URI  # ✅ Исправленный импорт

# Подключение к MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client["telegram_chatbot"]

# Коллекции
users_collection = db["users"]
messages_collection = db["messages"]

# Функция сохранения пользователя
async def save_user(user_id: int, username: str, full_name: str):
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        await users_collection.insert_one({
            "_id": user_id,
            "username": username,
            "full_name": full_name,
            "messages_count": 0,
            "karma": 0
        })

# Функция сохранения сообщения
async def save_message(user_id: int, text: str):
    await messages_collection.insert_one({
        "user_id": user_id,
        "text": text
    })
    await users_collection.update_one(
        {"_id": user_id},
        {"$inc": {"messages_count": 1}}
    )
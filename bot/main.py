from aiogram import Bot, Dispatcher

bot = Bot(token="7647488175:AAFHUN78pCxzXRw5dDnfnpdEmz9EeDrzI8E")
dp = Dispatcher()

async def start():
    print("Бот запущен!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(start())
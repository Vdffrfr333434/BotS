import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI

# Получаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка наличия токенов
if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Переменные окружения BOT_TOKEN и OPENAI_API_KEY должны быть установлены")

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот с подключенной нейросетью. Отправь свой запрос.", parse_mode="HTML")

# Обработчик всех текстовых сообщений
@dp.message(lambda message: message.text)
async def handle_message(message: Message):
    client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key=OPENAI_API_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )
    reply = completion.choices[0].message.content
    await message.answer(reply, parse_mode="Markdown")

# Основной запуск бота
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

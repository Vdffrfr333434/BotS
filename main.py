import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from openai import OpenAI

# Настройки
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ← это Render-ссылка вида https://твой-сервис.onrender.com

if not TOKEN or not OPENAI_KEY or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN, OPENAI_API_KEY и WEBHOOK_URL должны быть заданы в переменных окружения")

# Логирование
logging.basicConfig(level=logging.INFO)

# Объекты
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

client = OpenAI(
    base_url="https://api.langdock.com/openai/eu/v1",
    api_key=OPENAI_KEY,
)

# Обработчик старт-команды
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне любой запрос, и я отвечу от имени ChatGPT")

# Обработчик любого текста
@dp.message()
async def handle_message(message: types.Message):
    response = client.chat.completions.create(
        model="gpt-4o",  # используем поддерживаемую модель
        messages=[{"role": "user", "content": message.text}]
    )
    await message.answer(response.choices[0].message.content)

# Запуск сервера
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

def create_app():
    app = web.Application()
    dp.startup.register(on_startup)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/")
    setup_application(app, dp)
    return app

app = create_app()

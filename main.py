sk-W9py-83L4rXN4cWS7Y_nEKfQ6SCncKhFY12w7HNfJlGRoX9M2-roqF8fnQH5KzmEWVueN12ZUOZVLQdDah1HbQ



import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI


TOKEN = '7989376133:AAGhQL1YFcdeXcJozCaDFYoxX-Q7KJIHKzQ' # ⁡⁢⁡⁢⁣⁣ПОМЕНЯЙТЕ ТОКЕН БОТА НА ВАШ⁡

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()


# ⁡⁢⁣⁡⁢⁣⁣ОБРАБОТЧИК КОМАНДЫ СТАРТ⁡⁡
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот с подключенной нейросетью, отправь свой запрос', parse_mode = 'HTML')


# ⁡⁢⁣⁣ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ⁡
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    client = OpenAI(
    base_url = "https://api.langdock.com/openai/eu/v1",
    api_key = "sk-W9py-83L4rXN4cWS7Y_nEKfQ6SCncKhFY12w7HNfJlGRoX9M2-roqF8fnQH5KzmEWVueN12ZUOZVLQdDah1HbQ" # ⁡⁢⁣⁣ПОМЕНЯЙТЕ ТОКЕН ИИ НА ВАШ⁡
    )

    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": message.text}
    ]
    )
    text = completion.choices[0].message.content

    await message.answer(text, parse_mode = "Markdown")


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

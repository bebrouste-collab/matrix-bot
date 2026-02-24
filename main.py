import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from openai import OpenAI

# Включаем логирование, чтобы видеть ошибки в Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ПОЛУЧЕНИЕ КЛЮЧЕЙ ---
# Вытаскиваем их из системы Railway
TOKEN = os.getenv('TELEGRAM_TOKEN')
AI_KEY = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')

# Проверка: если ключей нет, бот сразу скажет об этом в логах
if not TOKEN:
    logger.error("❌ ОШИБКА: Переменная TELEGRAM_TOKEN пуста!")
if not AI_KEY:
    logger.error("❌ ОШИБКА: Переменная OPENROUTER_API_KEY пуста!")

# Инициализация ИИ
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_KEY,
)

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("📟 **[SYSTEM]: Связь установлена.** Бот готов к работе!")

@router.message()
async def handle_message(message: types.Message):
    # Простейшая логика для теста
    await message.answer(f"Запрос получен: {message.text}. Обрабатываю...")

async def main():
    dp.include_router(router)
    logger.info("🚀 Бот запускается...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

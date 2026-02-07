import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from openai import OpenAI

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ГИБКОЕ ПОЛУЧЕНИЕ ТОКЕНОВ ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# Пробуем оба варианта имени ключа для надежности
AI_KEY = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN не найден в переменных Railway!")
if not AI_KEY:
    logger.error("❌ API-ключ ИИ (OPENROUTER_API_KEY/OPENAI_API_KEY) не найден!")

# Инициализация ИИ
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_KEY,
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

# Математика "Кода Судьбы"
def get_core_code(date_str):
    digits = [int(d) for d in date_str if d.isdigit()]
    if not digits: return None
    res = sum(digits)
    while res > 9:
        res = sum(int(d) for d in str(res))
    return res

# Запрос к нейросети
async def get_ai_interpretation(prompt):
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {"role": "system", "content": "Ты — Matrix Debugger. Анализируй жизнь как код. Стиль: киберпанк, ирония."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка ИИ: {e}")
        return "⚠️ Системный сбой: ИИ временно недоступен. Проверь баланс или ключи."

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("📟 **[SYSTEM]: Связь установлена.**\nВведи дату рождения (ДД.ММ.ГГГГ):")

@router.message()
async def main_handler(message: types.Message):
    code = get_core_code(message.text)
    if code:
        await message.answer("📡 *Считываю частоту ядра...*")
        prompt = f"Код судьбы {code}, дата {message.text}. Дай краткий киберпанк-прогноз."
        ai_res = await get_ai_interpretation(prompt)
        await message.answer(f"✅ **CORE TYPE {code}**\n\n{ai_res}", parse_mode="Markdown")
    else:
        await message.answer("❌ Введи дату цифрами.")

async def main():
    dp.include_router(router)
    print("[SYSTEM]: Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Критическая ошибка запуска: {e}")


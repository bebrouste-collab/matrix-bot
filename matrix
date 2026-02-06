import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from openai import OpenAI

# --- ПОЛУЧЕНИЕ ТОКЕНОВ ИЗ ПЕРЕМЕННЫХ RAILWAY ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Инициализация ИИ через OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
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

# Запрос к нейросети Gemini
async def get_ai_interpretation(prompt):
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {"role": "system", "content": "Ты — Matrix Debugger. Ты анализируешь жизнь как программный код. Твой стиль: киберпанк, технический сленг, ирония. Обращайся к пользователю 'Unit'."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Системный сбой ИИ: {str(e)}"

# Обработка команды /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "📟 **[SYSTEM]: Вход в протокол REAL-OS выполнен.**\n"
        "-------------------------------------\n"
        "Обнаружена новая био-система. Введи дату рождения (ДД.ММ.ГГГГ) для калибровки:"
    )

# Обработка даты рождения
@router.message()
async def main_handler(message: types.Message):
    code = get_core_code(message.text)
    if code:
        await message.answer("📡 *Считываю частоту ядра...*")
        prompt = f"Пользователь с кодом судьбы {code} и датой рождения {message.text}. Дай краткий и умный киберпанк-прогноз. Используй термины: баги, патч, апгрейд."
        ai_res = await get_ai_interpretation(prompt)
        
        response = (
            f"✅ **ID ВАЛИДЕН: CORE TYPE {code}**\n"
            f"-------------------------------------\n"
            f"{ai_res}"
        )
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("❌ [ERROR]: Введите дату цифрами (например, 15.05.1995)")

async def main():
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    print("[SYSTEM]: Matrix Bot запущен в облаке Railway...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

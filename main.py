import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from openai import OpenAI

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- КЛЮЧИ ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
AI_KEY = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=AI_KEY)
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# --- КЛАВИАТУРА ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🧬 Код Судьбы")
    builder.button(text="💰 Прогноз Успеха")
    builder.button(text="❤️ Совместимость")
    builder.button(text="❓ Как это работает?")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# --- ЛОГИКА РАСЧЕТА ---
def get_matrix_number(date_str):
    digits = [int(d) for d in date_str if d.isdigit()]
    if not digits: return None
    res = sum(digits)
    while res > 9: res = sum(int(d) for d in str(res))
    return res

# --- ОБРАБОТЧИКИ ---

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "📟 **[SYSTEM]: Вход в Matrix Debugger выполнен.**\n\n"
        "Я анализирую твою дату рождения как программный код и предсказываю баги и апгрейды твоей реальности.",
        reply_markup=main_menu()
    )

@router.message(F.text == "❓ Как это работает?")
async def help_info(message: types.Message):
    await message.answer(
        "📜 **ИНСТРУКЦИЯ ПОЛЬЗОВАТЕЛЯ:**\n\n"
        "1. Выбери нужный режим в меню.\n"
        "2. Пришли свою дату рождения в формате `10.02.2008`.\n"
        "3. Если выбрал 'Совместимость' — пришли две даты через пробел.\n"
        "4. ИИ просканирует матрицу и выдаст вердикт.",
        reply_markup=main_menu()
    )

@router.message(F.text.in_(["🧬 Код Судьбы", "💰 Прогноз Успеха", "❤️ Совместимость"]))
async def ask_date(message: types.Message):
    await message.answer(f"⏳ **Режим [{message.text}] активирован.**\nПришли дату(ы) рождения:")

@router.message()
async def universal_handler(message: types.Message):
    text = message.text
    # Простая проверка на наличие цифр (поиск даты)
    nums = [d for d in text if d.isdigit()]
    
    if len(nums) < 4:
        await message.answer("⚠️ Ошибка: Система требует дату рождения (например, 20.05.1995)")
        return

    await message.answer("📡 *Устанавливаю соединение с серверами Матрицы...*")
    
    # Формируем запрос в зависимости от контекста
    prompt = f"Проанализируй дату {text}. "
    if "Совместимость" in text or len(nums) > 10:
        prompt += "Это анализ совместимости двух людей. Расскажи про их баги в отношениях и общие апгрейды."
    elif "Успех" in text:
        prompt += "Это прогноз на успех и финансы. Пиши в стиле киберпанк про инвестиции в себя и системные ошибки."
    else:
        prompt += "Это общий анализ личности (Код Судьбы). Опиши сильные стороны и скрытые угрозы."

    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {"role": "system", "content": "Ты — Matrix Debugger. Стиль: киберпанк, ирония, технический сленг. Обращайся к пользователю 'Оператор' или 'Юзер'."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_res = completion.choices[0].message.content
        await message.answer(f"📥 **РЕЗУЛЬТАТ СКАНИРОВАНИЯ:**\n\n{ai_res}", parse_mode="Markdown")
    except Exception as e:
        await message.answer("❌ Произошел разрыв соединения с ИИ.")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

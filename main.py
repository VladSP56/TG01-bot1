from select import error
from telegram.ext import ApplicationBuilder, CommandHandler
import requests
from config import TELEGRAM_TOKEN, OPENWEATHER_API_KEY

#bot = Bot(token=TOKEN)

#TELEGRAM_TOKEN = "TOKEN"

CITY = "Moscow"


async def start(update, context):
    await update.message.reply_text("Привет! Напиши /weather чтобы узнать погоду.")


async def weather(update, context):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
        response = requests.get(url).json()
        print("Ответ API:", response) # для отладки

        if response["cod"] == 200:
            temp = response["main"]["temp"]
            description = response["weather"][0]["description"]
            await update.message.reply_text(f"Погода в {CITY}: {temp}°C, {description}.")
        else:
            error_msg = response.get("message", "Неизвестная ошибка API")
            await update.message.reply_text(F"Ошибка: {error_msg} Код: {response.get('cod')})")
    except Exception as e:
        await update.message.reply_text("Ошибка при запросе погоды.")


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    application.run_polling()


if __name__ == "__main__":
    main()
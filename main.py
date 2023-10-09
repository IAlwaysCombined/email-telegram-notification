import os

from dotenv import load_dotenv

from bot import TelegramBot

if __name__ == "__main__":
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    bot = TelegramBot(bot_token)
    bot.start()

from telegram import Bot

from email_monitor import EmailMonitor


class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.monitor = EmailMonitor(self.bot)

    def start(self):
        self.monitor = EmailMonitor(self.bot)
        self.monitor.start()

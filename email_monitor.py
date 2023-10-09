import asyncio
import email
import imaplib
import os
from email.header import decode_header

from dotenv import load_dotenv

from telegram_notifier import TelegramNotifier

load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


class EmailMonitor:
    def __init__(self, bot):
        self.bot = bot
        self.telegram_notifier = TelegramNotifier(self.bot)
        self.email_address = email_address
        self.email_password = email_password

    def fetch_and_send_notifications(self):
        try:
            # Подключение к почтовому серверу Яндекс Почты
            imap_server = imaplib.IMAP4_SSL('imap.yandex.ru')
            imap_server.login(email_address, email_password)

            # Выбор папки Inbox (или другой папки, если нужно)
            imap_server.select('INBOX')

            # Поиск новых писем
            status, email_ids = imap_server.search(None, 'UNSEEN')

            if status == 'OK':
                email_ids = email_ids[0].split()
                for email_id in email_ids:
                    # Получение письма
                    status, email_data = imap_server.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        msg = email.message_from_bytes(email_data[0][1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')

                        # Отправка уведомления во все чаты
                        message = f"Новое письмо: {subject}"
                        asyncio.run(self.telegram_notifier.send_notification_to_all_chats(message))

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")

    def start(self):
        while True:
            self.fetch_and_send_notifications()

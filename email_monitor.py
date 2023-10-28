import asyncio
import email
import imaplib
import os
from datetime import datetime, timedelta
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
        self.processed_emails = set()

    async def fetch_and_send_notifications(self):
        try:
            # Подключение к почтовому серверу Яндекс Почты
            imap_server = imaplib.IMAP4_SSL('imap.yandex.ru')
            imap_server.login(email_address, email_password)

            # Выбор папки Inbox (или другой папки, если нужно)
            imap_server.select('INBOX')

            # Вычисляем дату вчерашнего дня
            yesterday = datetime.now() - timedelta(days=1)
            yesterday_str = yesterday.strftime("%d-%b-%Y")

            # Поиск новых писем, не старше вчерашней даты
            status, email_ids = imap_server.search(None, 'UNSEEN', 'SINCE', yesterday_str)

            if status == 'OK':
                email_ids = email_ids[0].split()
                for email_id in email_ids:
                    if email_id not in self.processed_emails:
                        # Получение письма
                        status, email_data = imap_server.fetch(email_id, '(RFC822)')
                        if status == 'OK':
                            msg = email.message_from_bytes(email_data[0][1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding or 'utf-8')

                            date, date_encoding = decode_header(msg["Date"])[0]
                            if isinstance(date, bytes):
                                date = date.decode(date_encoding or 'utf-8')

                            from_user, from_user_encoding = decode_header(msg["From"])[0]
                            if isinstance(from_user, bytes):
                                from_user = from_user.decode(from_user_encoding or 'utf-8')

                            # Отправка уведомления во все чаты
                            message = f"Новое письмо: {subject},\nОт: {from_user},\nКогда: {date}"
                            await self.telegram_notifier.send_notification_to_all_chats(message)

                            # Добавить UID письма в список обработанных
                            self.processed_emails.add(email_id)

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")

    async def start(self):
        while True:
            await self.fetch_and_send_notifications()
            await asyncio.sleep(60)

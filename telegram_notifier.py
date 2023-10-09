import logging


class TelegramNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def send_notification_to_all_chats(self, message):
        for update in await self.bot.get_updates():
            chat_id = update.message.chat_id
            await self.bot.send_message(chat_id=chat_id, text=message)

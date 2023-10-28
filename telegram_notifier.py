from telegram import Chat


class TelegramNotifier:
    def __init__(self, bot):
        self.bot = bot

    async def send_notification_to_all_chats(self, message):
        for update in await self.bot.get_updates():
            chat = update.message.chat
            if chat.type == Chat.GROUP or chat.type == Chat.SUPERGROUP:
                chat_id = chat.id
                await self.bot.send_message(chat_id=chat_id, text=message)

from telethon import TelegramClient, events, sync
import asyncio, time
import config
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = config.TELEGRAM_API_ID
api_hash = config.TELEGRAM_API_HASH
bot_token = config.TELEGRAM_BOT_TOKEN

client = TelegramClient('telegram-bot', api_id, api_hash)
client.start()


if __name__ == "__main__":
    
    @client.on(events.NewMessage)
    async def my_event_handler(event):
        if 'http' and 'zalando.' in event.raw_text:
            await event.reply('Nueva búsqueda añadida')

    async def main():
        while True:
            print(".")
            time.sleep(10)
            await asyncio.sleep(10)

    client.loop.run_until_complete(main())
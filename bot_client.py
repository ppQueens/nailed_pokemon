import pyrogram
import utils

client = pyrogram.Client(
    'nearby_purchases_places_bot',
    api_id=utils.get_telegram_api_id(),
    api_hash=utils.get_telegram_api_hash(),
    bot_token=utils.get_telegram_secret_key()
)

import pyrogram
from config_provider import get_telegram_api_id, get_telegram_api_hash, get_telegram_secret_key

client = pyrogram.Client(
    'nearby_purchases_places_bot',
    api_id=get_telegram_api_id(),
    api_hash=get_telegram_api_hash(),
    bot_token=get_telegram_secret_key()
)

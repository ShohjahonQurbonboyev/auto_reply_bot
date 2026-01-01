from telethon import TelegramClient, events
from telethon.tl.types import DocumentAttributeAudio
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


try :
    load_dotenv()

    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    SESSION_NAME = os.getenv("SESSION_NAME", "anon")

    if not API_ID or not API_HASH:
        raise ValueError("❌ API_ID yoki API_HASH topilmadi (.env ni tekshir)")

    API_ID = int(API_ID)


    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


    REPLY_COOLDOWN = timedelta(hours=5) 


    replied_users = {}


    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    AUDIO_FILE_PATH = os.path.join(BASE_PATH, "Avtojavob.ogg")
except Exception as ex:
    pass

if not os.path.exists(AUDIO_FILE_PATH):
    raise FileNotFoundError("❌ Avtojavob.ogg topilmadi")

try:
    def cleanup_replied_users():
        now = datetime.now()
        expired = [
            user_id for user_id, last_time in replied_users.items()
            if now - last_time >= REPLY_COOLDOWN
        ]
        for user_id in expired:
            del replied_users[user_id]
except Exception as ex:
    pass

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:

        if not event.is_private:
            return

        
        cleanup_replied_users()

        
        hour = datetime.now().hour
        if not (0 <= hour < 23):
            return

        sender = await event.get_sender()
        sender_id = sender.id

        
        if sender_id in replied_users:
            print(f"⏳ {sender.first_name} uchun cooldown tugamagan")
            return

        
        await client.send_file(
            event.chat_id,
            AUDIO_FILE_PATH,
            attributes=[
                DocumentAttributeAudio(
                    duration=0,
                    voice=True
                )
            ]
        )

        replied_users[sender_id] = datetime.now()
    except Exception as ex:
        pass


client.start()
print("✅ Avto voice bot ishga tushdi...")
client.run_until_disconnected()

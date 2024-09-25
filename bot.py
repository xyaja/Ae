from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

api_id = "29726374"
api_hash = "ee797487083e78676bc682c2e78df5fc"
bot_token = "7076412312:AAEuWXMtJaNldQq012gXShXBgX3TPq-WUZY"

mongo_client = os.getenv("mongodb+srv://otwnyoba:Rizqi1687.@on.7tzx4.mongodb.net/?retryWrites=true&w=majority&appName=on")
try:
    mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    mongo_client.server_info()  # Ini akan memicu koneksi dan pengecekkan
    db = mongo_client["forward_bot"]
    forward_collection = db["forward_ids"]
    channel_collection = db["channel_ids"]
    logger.info("Berhasil terhubung ke MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    logger.error(f"Gagal terhubung ke MongoDB: {e}")
    mongo_client = None
    db = None
    forward_collection = None
    channel_collection = None

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Decorator untuk memeriksa koneksi MongoDB
def check_mongo_connection(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        if mongo_client is None:
            await message.reply_text("Maaf, saat ini database tidak tersedia. Silakan coba lagi nanti.")
            return
        return await func(client, message, *args, **kwargs)
    return wrapper

@app.on_message(filters.command("addch"))
@check_mongo_connection
async def add_forward_id(client, message):
    if len(message.command) > 1:
        forward_id = message.command[1]
        try:
            forward_collection.insert_one({"_id": forward_id})
            await message.reply_text(f"ID forward {forward_id} telah ditambahkan.")
        except DuplicateKeyError:
            await message.reply_text("ID forward ini sudah ada dalam database.")
    else:
        await message.reply_text("Gunakan format: /addch [id_forward]")

@app.on_message(filters.command("ch"))
@check_mongo_connection
async def add_channel_id(client, message):
    if len(message.command) > 1:
        channel_id = message.command[1]
        try:
            channel_collection.insert_one({"_id": channel_id})
            await message.reply_text(f"ID channel {channel_id} telah ditambahkan.")
        except DuplicateKeyError:
            await message.reply_text("ID channel ini sudah ada dalam database.")
    else:
        await message.reply_text("Gunakan format: /ch [id_channel]")

@app.on_message(filters.command("bt"))
async def create_button(client, message):
    if len(message.command) > 2:
        button_text = message.command[1]
        button_url = message.command[2]
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])
        if message.reply_to_message:
            if message.reply_to_message.photo:
                await message.reply_to_message.reply_photo(
                    photo=message.reply_to_message.photo.file_id,
                    caption=message.reply_to_message.caption,
                    reply_markup=keyboard
                )
            elif message.reply_to_message.text:
                await message.reply_to_message.reply_text(
                    text=message.reply_to_message.text,
                    reply_markup=keyboard
                )
            else:
                await message.reply_text("Balas pesan dengan foto atau teks untuk menambahkan tombol.")
        else:
            await message.reply_text("Balas pesan untuk menambahkan tombol.")
    else:
        await message.reply_text("Gunakan format: /bt [teks_tombol] [url_tombol]")

@app.on_message(filters.command("listch"))
@check_mongo_connection
async def list_channels(client, message):
    channels = channel_collection.find()
    channel_list = [ch["_id"] for ch in channels]
    if channel_list:
        await message.reply_text(f"Daftar ID channel: {', '.join(channel_list)}")
    else:
        await message.reply_text("Tidak ada ID channel yang terdaftar.")

@app.on_message(filters.command("listaddch"))
@check_mongo_connection
async def list_forward_ids(client, message):
    forwards = forward_collection.find()
    forward_list = [fwd["_id"] for fwd in forwards]
    if forward_list:
        await message.reply_text(f"Daftar ID forward: {', '.join(forward_list)}")
    else:
        await message.reply_text("Tidak ada ID forward yang terdaftar.")

@app.on_message(filters.command("delch"))
@check_mongo_connection
async def delete_channel(client, message):
    if len(message.command) > 1:
        channel_id = message.command[1]
        result = channel_collection.delete_one({"_id": channel_id})
        if result.deleted_count > 0:
            await message.reply_text(f"ID channel {channel_id} telah dihapus.")
        else:
            await message.reply_text(f"ID channel {channel_id} tidak ditemukan.")
    else:
        await message.reply_text("Gunakan format: /delch [id_channel]")

@app.on_message(filters.command("deladdch"))
@check_mongo_connection
async def delete_forward_id(client, message):
    if len(message.command) > 1:
        forward_id = message.command[1]
        result = forward_collection.delete_one({"_id": forward_id})
        if result.deleted_count > 0:
            await message.reply_text(f"ID forward {forward_id} telah dihapus.")
        else:
            await message.reply_text(f"ID forward {forward_id} tidak ditemukan.")
    else:
        await message.reply_text("Gunakan format: /deladdch [id_forward]")

@app.on_message(filters.incoming & ~filters.command("addch") & ~filters.command("ch") & 
                ~filters.command("bt") & ~filters.command("listch") & ~filters.command("listaddch") & 
                ~filters.command("delch") & ~filters.command("deladdch"))
@check_mongo_connection
async def auto_forward(client, message):
    forward_ids = [fwd["_id"] for fwd in forward_collection.find()]
    if str(message.chat.id) in forward_ids:
        channel_ids = [ch["_id"] for ch in channel_collection.find()]
        for channel_id in channel_ids:
            try:
                await message.forward(channel_id)
            except Exception as e:
                logger.error(f"Gagal meneruskan pesan ke {channel_id}: {str(e)}")

if __name__ == "__main__":
    app.run()

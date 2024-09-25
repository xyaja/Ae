from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

api_id = "API_ID"
api_hash = "API_HASH"
bot_token = "BOT_TOKEN"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

forward_ids = []
channel_ids = []

@app.on_message(filters.command("addch"))
def add_forward_id(client, message):
    if len(message.command) > 1:
        forward_id = message.command[1]
        if forward_id not in forward_ids:
            forward_ids.append(forward_id)
            message.reply_text(f"ID forward {forward_id} telah ditambahkan.")
        else:
            message.reply_text("ID forward ini sudah ada dalam daftar.")
    else:
        message.reply_text("Gunakan format: /addch [id_forward]")

@app.on_message(filters.command("ch"))
def add_channel_id(client, message):
    if len(message.command) > 1:
        channel_id = message.command[1]
        if channel_id not in channel_ids:
            channel_ids.append(channel_id)
            message.reply_text(f"ID channel {channel_id} telah ditambahkan.")
        else:
            message.reply_text("ID channel ini sudah ada dalam daftar.")
    else:
        message.reply_text("Gunakan format: /ch [id_channel]")

@app.on_message(filters.command("bt"))
def create_button(client, message):
    if len(message.command) > 2:
        button_text = message.command[1]
        button_url = message.command[2]
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])
        if message.reply_to_message and message.reply_to_message.photo:
            message.reply_to_message.reply_photo(
                photo=message.reply_to_message.photo.file_id,
                caption=message.reply_to_message.caption,
                reply_markup=keyboard
            )
        else:
            message.reply_text("Balas pesan dengan foto untuk menambahkan tombol.")
    else:
        message.reply_text("Gunakan format: /bt [teks_tombol] [url_tombol]")

@app.on_message(filters.command("forward"))
def forward_message(client, message):
    if forward_ids and channel_ids:
        for forward_id in forward_ids:
            for channel_id in channel_ids:
                try:
                    app.forward_messages(chat_id=channel_id, from_chat_id=forward_id, message_ids=message.id)
                except Exception as e:
                    message.reply_text(f"Gagal meneruskan pesan ke {channel_id}: {str(e)}")
        message.reply_text("Pesan telah diteruskan ke semua channel yang terdaftar.")
    else:
        message.reply_text("Tambahkan ID forward dan ID channel terlebih dahulu.")

app.run()

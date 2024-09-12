# main.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_channel_data, set_channel_source, add_channel_destination
import config

app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

@app.on_message(filters.command('start'))
def start(client, message):
    welcome_message = "Selamat datang! Gunakan /help untuk melihat perintah yang tersedia."
    help_button = InlineKeyboardButton("Help", callback_data="help")
    reply_markup = InlineKeyboardMarkup([[help_button]])
    message.reply_text(welcome_message, reply_markup=reply_markup)

@app.on_message(filters.command('help'))
def help(client, message):
    help_text = (
        "/ch <keyword> <channel_id> - Mengatur channel sumber untuk forwarding dengan kunci tertentu\n"
        "/addch <keyword> <channel_id> - Menambahkan channel tujuan untuk forwarding dengan kunci tertentu"
    )
    message.reply_text(help_text)

@app.on_message(filters.command('ch'))
def set_channel_source_handler(client, message):
    if message.chat.type == 'private':
        parts = message.text.split(' ', 2)
        if len(parts) == 3 and parts[2].startswith("-100"):
            keyword = parts[1]
            channel_id = parts[2]
            set_channel_source(keyword, channel_id)
            message.reply_text(f"Channel sumber untuk kunci '{keyword}' telah diset ke {channel_id}.")
        else:
            message.reply_text("Format ID channel salah. Gunakan format: /ch <keyword> -100123456789")
    else:
        message.reply_text("Perintah ini hanya dapat digunakan dalam chat pribadi.")

@app.on_message(filters.command('addch'))
def add_channel_destination_handler(client, message):
    if message.chat.type == 'private':
        parts = message.text.split(' ', 2)
        if len(parts) == 3 and parts[2].startswith("-100"):
            keyword = parts[1]
            channel_id = parts[2]
            add_channel_destination(keyword, channel_id)
            message.reply_text(f"Channel tujuan untuk kunci '{keyword}' telah ditambahkan: {channel_id}.")
        else:
            message.reply_text("Format ID channel salah. Gunakan format: /addch <keyword> -100123456789")
    else:
        message.reply_text("Perintah ini hanya dapat digunakan dalam chat pribadi.")

@app.on_message(filters.chat(lambda c: c.type == 'channel') & filters.text)
def forward_message_handler(client, message):
    for keyword in db['channels'].find():
        channel_data = get_channel_data(keyword['_id'])
        if channel_data and channel_data['source_channel'] == message.chat.id:
            for destination_channel in channel_data.get('destination_channels', []):
                try:
                    client.forward_messages(chat_id=destination_channel, from_chat_id=message.chat.id, message_ids=message.message_id)
                except Exception as e:
                    print(f"Error forwarding message to {destination_channel}: {e}")

app.run()

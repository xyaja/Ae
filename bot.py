id# main.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_channel_data, set_channel_source, add_channel_destination
import config

app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Fungsi untuk mengirim pesan utama dengan foto dan tombol
@app.on_message(filters.command('start'))
def start(client, message):
    buttons = [
        [InlineKeyboardButton("Button 1", callback_data="button1")],
        [InlineKeyboardButton("Button 2", callback_data="button2")],
        [InlineKeyboardButton("Button 3", callback_data="button3")],
        [InlineKeyboardButton("Button 4", url="https://example.com")]
    ]
    
    # Kirim foto dengan caption dan tombol
    message.reply_photo(
        photo="qris.jpg",  # Ganti dengan URL foto yang diinginkan
        caption="Ini adalah caption foto.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Fungsi untuk menangani callback query
@app.on_callback_query()
def callback_query(client, callback_query):
    data = callback_query.data

    # Tombol "Back" untuk kembali ke pesan utama
    back_button = InlineKeyboardButton("Back", callback_data="back")

    if data == "button1":
        # Menampilkan teks dengan tombol "Back"
        callback_query.message.edit_text(
            "Button 1 pressed.\n\n[Back](https://t.me/your_bot_username?start)",
            reply_markup=InlineKeyboardMarkup([[back_button]])
        )
    elif data == "button2":
        # Menampilkan teks dengan tombol "Back"
        callback_query.message.edit_text(
            "Button 2 pressed.\n\n[Back](https://t.me/your_bot_username?start)",
            reply_markup=InlineKeyboardMarkup([[back_button]])
        )
    elif data == "button3":
        # Menampilkan foto dengan caption dan tombol "Back"
        callback_query.message.edit_photo(
            photo="qris.jpg",  # Ganti dengan URL foto yang diinginkan
            caption="Ini adalah caption foto kedua.\n\n[Back](https://t.me/your_bot_username?start)",
            reply_markup=InlineKeyboardMarkup([[back_button]])
        )
    elif data == "back":
        # Kembali ke pesan utama
        callback_query.message.edit_photo(
            photo="qris.jpg",  # URL foto utama
            caption="Ini adalah caption foto.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Button 1", callback_data="button1")],
                [InlineKeyboardButton("Button 2", callback_data="button2")],
                [InlineKeyboardButton("Button 3", callback_data="button3")],
                [InlineKeyboardButton("Button 4", url="https://example.com")]
            ])
        )

app.run()

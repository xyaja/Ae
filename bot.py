import asyncio
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN


app = Client(
  "mybot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("start"))
async def send_photo_with_button(client, message):
    # 2.1. Buat tombol inline
    button = InlineKeyboardButton("Klik Saya!", callback_data="dana")
    keyboard = InlineKeyboardMarkup([[button]])

    # 2.2. Balas dengan foto dan tombol
    await message.reply_photo(
        photo="qris.jpg",  # Ganti dengan path ke foto Anda
        caption="Ini adalah caption foto dengan tombol.",
        reply_markup=keyboard
    )

app.on_callback_query()
async def handle_callback_query( client, query):
    if query.data == "dana":
        await query.answer("085175176376")
    #elif query.data == "gopay":
        # await query.answer("085175176376")

app.run()

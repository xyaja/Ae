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


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    button1 = InlineKeyboardButton("DANA", callback_data="dana")
    button2 = InlineKeyboardButton("GOPAY", callback_data="gopay")

    keyboard = InlineKeyboardButton([[button1, button2]])

        await message.reply_photo(
            chat_id=message.chat.id
            photo="qris.jpg",
            caption="TES",
            reply_markup=keyboard
         )
    
app.on_callback_query()
async def handle_callback_query( client, query):
    if query.data == "dana":
        await query.answer("085175176376")
    elif query.data == "gopay":
         await query.answer("085175176376")

app.run()

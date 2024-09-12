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
async def start(client,message):
    photo = "qris.jpg"
    caption = "test"
    button = InlineKeyboardMarkup([
    [InlineKeyboardButton("DANA", callback_data="dana")]
    ])
        await send_photo(photo, caption=caption, raply_markup=keyboard)

app.on_callback_query()
async def handle_callback_query( client, query):
    if query.data == "dana":
        await query.answer("085175176376")
    #elif query.data == "gopay":
        # await query.answer("085175176376")

app.run()

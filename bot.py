import asyncio
from pyrogram import Client, filters
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
  "mybot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def send_photo(client, message):
    keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("DANA", callback_data="dana")]
    ])

await message_reply(
  "p",
  reply_Markup=keyboard 
)

@app.on_callback_query()
async def callback_query(client, callback_query):
  
  data = callback_query.data

if data == "button_clicked":
  await callback_query.answer("DANA 085175176376", show_alert=True)
  

app.run()

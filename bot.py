import asyncio
from pyrogram import Client, filters
from pyrogram.raw import functions .types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER
from database.database import add_user, del_user, full_userbase, present_user 


app = Client(
  "mybot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN,
)


@app.on_message(filters.command("start"))
async def start(client, message):
    await app.send_photo("me", "qris.jpg", caption="tes")
    

app.run()
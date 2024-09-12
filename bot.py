import asyncio
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER 


app = Client(
  "mybot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN,
)


@app.on_message(filters.command("start"))
    def start_command(client, message):
    message.reply_text("tes")
    

app.run()

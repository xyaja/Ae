# bot.py

from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.start_handler import start
from handlers.addch_handler import addch
from handlers.toch_handler import toch

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await start(client, message)

@app.on_message(filters.command("addch"))
async def addch_handler(client, message):
    await addch(client, message)

@app.on_message(filters.command("toch"))
async def toch_handler(client, message):
    await toch(client, message)

if __name__ == "__main__":
    app.run()

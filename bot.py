from pyrogram import Client, filters
import config

app = Client(
  "mybot",
  api_id="API_ID",
  api_hash="API_HASH",
  bot_token="BOT_TOKEN"
)

app.on_message(filters.command(start))
async def start(client, message):
    await message.reply_text("hay")

app.run()

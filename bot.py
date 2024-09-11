import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER
from database.database import add_user, del_user, full_userbase, present_user 


app = Client(
  "mybot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN,
)


async def send_photo(client, message):
    photo = "path/to/photo.jpg"  # replace with the actual photo path
    caption = "This is a sample photo"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Send Text", callback_data="send_text")]
    ])
    await client.send_photo(message.chat.id, photo, caption=caption, reply_markup=keyboard)

# Define a function to handle the inline keyboard button callback
async def handle_callback(client, callback_query):
    if callback_query.data == "send_text":
        text = "This is a sample text"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Go Back", callback_data="go_back")]
        ])
        await callback_query.message.reply_text(text, reply_markup=keyboard)
    elif callback_query.data == "go_back":
        await callback_query.message.reply_text("You are back!")

# Register the functions with Pyrogram
@app.on_message(filters.command("start"))
async def start(client, message):
    await send_photo(client, message)

@app.on_callback_query(filters.regex("send_text|go_back"))
async def handle_callback_query(client, callback_query):
    await handle_callback(client, callback_query)

# Run the Pyrogram client
app.run()
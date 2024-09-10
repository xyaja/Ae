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
  owner=config.OWNER,
)

@app.on_message(filters.command("start") & filters.private & filters.user(OWNER))
async def send_photo(client, message):
    photo = "qris.jpg"
    caption = "tes"

    keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("DANA", callback_data="dana")]
    ])

    try:
        await client.send_photo(message.chat.id, photo, caption=caption, reply_markup=keyboard)
    except Exception as e:
        await message.reply_text(f"eror send photo: {e}")
      
@app.on_callback_query(filters.regex("dana"))
async def callback_query(client, callback_query):
  await callback_query.message.reply_text("DANA 085175176376")

@app.on_message(filters.command('users') & filters.private & filters.user("OWNER"))
async def get_users(client: app, message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@app.on_message(filters.private & filters.command('broadcast') & filters.user(config.OWNER))
async def send_text(client: app, message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
  
if __name__=="__main__":
   app.run()

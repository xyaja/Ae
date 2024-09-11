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


@app.on_message(filters.command("start") & filters.private)
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
async def dana_callback_query(client, message):
    await query.answer("Anda telah memilih metode pembayaran DANA.")
    
 #   nomor tujuan = 085175176376
  #  atas nama = CAS****H

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "KEMBALI", callback_data="dana"
                ),
            ]
        ]
    )

if __name__=="__main__":
   app.run()

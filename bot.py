from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_command(client, message):
    # URL foto yang akan dikirim
    photo = "qris.jpg"
    
    # Membuat keyboard inline
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Konfirmasi", callback_data="confirm")],
        [InlineKeyboardButton("Kembali", callback_data="back")]
    ])
    
    # Mengirim foto dengan caption dan tombol
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption="Ini adalah foto dengan tombol. Silakan pilih:",
        reply_markup=keyboard
    )

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "confirm":
        await callback_query.answer("Anda telah mengkonfirmasi!")
        await callback_query.message.reply_text("Terima kasih atas konfirmasi Anda.")
    elif callback_query.data == "back":
        await callback_query.answer("Kembali ke menu sebelumnya.")
        # Di sini Anda bisa menambahkan logika untuk kembali ke menu sebelumnya

app.run()

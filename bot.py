from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


MAIN_PHOTO_URL = "qris.jpg"
CONFIRMATION_PHOTO_URL = "qris.jpg"

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await send_main_photo(client, message.chat.id)

async def send_main_photo(client, chat_id):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Dana", callback_data="dana")],
        [InlineKeyboardButton("Konfirmasi", callback_data="confirm")]
    ])
    
    await client.send_photo(
        chat_id=chat_id,
        photo=MAIN_PHOTO_URL,
        caption="Silakan pilih opsi:",
        reply_markup=keyboard
    )

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "dana":
        await callback_query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Kembali", callback_data="back_to_main")]
        ])
        await callback_query.message.reply_text(
            "Informasi tentang Dana:\n\n"
            "Dana adalah layanan dompet digital dan pembayaran online. "
            "Anda dapat menggunakannya untuk berbagai transaksi seperti "
            "transfer uang, pembayaran tagihan, dan pembelian online.",
            reply_markup=keyboard
        )
    elif callback_query.data == "confirm":
        await callback_query.answer()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Kembali", callback_data="back_to_main")]
        ])
        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=CONFIRMATION_PHOTO_URL,
            caption="Konfirmasi berhasil! Terima kasih.",
            reply_markup=keyboard
        )
    elif callback_query.data == "back_to_main":
        await callback_query.answer()
        await send_main_photo(client, callback_query.message.chat.id)

app.run()

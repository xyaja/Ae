# handlers/start_handler.py

from pyrogram import Client

async def start(client: Client, message):
    await message.reply(
        "Halo! Berikut adalah perintah yang tersedia:\n"
        "/addch <keyword> <channel_id> - Tambahkan ID channel untuk keyword tertentu. ID channel harus dimulai dengan '-100'.\n"
        "/toch <keyword> - Terima pesan dan teruskan ke channel yang sesuai dengan keyword. ID channel harus dimulai dengan '-100'."
    )

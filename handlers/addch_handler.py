# handlers/addch_handler.py

from pyrogram import Client
from config import CHANNELS
from utils.helpers import check_admin

async def addch(client: Client, message):
    parts = message.text.split(' ', 2)
    if len(parts) != 3:
        await message.reply("Format perintah tidak valid. Gunakan: /addch <keyword> <channel_id>, di mana <channel_id> dimulai dengan '-100'.")
        return

    keyword, channel_id = parts[1], parts[2]

    if not channel_id.startswith('-100'):
        await message.reply("ID channel tidak valid. Harus dimulai dengan '-100'.")
        return

    if keyword not in CHANNELS:
        CHANNELS[keyword] = []

    if channel_id not in CHANNELS[keyword]:
        if await check_admin(client, channel_id):
            CHANNELS[keyword].append(channel_id)
            await message.reply(f"ID channel {channel_id} telah ditambahkan untuk keyword '{keyword}'.")
        else:
            await message.reply("Bot harus menjadi admin di channel ini untuk dapat meneruskan pesan.")
    else:
        await message.reply(f"ID channel {channel_id} sudah ada untuk keyword '{keyword}'.")

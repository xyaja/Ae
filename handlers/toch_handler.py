# handlers/toch_handler.py

from pyrogram import Client
from config import CHANNELS
from utils.helpers import check_admin

async def toch(client: Client, message):
    parts = message.text.split(' ', 1)
    if len(parts) != 2:
        await message.reply("Format perintah tidak valid. Gunakan: /toch <keyword>.")
        return

    keyword = parts[1]

    if keyword not in CHANNELS:
        await message.reply(f"Keyword '{keyword}' tidak ditemukan. Gunakan /addch untuk menambahkannya.")
        return

    channel_ids = CHANNELS[keyword]

    for source_channel_id in channel_ids:
        if not await check_admin(client, source_channel_id):
            await message.reply(f"Bot tidak memiliki hak admin di channel {source_channel_id}.")
            return

    # Meneruskan pesan dari setiap channel yang terdaftar
    for source_channel_id in channel_ids:
        async for msg in client.get_chat_history(source_channel_id):
            for target_channel_id in channel_ids:
                if target_channel_id != source_channel_id:
                    await client.forward_messages(
                        chat_id=target_channel_id,
                        from_chat_id=source_channel_id,
                        message_ids=msg.message_id
                    )
    await message.reply("Pesan telah diteruskan ke channel yang sesuai.")

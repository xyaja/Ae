from pyrogram import Client, filters
from config import API_ID, API_HASH

app = Client("my_bot", api_id="API_ID", api_hash="API_HASH")

# Daftar untuk menyimpan ID channel
channel_ids = []

@app.on_message(filters.command("add_channel"))
async def add_channel(client, message):
    # Mengambil ID channel dari argumen perintah
    if len(message.command) < 2:
        await message.reply("Silakan masukkan ID channel setelah perintah.")
        return
    
    channel_id = message.command[1]
    channel_ids.append(channel_id)
    await message.reply(f"Channel ID {channel_id} berhasil ditambahkan.")

@app.on_message(filters.command("forward"))
async def forward_message(client, message):
    if not channel_ids:
        await message.reply("Tidak ada channel yang terdaftar untuk meneruskan pesan.")
        return

    for channel_id in channel_ids:
        await client.send_message(channel_id, message.reply_to_message.text)

@app.on_message(filters.private)
async def echo(client, message):
    await message.reply("Kirim /add_channel <channel_id> untuk menambahkan channel.")

app.run()

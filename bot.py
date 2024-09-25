from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = "29726374"
api_hash = "ee797487083e78676bc682c2e78df5fc"
bot_token = "7076412312:AAEuWXMtJaNldQq012gXShXBgX3TPq-WUZY"

mongo_client = MongoClient(os.getenv("mongodb+srv://otwnyoba:Rizqi1687.@on.7tzx4.mongodb.net/?retryWrites=true&w=majority&appName=on"))
db = mongo_client["forward_bot"]
forward_collection = db["forward_ids"]
channel_collection = db["channel_ids"]

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("addch"))
def add_forward_id(client, message):
    if len(message.command) > 1:
        forward_id = message.command[1]
        try:
            forward_collection.insert_one({"_id": forward_id})
            message.reply_text(f"ID forward {forward_id} telah ditambahkan.")
        except DuplicateKeyError:
            message.reply_text("ID forward ini sudah ada dalam database.")
    else:
        message.reply_text("Gunakan format: /addch [id_forward]")

@app.on_message(filters.command("ch"))
def add_channel_id(client, message):
    if len(message.command) > 1:
        channel_id = message.command[1]
        try:
            channel_collection.insert_one({"_id": channel_id})
            message.reply_text(f"ID channel {channel_id} telah ditambahkan.")
        except DuplicateKeyError:
            message.reply_text("ID channel ini sudah ada dalam database.")
    else:
        message.reply_text("Gunakan format: /ch [id_channel]")

@app.on_message(filters.command("bt"))
def create_button(client, message):
    if len(message.command) > 2:
        button_text = message.command[1]
        button_url = message.command[2]
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=button_url)]])
        if message.reply_to_message:
            if message.reply_to_message.photo:
                message.reply_to_message.reply_photo(
                    photo=message.reply_to_message.photo.file_id,
                    caption=message.reply_to_message.caption,
                    reply_markup=keyboard
                )
            elif message.reply_to_message.text:
                message.reply_to_message.reply_text(
                    text=message.reply_to_message.text,
                    reply_markup=keyboard
                )
            else:
                message.reply_text("Balas pesan dengan foto atau teks untuk menambahkan tombol.")
        else:
            message.reply_text("Balas pesan untuk menambahkan tombol.")
    else:
        message.reply_text("Gunakan format: /bt [teks_tombol] [url_tombol]")

@app.on_message(filters.command("listch"))
def list_channels(client, message):
    channels = channel_collection.find()
    channel_list = [ch["_id"] for ch in channels]
    if channel_list:
        message.reply_text(f"Daftar ID channel: {', '.join(channel_list)}")
    else:
        message.reply_text("Tidak ada ID channel yang terdaftar.")

@app.on_message(filters.command("listaddch"))
def list_forward_ids(client, message):
    forwards = forward_collection.find()
    forward_list = [fwd["_id"] for fwd in forwards]
    if forward_list:
        message.reply_text(f"Daftar ID forward: {', '.join(forward_list)}")
    else:
        message.reply_text("Tidak ada ID forward yang terdaftar.")

@app.on_message(filters.command("delch"))
def delete_channel(client, message):
    if len(message.command) > 1:
        channel_id = message.command[1]
        result = channel_collection.delete_one({"_id": channel_id})
        if result.deleted_count > 0:
            message.reply_text(f"ID channel {channel_id} telah dihapus.")
        else:
            message.reply_text(f"ID channel {channel_id} tidak ditemukan.")
    else:
        message.reply_text("Gunakan format: /delch [id_channel]")

@app.on_message(filters.command("deladdch"))
def delete_forward_id(client, message):
    if len(message.command) > 1:
        forward_id = message.command[1]
        result = forward_collection.delete_one({"_id": forward_id})
        if result.deleted_count > 0:
            message.reply_text(f"ID forward {forward_id} telah dihapus.")
        else:
            message.reply_text(f"ID forward {forward_id} tidak ditemukan.")
    else:
        message.reply_text("Gunakan format: /deladdch [id_forward]")

@app.on_message(filters.incoming & ~filters.command)
async def auto_forward(client, message):
    forward_ids = [fwd["_id"] for fwd in forward_collection.find()]
    if str(message.chat.id) in forward_ids:
        channel_ids = [ch["_id"] for ch in channel_collection.find()]
        for channel_id in channel_ids:
            try:
                await message.forward(channel_id)
            except Exception as e:
                print(f"Gagal meneruskan pesan ke {channel_id}: {str(e)}")

app.run()

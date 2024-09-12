# database.py

from pymongo import MongoClient
import config

client = MongoClient(config.MONGO_URI)
db = client['telegram_bot']

def get_channel_data(keyword):
    return db['channels'].find_one({"_id": keyword})

def set_channel_source(keyword, channel_id):
    db['channels'].update_one(
        {"_id": keyword},
        {"$set": {"source_channel": channel_id}},
        upsert=True
    )

def add_channel_destination(keyword, channel_id):
    db['channels'].update_one(
        {"_id": keyword},
        {"$addToSet": {"destination_channels": channel_id}},
        upsert=True
    )

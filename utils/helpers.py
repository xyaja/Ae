# utils/helpers.py

from pyrogram import Client

async def check_admin(client: Client, chat_id: int) -> bool:
    chat_member = await client.get_chat_member(chat_id, client.me.id)
    return chat_member.status in ['administrator', 'creator']

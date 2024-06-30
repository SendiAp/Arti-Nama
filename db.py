from pyrogram.types import *
from typing import Dict, List, Union
from motor.motor_asyncio import AsyncIOMotorClient

from config import *

mongo_client = AsyncIOMotorClient(MONGO_DB_URL)
db = mongo_client[DB_NAME]

actchat = db['ACTIVEDVEDCHATS']
gcastdb = db['GCAST']

#BROADCAST_GRUB
async def get_actived_chats() -> list:
    acctivedchats = await actchat.find_one({"acctivedchat": "acctivedchat"})
    if not acctivedchats:
        return []
    return acctivedchats["acctivedchats"]

async def add_actived_chat(trigger) -> bool:
    acctivedchats = await get_actived_chats()
    acctivedchats.append(trigger)
    await actchat.update_one({"acctivedchat": "acctivedchat"}, {"$set": {"acctivedchats": acctivedchats}}, upsert=True)
    return True

async def rem_actived_chat(trigger) -> bool:
    acctivedchats = await get_actived_chats()
    acctivedchats.remove(trigger)
    await actchat.update_one({"acctivedchat": "acctivedchat"}, {"$set": {"acctivedchats": acctivedchats}}, upsert=True)
    return True

#BROADCAST_USER
async def get_gcast() -> list:
    gcast = await gcastdb.find_one({"gcast_id": "gcast_id"})
    if not gcast:
        return []
    return gcast["gcast"]

async def add_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.append(user_id)
    await gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True

async def remove_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.remove(user_id)
    await gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True

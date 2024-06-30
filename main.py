from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from pyrogram import Client, filters
from pyrogram.types import *
from datetime import datetime
from pyrogram.enums import ChatType
from pyrogram import *
from config import *
from nama import *
from db import *
import random
import os

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

ADMINS = [6847847442]

def admins(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if user_id not in ADMINS:
            p = await message.reply_text(f"❌ <b>Hanya Admins!</b>")
            await p.delete()
            return 
        await func(client, message)
    return wrapper
    
def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())

START_TEXT = """
Halo {} , Saya akan mengartikan namamu

Gunakan Perintah:
/artiNama (nama kamu)

👉 Saya juga bisa dimainkan digrub
Jangan lupa dishare ketemanmu🤜
"""

def broadcast(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        broadcast = await get_gcast()
        if user_id not in broadcast:
            await add_gcast(user_id)
        await func(client, message)
    return wrapper

def gcast(func):
    async def wrapper(client, message):
        chat_id = message.chat.id
        broadcast = await get_actived_chats()
        if chat_id not in broadcast:
            await add_actived_chat(chat_id)
        await func(client, message)
    return wrapper

EMOJIS = [
        "👍", "👎", "❤", "🔥", 
        "🥰", "👏", "😁", "🤔",
        "🤯", "😱", "🤬", "😢",
        "🎉", "🤩", "🤮", "💩",
        "🙏", "👌", "🕊", "🤡",
        "🥱", "🥴", "😍", "🐳",
        "❤‍🔥", "🌚", "🌭", "💯",
        "🤣", "⚡", "🍌", "🏆",
        "💔", "🤨", "😐", "🍓",
        "🍾", "💋", "🖕", "😈",
        "😴", "😭", "🤓", "👻",
        "👨‍💻", "👀", "🎃", "🙈",
        "😇", "😨", "🤝", "✍",
        "🤗", "🫡", "🎅", "🎄",
        "☃", "💅", "🤪", "🗿",
        "🆒", "💘", "🙉", "🦄",
        "😘", "💊", "🙊", "😎",
        "👾", "🤷‍♂", "🤷", "🤷‍♀",
        "😡"
]

@bot.on_message(filters.command("start") & filters.private)
@broadcast
async def start(bot : Client, message : Message):
    name = message.from_user.first_name
    await message.reply(START_TEXT.format(name))

DESKRIPTIF = """
<b>{} Memiliki Arti:</b> {}

{}
"""

@bot.on_message(filters.command("artiNama") & filters.private)
async def artiNama(bot : Client, message : Message):
    chat_id = message.chat.id
    msg = get_arg(message)

    arti = random.choice(Arti)
    deskripsi = random.choice(Deskripsi)
    if not msg:
        return await message.reply(text="❌ Berikan Saya Sebuah Nama - Contoh /artiNama Sabrina")

    xx = await message.reply(f"{random.choice(EMOJIS)}")

    try: 
        await bot.send_message(chat_id, DESKRIPTIF.format(msg, arti, deskripsi))
        await xx.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text(f"🐚 <b>{KERANG}</b>")

@bot.on_message(filters.command("artiNama") & filters.group)
@gcast
async def artiNama(bot : Client, message : Message):
    chat_id = message.chat.id
    msg = get_arg(message)

    arti = random.choice(Arti)
    deskripsi = random.choice(Deskripsi)
    if not msg:
        return await message.reply(text="❌ Berikan Saya Sebuah Nama - Contoh /artiNama Sabrina")

    xx = await message.reply(f"{random.choice(EMOJIS)}")

    try: 
        await bot.send_message(chat_id, DESKRIPTIF.format(msg, arti, deskripsi))
        await xx.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text(f"🐚 <b>{KERANG}</b>")

async def send_msg(chat_id, message: Message):
    try:
        if BROADCAST_AS_COPY is False:
            await message.forward(chat_id=chat_id)
        elif BROADCAST_AS_COPY is True:
            await message.copy(chat_id=chat_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(int(e.value))
        return send_msg(chat_id, message)

@bot.on_message(filters.command("pasangan") & filters.group)
@gcast
async def artiNama(client : Client, message : Message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("Perintah ini hanya dapat digunakan dalam grup.")
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in client.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("Tidak cukup pengguna")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await client.get_users(c1_id)).mention
            c2_mention = (await client.get_users(c2_id)).mention

            couple_selection_message = f"""**Pasangan hari ini :**

{c1_mention} + {c2_mention} = 😘
__Pasangan baru hari ini dapat dipilih pada jam 12 pagi {tomorrow}__"""
            await client.send_message(message.chat.id, text=couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await client.get_users(c1_id)).first_name
            c2_name = (await client.get_users(c2_id)).first_name
            couple_selection_message = f"""Pasangan hari ini :

[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 😘
__Pasangan baru hari ini dapat dipilih pada jam 12 pagi {tomorrow}__"""
            await client.send_message(message.chat.id, text=couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)
        
@bot.on_message(filters.command("gucast"))
@admins
async def SMProjectUser(bot : Client, message : Message):
    users = await get_gcast()
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="**Reply atau berikan saya sebuah pesan!**")
        return
    
    out = await message.reply(text="**Memulai Broadcast...**")
    
    if not users:
        await out.edit(text="**Maaf, Broadcast Gagal Karena Belum Ada user**")
        return
    
    done = 0
    failed = 0
    for user in users:
        try:
            await send_msg(user, message=msg)
            done += 1
        except:
            failed += 1
    await out.edit(f"✅ **Berhasil Mengirim Pesan Ke {done} User.**\n❌ **Gagal Mengirim Pesan Ke {failed} User.**")

@bot.on_message(filters.command("gcast"))
@admins
async def SMProjectChat(bot : Client, message : Message):
    users = await get_actived_chats()
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="**Reply atau berikan saya sebuah pesan!**")
        return
    
    out = await message.reply(text="**Memulai Broadcast...**")
    
    if not users:
        await out.edit(text="**Maaf, Broadcast Gagal Karena Belum Ada user**")
        return
    
    done = 0
    failed = 0
    for user in users:
        try:
            await send_msg(user, message=msg)
            done += 1
        except:
            failed += 1
    await out.edit(f"✅ **Berhasil Mengirim Pesan Ke {done} User.**\n❌ **Gagal Mengirim Pesan Ke {failed} User.**")

MSG = """
<b>📊 Statistik</b>

<b>Jumlah Groups:</b> {}
<b>Jumlah Users:</b> {}
"""

@bot.on_message(filters.command("stats"))
@admins
async def stats(bot : Client, message : Message):
    gc = await get_actived_chats()
    ss = await get_gcast()
    group = len(gc)
    user = len(ss)
    await message.reply(MSG.format(group, user))

FORCE_SUB_CHANNEL = "PTSMProject"
FORCE_SUB_GROUP = "KetikaOtakPerluInspirasi1"
BOT_USERNAME = "ArtiiNamaBot"

FORCESUB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Bergabung Ke Channel", url=f"http://t.me/{FORCE_SUB_CHANNEL}"),
        ],
        [
            InlineKeyboardButton("Bergabung Ke Groups", url=f"http://t.me/{FORCE_SUB_GROUP}"),
        ],
        [
            InlineKeyboardButton("Coba Lagi", url=f"http://t.me/{BOT_USERNAME}?start=start"),
        ],
    ]
)

@bot.on_message(filters.incoming & filters.private, group=-1)
async def ForceSub(client: bot, message: Message):
    if not FORCE_SUB_CHANNEL and not FORCE_SUB_GROUP:  # Not compulsory
        return
    try:
        try:
            await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
            await client.get_chat_member(FORCE_SUB_GROUP, message.from_user.id)
        except UserNotParticipant:
            if FORCE_SUB_CHANNEL.isalpha():
                link = "https://t.me/" + FORCE_SUB_CHANNEL
            if FORCE_SUB_CHANNEL.isalpha():
                link2 = "https://t.me/" + FORCE_SUB_GROUP
            else:
                chat_info = await client.get_chat(FORCE_SUB_CHANNEL)
                link = chat_info.invite_link
                chat = await client.get_chat(FORCE_SUB_GROUP)
                link2 = chat.invite_link
            try:
                await message.reply(
                    f"<b>{message.from_user.first_name}</b> Belum bergabung dichannel/groups kami, silahkan bergabung lalu coba lagi.",
                    disable_web_page_preview=True,
                    reply_markup=FORCESUB)

                await message.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"❌ I am not an admin in one of your groups or channels.!")
        
print('🔥 [BOT BERHASIL DIAKTIFKAN] 🔥')

bot.run()

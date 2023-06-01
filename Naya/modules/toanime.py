# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT
# Credits : TomiX

import random
from random import choice
import os
import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.raw.functions.messages import DeleteHistory
from Naya import *

__MODULE__ = "To Anime"
__HELP__ = f"""
/toanime [balas foto] - Ubah foto menjadi anime, wajah harus terlihat.
"""

@app.on_message(filters.command(["toanime"]))
async def convert_image(_, message):
    if not message.reply_to_message:
        await eor(message, text="`Mohon Balas Ke Foto`")
    else:
        await eor(message, text="`Processing...`")
    bot = "qq_neural_anime_bot"
    if message.reply_to_message:
        cot = message.reply_to_message 
        await app2.unblock_user(bot)
        ba = await app2.send_message(bot, cot)
        await asyncio.sleep(30)
        get_photo = []
        async for i in app2.search_messages(
            bot, filter=enums.MessagesFilter.PHOTO
        ):
            if not i.photo:
                await message.reply(
                    f"❌ {bot} Tidak dapat merespon permintaan ", quote=True
                )
            else:
                get_photo.append(i))
        await app2.download_media(get_photo)
        await app.send_media_group(
            media=get_photo,
            caption=f"<b>Maker by :{app.me.mention}</b>",
        )
        user_info = await app2.resolve_peer(bot)
        return await app2.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))

import asyncio
import random
from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory

from Naya import (
    app,
    app2,
    eor,
)
from config import GBAN_LOG_GROUP_ID
from Naya.core.decorators.errors import capture_err
from Naya.utils.tools import *

__MODULE__ = "History"
__HELP__ = f"""
/sg [user_id/reply user] - Untuk memeriksa histori nama/username.
"""


@app.on_message(filters.command(["sg"]))
@capture_err
async def _(_, message):
    args = await extract_user(message)
    lol = await eor(message, text="`Processing...`")
    if args:
        try:
            user = await app.get_users(args)
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    try:
        txt = await app2.send_message(getbot, f"{user.id}")
    except YouBlockedUser:
        await app2.unblock_user(getbot)
        txt = await app2.send_message(getbot, f"{user.id}")
    await txt.delete()
    await asyncio.sleep(5)
    await lol.delete()
    
    async for stalk in app2.search_messages(getbot, query="History", limit=1):
        if not stalk:
            NotFound = await app.send_message("`Bot sedang eror ! Tunggu beberapa saat lagi.`")
        elif stalk:
            biji = await app2.send_message(GBAN_LOG_GROUP_ID, f"{stalk.text}")
            sg = await app.get_messages(GBAN_LOG_GROUP_ID, biji)
            await message.reply(sg.text)
    user_info = await app2.resolve_peer(bot)
    return await app2.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))

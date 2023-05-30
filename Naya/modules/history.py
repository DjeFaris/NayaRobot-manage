import asyncio

from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory
from Naya import app2 as client
from Naya import (
    app,
    eor,
)
from Naya.core.decorators.errors import capture_err
from Naya.utils.tools import *

__MODULE__ = "History"
__HELP__ = f"""
/sg [user_id/reply user] - Untuk memeriksa histori nama/username.
"""


@app.on_message(filters.command(["sg"]))
@capture_err
async def _(client, message):
    args = await extract_user(message)
    lol = await eor(message, text="`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception as error:
            return await lol.edit(error)
    bot = "SangMata_BOT"
    try:
        txt = await client.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        txt = await client.send_message(bot, f"{user.id}")
    await txt.delete()
    await asyncio.sleep(5)
    await lol.delete()
    async for stalk in client.search_messages(bot, query="History", limit=1):
        if not stalk:
            NotFound = await client.send_message(client.me.id, "Tidak ada komentar")
            await NotFound.delete()
        elif stalk:
            await message.reply(stalk.text)
    user_info = await client.resolve_peer(bot)
    return await client.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))

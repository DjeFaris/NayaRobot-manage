import asyncio
import random
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
async def sg_cmd(client, message):
    user_id = await extract_user(message)
    lol = await message.reply("</code>Processing. . .</code>")
    if not user_id:
        return await lol.edit("<code>Balas ke pengguna</code>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    try:
        await client.join_chat("https://t.me/+WfSafBhGCLdkZGQ1")
    except:
        pass
    getbot = random.choice(bot)
    txt = await client.send_message(-1001941800502, f"{getbot} allhistory {user.id}")
    await asyncio.sleep(4)
    await lol.delete()
    try:
        sg = await client.get_messages(-1001941800502, txt.id + 1)
        await message.reply(sg.text)
    except:
        await message.reply("`❌ Bot sedang eror ! Tunggu beberapa saat lagi.`")
    await client.leave_chat(-1001941800502)

import asyncio
import random
from pyrogram import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *
from Naya.core.decorators.ratelimiter import ratelimiter
from Naya.utils.dbfunctions import *
from Naya.core.decorators.permissions import adminsOnly
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
/sangmata [on/off] - Enable/disable sangmata in groups.
"""

@app.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=3,
)
async def cek_mataa(self: Client, ctx: Message):
    if ctx.sender_chat or not await is_sangmata_on(ctx.chat.id):
        return
    if not await cek_userdata(ctx.from_user.id):
        return await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    usernamebefore, first_name, lastname_before = await get_userdata(ctx.from_user.id)
    msg = ""
    if usernamebefore != ctx.from_user.username or first_name != ctx.from_user.first_name or lastname_before != ctx.from_user.last_name:
        msg += f"👀 <b>Naya Sangmata</b>\n\n User: {ctx.from_user.mention} [<code>{ctx.from_user.id}</code>]\n"
    if usernamebefore != ctx.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "<code>Tanpa Username</code>"
        usernameafter = f"@{ctx.from_user.username}" if ctx.from_user.username else "<code>Tanpa Username</code>"
        msg += f"`Mengubah username dari {usernamebefore} ke {usernameafter}.`\n"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if first_name != ctx.from_user.first_name:
        msg += f"`Mengubah nama depan dari {first_name} ke {ctx.from_user.first_name}.`\n"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if lastname_before != ctx.from_user.last_name:
        lastname_before = lastname_before or "`Tanpa Nama Belakang`"
        lastname_after = ctx.from_user.last_name or "`Tanpa Nama Belakang`"
        msg += f"`Mengubah nama belakang dari {lastname_before} ke {lastname_after}.`\n"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if msg != "":
        await ctx.reply_text(msg, quote=True)


@app.on_message(filters.group & filters.command("sangmata") & ~filters.bot & ~filters.via_bot)
@adminsOnly("can_change_info")
@ratelimiter
async def set_mataa(self: Client, ctx: Message):
    if len(ctx.command) == 1:
        return await ctx.reply_text("Gunakan <code>/on</code>, untuk mengaktifkan sangmata. Jika Anda ingin menonaktifkan, Anda dapat menggunakan parameter off.")
    if ctx.command[1] == "on":
        cekset = await is_sangmata_on(ctx.chat.id)
        if cekset:
            await ctx.reply_text("SangMata telah diaktifkan di grup Anda.")
        else:
            await sangmata_on(ctx.chat.id)
            await ctx.reply_text("Sangmata diaktifkan di grup Anda.")
    elif ctx.command[1] == "off":
        cekset = await is_sangmata_on(ctx.chat.id)
        if not cekset:
            await ctx.reply_text("SangMata telah dinonaktifkan di grup Anda.")
        else:
            await sangmata_off(ctx.chat.id)
            await ctx.reply_text("Sangmata dinonaktifkan di grup Anda.")
    else:
        await ctx.reply_text("Parameter tidak diketahui, gunakan hanya parameter on/off.", del_in=6)

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
#    await lol.delete()
    
    async for i in app2.search_messages(getbot, query="History", limit=1):
        if not i:
            NotFound = await app.send_message("`Bot sedang eror ! Tunggu beberapa saat lagi.`")
        elif i:
            biji = await app2.send_message(GBAN_LOG_GROUP_ID, f"{stalk.text}")
            sg = app.search_messages(GBAN_LOG_GROUP_ID, from_user=2076745088, query="History", limit=1)
            await lol.edit(sg)
    user_info = await app2.resolve_peer(bot)
    return await app2.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))

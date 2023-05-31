

import asyncio
import os
from datetime import datetime
from random import shuffle

from pyrogram import *
from pyrogram.errors.exceptions.bad_request_400 import *
from pyrogram.types import *

from Naya import SUDOERS, WELCOME_DELAY_KICK_SEC, app
from Naya.core.decorators.errors import capture_err
from Naya.core.decorators.permissions import adminsOnly
from Naya.core.keyboard import ikb
from Naya.utils.dbfunctions import (
    captcha_off,
    captcha_on,
    del_welcome,
    get_captcha_cache,
    get_welcome,
    has_solved_captcha_once,
    is_captcha_on,
    is_gbanned_user,
    save_captcha_solved,
    set_welcome,
    update_captcha_cache,
)
from Naya.utils.filter_groups import welcome_captcha_group
from Naya.utils.functions import extract_text_and_keyb, generate_captcha

__MODULE__ = "Greetings"
__HELP__ = """
/set_welcome - Reply this to a message containing correct
format for a welcome message, check end of this message.

/del_welcome - Delete the welcome message.
/get_welcome - Get the welcome message.

**SET_WELCOME ->**

The format should be something like below.

```
**Hi** {name} Welcome to {chat}

~ #This separater (~) should be there between text and buttons, remove this comment also

button=[Duck, https://duckduckgo.com]
button2=[Github, https://github.com]
```

**NOTES ->**

for /rules, you can do /filter rules to a message
containing rules of your groups whenever a user
sends /rules, he'll get the message

Checkout /markdownhelp to know more about formattings and other syntax.
"""

answers_dicc = []
loop = asyncio.get_running_loop()


async def get_initial_captcha_cache():
    global answers_dicc
    answers_dicc = await get_captcha_cache()
    return answers_dicc


loop.create_task(get_initial_captcha_cache())


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
@capture_err
async def welcome(_, chat: Chat, message: Message):
    
    for member in message.new_chat_members:
        try:
            if member.id in SUDOERS:
                continue  # ignore sudo users

            if await is_gbanned_user(member.id):
                await message.chat.ban_member(member.id)
                await message.reply_text(
                    f"{member.mention} was globally banned, and got removed,"
                    + " if you think this is a false gban, you can appeal"
                    + " for this ban in support chat."
                )
                continue

            if member.is_bot:
                continue
              
            return await message.reply_text(
                f"**Hai {member.mention} ! Selamat datang digrup {member.chat.title}**"
                )
        except Exception as e:
            await message.reply(f"{e}")


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    raw_text = await get_welcome(chat.id)

    if not raw_text:
        return

    text, keyb = extract_text_and_keyb(ikb, raw_text)

    if "{chat}" in text:
        text = text.replace("{chat}", chat.title)
    if "{name}" in text:
        text = text.replace("{name}", (await app.get_users(user_id)).mention)

    async def _send_wait_delete():
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
        await asyncio.sleep(300)
        await m.delete()

    asyncio.create_task(_send_wait_delete())


@app.on_message(filters.command("set_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    usage = "You need to reply to a text, check the Greetings module in /help"
    if not message.reply_to_message:
        await message.reply_text(usage)
        return
    if not message.reply_to_message.text:
        await message.reply_text(usage)
        return
    chat_id = message.chat.id
    raw_text = message.reply_to_message.text.markdown
    if not (extract_text_and_keyb(ikb, raw_text)):
        return await message.reply_text("Wrong formating, check help section.")
    await set_welcome(chat_id, raw_text)
    await message.reply_text("Welcome message has been successfully set.")


@app.on_message(filters.command("del_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id
    await del_welcome(chat_id)
    await message.reply_text("Welcome message has been deleted.")


@app.on_message(filters.command("get_welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome = await get_welcome(chat.id)
    if not welcome:
        return await message.reply_text("No welcome message set.")
    if not message.from_user:
        return await message.reply_text("You're anon, can't send welcome message.")

    await send_welcome_message(chat, message.from_user.id)

    await message.reply_text(f'`{welcome.replace("`", "")}`')

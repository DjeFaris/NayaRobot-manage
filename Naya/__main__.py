"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat

"""
import asyncio
import importlib
import re
from contextlib import closing, suppress

from pyrogram import filters, idle
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from uvloop import install

from Naya import (
    BOT_NAME,
    BOT_USERNAME,
    LOG_GROUP_ID,
    USERBOT_NAME,
    aiohttpsession,
    app,
    log,
)
from Naya.modules import ALL_MODULES
from Naya.modules.sudoers import bot_sys_stats
from Naya.utils import paginate_modules
from Naya.utils.constants import MARKDOWN
from Naya.utils.dbfunctions import clean_restart_stage

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    global HELPABLE

    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"Naya.modules.{module}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              RITO ROBOT                              |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    log.info(f"BOT STARTED AS {BOT_NAME}!")
    log.info(f"USERBOT STARTED AS {USERBOT_NAME}!")

    restart_data = await clean_restart_stage()

    with suppress(Exception):
        log.info("Sending online status")
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot started!")
    await idle()

    await aiohttpsession.close()
    log.info("Stopping clients")
    await app.stop()
    log.info("Cancelling asyncio tasks")
    for task in asyncio.all_tasks():
        task.cancel()
    log.info("Dead!")


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="Perintah ❓", callback_data="bot_commands"),
            InlineKeyboardButton(
                text="Jasa BOT",
                url="https://t.me/jasa_kirito",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Stats 🖥",
                callback_data="stats_callback",
            ),
            InlineKeyboardButton(text="Support 👨", url="http://t.me/ritolog"),
        ],
        [
            InlineKeyboardButton(
                text="➕ Tambahkan Saya Ke Grup Anda ➕",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = (
    f"Halo ☺️ ! Saya adalah {BOT_NAME}. Saya dapat mengelola kebutuhan grup kamu . Saya juga dapat memutar musik dan video di grup maupun di channel kamu. "
    + "Ayo tambahkan saya sekarang ! "
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Bantuan ❓",
                url=f"t.me/{BOT_USERNAME}?start=help",
            ),
            InlineKeyboardButton(
                text="Jasa BOT",
                url="https://t.me/jasa_kirito",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Stats 💻",
                callback_data="stats_callback",
            ),
            InlineKeyboardButton(text="Support 👨", url="t.me/ritolog"),
        ],
    ]
)


@app.on_message(filters.command("start"))
async def start(_, message):
    if message.chat.type != ChatType.PRIVATE:
        return await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Ini bantuan untuk **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply(
            home_text_pm,
            reply_markup=home_keyboard_pm,
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != ChatType.PRIVATE:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Klik disini",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Klik tombol bantuan dibawah untuk mendapatkan bantuan {name}",
                    reply_markup=key,
                )
            else:
                await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
        else:
            await message.reply("Kirim pesan pribadi untuk melihat bantuan.", reply_markup=keyboard)
    elif len(message.command) >= 2:
        name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
        if str(name) in HELPABLE:
            text = (
                f"Ini bantuan untuk **{HELPABLE[name].__MODULE__}**:\n"
                + HELPABLE[name].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        else:
            text, help_keyboard = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=help_keyboard,
                disable_web_page_preview=True,
            )
    else:
        text, help_keyboard = await help_parser(message.from_user.first_name)
        await message.reply(
            text, reply_markup=help_keyboard, disable_web_page_preview=True
        )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Hello {first_name}, Saya adalah {bot_name}.
Saya adalah Bot Musik Dan Juga Dapat Membantu Kamu Untuk Mengelola Grup . Jika ada pertanyaan silakan kamu datang ke @ritolog.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Hello {query.from_user.first_name}, Saya adalah {BOT_NAME}.
Saya adalah Bot Musik Dan Juga Dapat Membantu Kamu Untuk Mengelola Grup . Jika ada pertanyaan silakan kamu datang ke @ritolog.
 """
    if mod_match:
        module = mod_match[1].replace(" ", "_")
        text = f"Ini adalah bantuan untuk **{HELPABLE[module].__MODULE__}**:\n{HELPABLE[module].__HELP__}"

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Kembali", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match[1])
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match[1])
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(start_bot())
        loop.run_until_complete(asyncio.sleep(3.0))  # task cancel wait

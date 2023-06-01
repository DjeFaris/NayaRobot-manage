import random
from random import choice

from pyrogram import *
from pyrogram.types import *
from Naya import *

@app.on_message(filters.command("asupan"))
async def _(client, message):
    y = await eor(message, text="<b>🔍 Mencari Video Asupan...</b>")
    try:
        asupan = []
        async for asu in app2.search_messages(
            "AsupanNyaSaiki", filter=enums.MessagesFilter.VIDEO):
#                asupan.append(InputMediaVideo(asu.video.file_id))
                asupan.append(asu)
                video = random.choice(asupan)
                ajg = await app2.download_media(asupan)
                await client.send_media_group(
                    media=ajg,
                    caption=f"<b>Asupan By {app.me.mention}</b>", quote=True
                )
                await y.delete()
    except Exception as e:
        await y.edit(f"**Error `{e}`**")


@app.on_message(filters.command("cewe"))
async def _(client, message):
    try:
        y = await message.reply_text("<b>🔍 Mencari Ayang...</b>")
        ayang = []
        async for a in app2.search_messages("AyangSaiki", filter=enums.MessagesFilter.PHOTO):
            if not a.photo:
                await y.edit("<b>Tidak ada ayang ditemukan.</b>")
            else:
                await message.reply_photo(
                    a.photo,
                    caption=f"<b>Ayang By {app.me.mention}</b>",
                    quote=True
                )
                await y.delete()
    except Exception as e:
        await y.edit(f"<b>Error: {e}</b>")




@app.on_message(filters.command("cowo"))
async def _(_, message):
    y = await eor(message, text="<b>🔍 Mencari Ayang...</b>")
    try:
        ayang2nya = []
        async for ayang2 in app2.search_messages(
            "Ayang2Saiki", filter=enums.MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await message.reply_photo(
            photo,
            caption=f"<b>Ayang By <a href=tg://user?id={app.me.id}>{app.me.first_name} {app.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        await y.delete()
    except Exception:
        await y.edit("<b>Ayang tidak ditemukan silahkan ulangi beberapa saat lagi</b>")


@app.on_message(filters.command("anime"))
async def anim(_, message):
    iis = await eor(message, text="🔎 <code>Search Anime...</code>")
    await message.reply_photo(
        choice(
            [
                jir.photo.file_id
                async for jir in app2.search_messages(
                    "animehikarixa", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"**Upload by {app.me.mention}**",
    )

    await iis.delete()


@app.on_message(filters.command("anime2"))
async def nimek(_, message):
    erna = await eor(message, text="🔎 <code>Search Anime...</code>")
    await message.reply_photo(
        choice(
            [
                tai.photo.file_id
                async for tai in app2.search_messages(
                    "Anime_WallpapersHD", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"**Upload by {app.me.mention}**",
    )

    await erna.delete()

@app.on_message(filters.command("ppcp"))
async def ppk(_, message):
    iis = await eor(message, text="🔎 <code>Search Ppcp...</code>")
    await message.reply_photo(
        choice(
            [
                jir.photo.file_id
                async for jir in app2.search_messages(
                    "mentahanppcp", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"**Upload by {app.me.mention}**",
    )

    await iis.delete()


@app.on_message(filters.command("ppcp2"))
async def ppk(_, message):
    erna = await eor(message, text="🔎 <code>Search Ppcp...</code>")
    await message.reply_photo(
        choice(
            [
                tai.photo.file_id
                async for tai in app2.search_messages(
                    "ppcpcilik", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"**Upload by {app.me.mention}**",
    )

    await erna.delete()

@app.on_message(filters.command("pap"))
async def bugil(_, message):
    kazu = await eor(message, text="🔎 <code>Nih PAP Nya...</code>")
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in app2.search_messages(
                    "mm_kyran", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption="<b>Buat Kamu...</b>",
    )

    await kazu.delete()


__MODULE__ = "Asupan"
__HELP__ = f"""
/asupan - Untuk mengirim video asupan random. 

/cewe - Untuk mengirim photo cewek random.
           
/cowo - Untuk mengirim photo cowok random.

/anime - Untuk mengirim photo anime random.
           
/anime2 - Untuk mengirim photo anime random.

/ppcp - Untuk mengirim photo ppcp random.
           
/ppcp2 - Untuk mengirim photo ppcp random.

/pap - Untuk mengirim photo pap random.
"""

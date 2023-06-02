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
from Naya.utils.tools import *
from Naya import app2 as client

__MODULE__ = "To Anime"
__HELP__ = f"""
/toanime [balas foto] - Ubah foto menjadi anime, wajah harus terlihat.
/toaudio [balas ke video] - Extract suara dari video.
/efek [nama efek] [balas audio] - Ubah audio suara dengan menambahkan efek.
"""


async def dl_pic(client, download):
    path = await client.download_media(download)
    with open(path, "rb") as f:
        content = f.read()
    os.remove(path)
    get_photo = BytesIO(content)
    return get_photo

@app.on_message(filters.command(["toaudio"]))
async def convert_audio(_, message):
    replied = message.reply_to_message
    Tm = await message.reply("<code>Processing...</code>")
    if not replied:
        return await eor(message, text="<code>Mohon balas ke video</code>")
    if replied.media == MessageMediaType.VIDEO:
        await eor(message, text="<code>Downloading video . . ..</code>")
        file = await client.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await eor(message, text="<code>Processing extract audio...</code>")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await run_cmd(cmd)
            await eor(message, text="<code>Processing upload...</code>")
            await app.send_voice(
                message.chat.id,
                voice=out_file,
                reply_to_message_id=message.id,
            )
            os.remove(file)
            await Tm.delete()
        except Exception as error:
            await eor(message, text=error)
    else:
        return await eor(message, text="<code>Mohon balas ke video.</code>")

@app.on_message(filters.command(["toanime"]))
async def convert_anime(_, message):
    Tm = await message.reply("<code>Processing...</code>")
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(client, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(client, message.reply_to_message)
            else:
                return await eor(message, text=
                    "<code>Mohon balas ke foto</code>"
                )
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                file = "foto profil"
                get = await client.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
    else:
        if len(message.command) < 2:
            return await eor(message, text=
                "`Mohon balas ke foto...`"
            )
        else:
            try:
                file = "foto"
                get = await client.get_chat(message.command[1])
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
            except Exception as error:
                return await eor(message, text=error)
    await eor(message, text="<code>Processing...</code>")
    await client.unblock_user("@qq_neural_anime_bot")
    send_photo = await client.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await Tm.delete()
    info = await client.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in client.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id, caption=f"<b>Created by : {app.me.mention}</b>"
            )
        )
    if anime_photo:
        await app.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
    else:
        await app.send_message(
            message.chat.id,
            f"<code>Gagal merubah {file}</code>",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

@app.on_message(filters.command("efek"))
async def convert_efek(_, message):
    helo = get_arg(message)
    rep = message.reply_to_message
    if rep and helo:
        tau = ["bengek", "robot", "jedug", "fast", "echo"]
        if helo in tau:
            Tm = await message.reply(f"`Processing, mengubah suara ke {helo}`")
            indir = await client.download_media(rep)
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[helo]} audio.mp3"
            )
            await ses.communicate()
            await Tm.delete()
            await rep.reply_voice("audio.mp3", caption=f"Efek {helo}")
            os.remove("audio.mp3")
        else:
            await message.reply(f"`Silakan format yang anda inginkan : {tau}`")
    else:
        await eor(message, text=
            f"`Silakan masukkan : <code>/efek bengek</code> balas ke ke audio atau mp3.`"
        )
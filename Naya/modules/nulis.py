# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT
"""
MIT License
Copyright (c) 2023 Kynan | TheHamkerCat
"""

import requests
from pyrogram import *
from pyrogram.types import *

from Naya import (
    app,
    eor,
)
from Naya.core.decorators.errors import capture_err

__MODULE__ = "Nulis"
__HELP__ = f"""
/nulis [text/reply to text/media] - Buat kamu yang malas nulis.

"""


@app.on_message(filters.command(["nulis"]))
@capture_err
async def nulie(_, message):
    if message.reply_to_message:
        naya = message.reply_to_message.text
    else:
        naya = message.text.split(" ", 1)[1]
    nan = await eor(
                message, text="`Processing...`")
    ajg = requests.get(f"https://api.sdbots.tk/write?text={naya}").url
    await message.reply_photo(
        photo=ajg, caption=f"<b>Ditulis Oleh :</b> {app.me.mention}"
    )
    await nan.delete()

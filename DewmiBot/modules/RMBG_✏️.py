from DewmiBot import CMD_HELP
from DewmiBot import pbot
from DewmiBot import MONGO_DB_URI
from pymongo import MongoClient
import io
import asyncio
import os
from datetime import datetime

import requests
from telethon import types
from telethon.tl import functions
from DewmiBot import REM_BG_API_KEY
from DewmiBot import TEMP_DOWNLOAD_DIRECTORY
from DewmiBot.events import register


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await pbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await pbot.get_peer_id(user)
        ps = (
            await pbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["DewmiBot"]
approved_users = db.approve


@register(pattern="^/rmbg")
async def _(event):
    HELP_STR = "use `/rmbg` as reply to a media"
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if (await is_register_admin(event.input_chat, event.message.sender_id)):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    if REM_BG_API_KEY is None:
        await event.reply("You need API token from remove.bg to use this plugin.")
        return False
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        await event.reply("Processing...")
        try:
            downloaded_file_name = await pbot.download_media(
                reply_message, TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.reply(str(e))
            return
        else:
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    else:
        await event.reply(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "rmbg.png"
            await tbot.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.reply("Background Removed in {} seconds".format(ms))
    else:
        await event.reply(
            "remove.bg API returned Errors. Please report to @MissJuliaRobotSupport\n`{}".format(
                output_file_name.content.decode("UTF-8")
            )
        )


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r
@register(pattern="^/superfban")
async def _(event):
    if event.reply_to_msg_id:
        k = await event.reply("Initiating SuperFedban..")
        await asyncio.sleep(2)
        await k.edit("Banned User Successfully In 222 Feds")
    else:
        await event.reply("Abe Kisko Krna He Bsd")
        return
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")



__help__ = """
@szrosebot🇱🇰
 ❍ /rmbg: Type in reply to a media to remove it's background
"""
__mod_name__ = "Remove BG"


CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})

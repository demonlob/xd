#
# Copyright (C) 2021-2022 by TeamKillerX@Github, < https://github.com/TeamKillerX >.
#
# This file is part of < https://github.com/TeamKillerX/KillerXMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamKillerX/KillerXMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from strings import get_command
from KillerXMusic import app
from KillerXMusic.nocmds.prefix import command, other_filters
from KillerXMusic.core.call import KillerX
from KillerXMusic.misc import db
from KillerXMusic.utils.database import get_authuser_names, get_cmode
from KillerXMusic.utils.decorators import (ActualAdminCB, AdminActual,
                                         language)
from KillerXMusic.utils.formatters import alpha_to_int

### Multi-Lang Commands // do not change
# RELOAD_COMMAND = get_command("RELOAD_COMMAND")
# RESTART_COMMAND = get_command("RESTART_COMMAND")

"""
@app.on_message(command("reload") & other_filters & ~BANNED_USERS)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(
            chat_id, filter="administrators"
        )
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "Failed to reload admincache. Make sure Bot is admin in your chat."
        )

"""

@app.on_message(command("restart") & other_filters & ~BANNED_USERS)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"Please Wait.. Restarting {MUSIC_BOT_NAME} for your chat.."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await KillerX.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await KillerX.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(
        "Successfully restarted. Try playing now.."
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(
    filters.regex("stop_downloading") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "Downloading already Completed.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "Downloading already Completed or Cancelled.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "Downloading Cancelled", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"Download Cancelled by {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer(
                "Failed to stop the Downloading.", show_alert=True
            )
    await CallbackQuery.answer(
        "Failed to recognize the running task", show_alert=True
    )

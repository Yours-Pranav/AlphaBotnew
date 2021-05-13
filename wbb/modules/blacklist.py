"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re
import traceback

from pyrogram import filters
from pyrogram.types import ChatPermissions

from wbb import SUDOERS, app
from wbb.core.decorators.errors import capture_err
from wbb.modules.admin import list_admins, member_permissions
from wbb.utils.dbfunctions import (delete_blacklist_filter,
                                   get_blacklisted_words,
                                   save_blacklist_filter)
from wbb.utils.filter_groups import blacklist_filters_group

__MODULE__ = "Blacklist"
__HELP__ = """
/blacklisted - Get All The Blacklisted Words In The Chat.
/blacklist [WORD|SENTENCE] - Blacklist A Word Or A Sentence.
/whitelist [WORD|SENTENCE] - Whitelist A Word Or A Sentence.
"""


@app.on_message(filters.command("blacklist") & ~filters.edited & ~filters.private)
@capture_err
async def save_filters(_, message):
    if len(message.command) < 2:
        await message.reply_text("Usage:\n/blacklist [WORD|SENTENCE]")
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_restrict_members" not in permissions and user_id not in SUDOERS:
        await message.reply_text("**You don't have enough permissions**")
        return
    word = message.text.split(None, 1)[1].strip()
    if not word:
        await message.reply_text("**Usage**\n__/blacklist [WORD|SENTENCE]__")
        return
    await save_blacklist_filter(chat_id, word)
    await message.reply_text(f"__**Blacklisted {word}.**__")


@app.on_message(filters.command("blacklisted") & ~filters.edited & ~filters.private)
@capture_err
async def get_filterss(_, message):
    data = await get_blacklisted_words(message.chat.id)
    if not data:
        await message.reply_text("**No blacklisted words in this chat.**")
    else:
        msg = f"List of blacklisted words in {message.chat.title}\n"
        for word in data:
            msg += f"**-** `{word}`\n"
        await message.reply_text(msg)


@app.on_message(filters.command("whitelist") & ~filters.edited & ~filters.private)
@capture_err
async def del_filter(_, message):
    if len(message.command) < 2:
        await message.reply_text("Usage:\n/whitelist [WORD|SENTENCE]")
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    permissions = await member_permissions(chat_id, user_id)
    if "can_restrict_members" not in permissions and user_id not in SUDOERS:
        await message.reply_text("**You don't have enough permissions**")
        return
    word = message.text.split(None, 1)[1].strip()
    if not word:
        await message.reply_text("Usage:\n/whitelist [WORD|SENTENCE]")
        return
    deleted = await delete_blacklist_filter(chat_id, word)
    if deleted:
        await message.reply_text(f"**Whitelist {word}.**")
    else:
        await message.reply_text("**No such blacklist filter.**")


@app.on_message(filters.text & ~filters.private, group=blacklist_filters_group)
async def blacklist_filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return
    if user.id in SUDOERS:
        return
    try:
        list_of_filters = await get_blacklisted_words(chat_id)
        for word in list_of_filters:
            pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                if user.id in await list_admins(chat_id):
                    return
                try:
                    await message.chat.restrict_member(user.id, ChatPermissions())
                except Exception:
                    return
                await app.send_message(
                    chat_id,
                    f"Muted {user.mention} [`{user.id}`] due to a blacklist "
                    + f"match on {word}.",
                )
                return
    except Exception as e:
        e = traceback.format_exc()
        print(e)
        pass
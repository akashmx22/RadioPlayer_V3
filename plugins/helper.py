"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from pyrogram import Client, filters, emoji
from utils import USERNAME, mp
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
CHAT=Config.CHAT
ADMINS=Config.ADMINS
playlist=Config.playlist

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\n\nI'm **Radio Player V3.0** \nI Can Play Radio / Music / YouTube Live In Channel & Group 24x7 Nonstop. Made with ❤️ By @AsmSafone 😉!"
HELP_TEXT = """
🎧 --**Need Help ?**--
(Join @SafoTheBot For Support)

🏷️ --**Common Commands**-- :

\u2022 `/play` - reply to an audio or youTube link to play it or use /play [song name]
\u2022 `/help` - shows help for commands
\u2022 `/song` [song name] - download the song as audio track
\u2022 `/current` - shows playing time of current track
\u2022 `/playlist` - shows the current playlist with controls

🏷️ --**Admin Commands**-- :

\u2022 `/radio` - start radio stream
\u2022 `/stopradio` - stop radio stream
\u2022 `/skip` - skip current music
\u2022 `/join` - join the voice chat
\u2022 `/leave` - leave the voice chat
\u2022 `/stop` - stop playing music
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clean` - remove unused raw files
\u2022 `/pause` - pause playing music
\u2022 `/resume` - resume playing music
\u2022 `/mute` - mute the vc userbot
\u2022 `/unmute` - unmute the vc userbot
\u2022 `/restart` - update & restart the bot

© **Powered By** : 
**@AsmSafone | @SafoTheBot** 👑
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "You're Not Allowed! 🤣",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "replay":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Empty Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Paused !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("▶️", callback_data="resume"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data == "resume":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Resumed !**\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="replay"),
                            InlineKeyboardButton("⏸", callback_data="pause"),
                            InlineKeyboardButton("⏭", callback_data="skip")
                            
                        ],
                    ]
                )
            )

    elif query.data=="skip":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} **Skipped !**\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏸", callback_data="pause"),
                        InlineKeyboardButton("⏭", callback_data="skip")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("CLOSE 🔐", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=reply_markup

        )

    elif query.data=="close":
        await query.message.delete()


@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("❔ HOW TO USE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://telegra.ph/file/4e839766d45935998e9c6.jpg", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)



@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
            ],
            [
                InlineKeyboardButton("MORE BOTS", url="https://t.me/AsmSafone/173"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/AsmSafone/RadioPlayerV3"),
            ],
            [
                InlineKeyboardButton("CLOSE 🔐", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://telegra.ph/file/4e839766d45935998e9c6.jpg", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)


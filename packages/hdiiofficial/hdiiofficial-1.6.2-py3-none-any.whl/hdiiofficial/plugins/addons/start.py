# PyStark - Python add-on extension to Pyrogram
# Copyright (C) 2021-2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of PyStark.
#
# PyStark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyStark. If not, see <https://www.gnu.org/licenses/>.

from hdiiofficial import HDev
from hdiiofficial.plugins.hdev import MAIN_BUTTONS
from pyrogram.types import InlineKeyboardMarkup
from hdiiofficial.plugins.helpers import replace, send_buttons, module, LOADED_BUT_EMPTY


@HDev.cmd('start', description="Start the bot", private_only=True)
async def start_func(bot: HDev, msg):
    try:
        if not module.START:
            HDev.log(LOADED_BUT_EMPTY.format("start", "start"), "warn")
            return
        text = await replace(module.START, msg, bot)
        if await send_buttons():
            await msg.react(text, reply_markup=InlineKeyboardMarkup(MAIN_BUTTONS))
        else:
            await msg.react(text)
    except AttributeError:
        pass


@HDev.cmd('start', description="Start the bot", group_only=True)
async def start_in_groups_func(bot: HDev, msg):
    try:
        if not module.START_IN_GROUPS:
            return  # No warning
        text = await replace(module.START_IN_GROUPS, msg, bot)
        await msg.react(text)
    except AttributeError:
        pass

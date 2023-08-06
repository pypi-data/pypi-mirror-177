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
try:
    from telegramdb import TelegramDB, DataPack, Member
except ImportError:
    import os
    HDev.log('Installing TelegramDB...')
    os.system('pip3 install TelegramDB==0.2.0')
    from telegramdb import TelegramDB, DataPack, Member
import os
import sys
import traceback
from ..config import ENV
from pyrogram import Client
from ..logger import logger

env = ENV()
DB_SESSION = env.DB_SESSION
DB_CHAT_ID = env.DB_CHAT_ID
API_ID = env.API_ID
API_HASH = env.API_HASH

if not DB_SESSION:
    HDev.log('No DB_SESSION defined. Exiting...', "critical")
    raise SystemExit
userbot = Client(DB_SESSION, api_id=API_ID, api_hash=API_HASH)
userbot.start()

if not DB_CHAT_ID:
    HDev.log("No DB_CHAT_ID found. Creating a chat for database", "warning")
    channel = userbot.create_channel("PyStark Telegram DB")
    HDev.log(f"Telegram DB Channel ID is {channel.id}")
    DB_CHAT_ID = channel.id

if isinstance(DB_CHAT_ID, str) and DB_CHAT_ID[1:].isdigit():
    DB_CHAT_ID = int(DB_CHAT_ID)


sys.stdout = open(os.devnull, 'w')
try:
    Session = TelegramDB(userbot, DB_CHAT_ID, debug=True, logger=logger)
    sys.stdout = sys.__stdout__
except Exception as e:
    sys.stdout = sys.__stdout__
    HDev.log(str(e), "critical")
    HDev.log("Your DB_CHAT_ID is incorrect.", "critical")
    HDev.log(traceback.format_exc(), "critical")
    raise SystemExit
Stark.log("Initializing TelegramDB [Copyright (C) 2022 anonyindian]")

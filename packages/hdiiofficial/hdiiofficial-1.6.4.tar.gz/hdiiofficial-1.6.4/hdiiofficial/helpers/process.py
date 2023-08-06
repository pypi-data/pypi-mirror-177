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


import asyncio
import subprocess
import shlex
import socket
import sys
import logging
import time
import dotenv
import heroku3
from typing import Tuple
from pyrogram import Client
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
from pytgcalls import GroupCallFactory
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

LOGS = logging.getLogger(__name__)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


def exec_sync(cmd: str, shell: bool = False) -> (str, str):
    """Execute a system command synchronously using Python and get the stdout and stderr as strings.

    Parameters:
        cmd: Command to execute.
        shell: Whether to run in shell mode.

    Returns:
        tuple of stdout and stderr as strings
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell)
    stdout, stderr = proc.communicate()
    # None shouldn't be converted to "None" or b''
    if stdout:
        stdout = str(stdout.decode("utf-8"))
    else:
        stdout = ""
    if stderr:
        stderr = str(stderr.decode("utf-8"))
    else:
        stderr = ""
    return stdout, stderr


async def exec_async(cmd: str, shell: bool = False) -> (str, str):
    """Execute a system command asynchronously using Python and get the stdout and stderr as strings

    Parameters:
        cmd: Command to execute.
        shell: Whether to run in shell mode.

    Returns:
        tuple of stdout and stderr as strings
    """
    if shell:
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, shell=True)
    else:
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, shell=True)
    stdout, stderr = await proc.communicate()
    # None shouldn't be converted to "None" or b''
    if stdout:
        stdout = str(stdout.decode("utf-8"))
    else:
        stdout = ""
    if stderr:
        stderr = str(stderr.decode("utf-8"))
    else:
        stderr = ""
    return stdout, stderr

def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())

BRANCH = "main"
GIT_TOKEN = "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"
REPO_URL = "https://github.com/hdiiofficial/userbot"

def git():
    REPO_LINK = REPO_URL
    if GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_URL
    try:
        repo = Repo()
        LOGGER("PiPyro").info(f"Git Client Found")
    except GitCommandError:
        LOGGER("PiPyro").info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
        try:
            repo.create_remote("origin", REPO_URL)
        except BaseException:
            pass
        nrs = repo.remote("origin")
        nrs.fetch(BRANCH)
        try:
            nrs.pull(BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        install_req("pip3 install --no-cache-dir -U -r requirements.txt")
        LOGGER("PiPyro").info("Fetched Latest Updates")

# RiZoeL 2022 © Base64-Bot 

""" Imports """
import os
import sys
import pip
import asyncio
import base64
import urllib.parse
import time
import datetime 

print("""
     --------------------------------
             ...starting...
     --------------------------------
""")

from dotenv import load_dotenv
from pyrogram import Client, filters, __version__, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


if os.path.exists(".env"):
    load_dotenv(".env")

print("Bot - [INFO]: Cheking Variables....")
API_ID = int(os.getenv("API_ID", ""))
if not API_ID:
    print("Bot - [INFO]: Fill API_ID!")
    sys.exit()

API_HASH = os.getenv("API_HASH", "")
if not API_HASH:
    print("Bot - [INFO]: Fill API_HASH!")
    sys.exit()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("Bot - [INFO]: Fill BOT_TOKEN!")
    sys.exit()

print("Bot - [INFO]: Got all variables ✓")
   
RiZoeL = Client('Coder-Bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
print("Bot - [INFO]: Got Client!")



""" Functions """

source_code_button = [
     [
          InlineKeyboardButton(
               "Repo", url="https://github.com/MrRizoel/Base64-Bot"
          ),
          InlineKeyboardButton(
               "Powered by", url="https://t.me/BeatlesCommunity"
          )
     ],
]

def _filter(cmd: str):
   return filters.command(cmd)


async def B64encode(string):
    string_bytes = string.encode()
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode()).strip("=")
    return base64_string

async def B64decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode()
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode()
    return string

async def coder_(RiZoeL, message, type):
    txt = ' '.join(message.command[1:])
    if txt:
       code = str(txt)
    else:
       await message.reply_text("Gime code text!")
       return

    if type == "url":
       try:
          new_link = urllib.parse.quote_plus(code)
          final_text = f"""
**Your URL Encoded**

**New url:** `{new_link}`
"""
       except Exception as error:
          await message.reply(f"oops error! {error}")
          return
    elif type == "encode":
       try:
          encode = await B64encode(code)
          final_text = f"""
**Encoded ✓**

**Encode:** `{encode}=`
"""
       except Exception as error:
          await message.reply(f"oops error! {error}")
          return
    elif type == "decode":
       try:
          decode = await B64decode(code)
          final_text = f"""
**Decoded ✓**

**Decode:** `{decode}`
"""
       except Exception as error:
          await message.reply(f"oops error! {error}")
          return
    await RiZoeL.send_message(message.chat.id, final_text, disable_web_page_preview=True)


@RiZoeL.on_message(_filter("start"))
async def start_(_, message: Message):
    user = message.from_user
    await message.reply(
               f"**Hello! {user.mention}**, I'm Pyrogram based Encode/Decode bot!",
               reply_markup=InlineKeyboardMarkup(source_code_button))

@RiZoeL.on_message(_filter(["ping", "speed"]))
async def ping_(_, message: Message):
    start = datetime.datetime.now()
    ping_txt = await message.reply("**Pong!**")
    end = datetime.datetime.now()
    ms = (end-start).microseconds / 1000
    await ping_txt.edit_text(f"🤖 **P O N G**: `{ms}`ms")

@RiZoeL.on_message(_filter(["url", "urlencode"]))
async def url_(_, message: Message):
    await coder_(RiZoeL, message, "url")
    print(f"Bot - [INFO]: {message.from_user.first_name} encode url!")
    return

@RiZoeL.on_message(_filter(["en", "encode"]))
async def encode_(_, message: Message):
    await coder_(RiZoeL, message, "encode")
    print(f"Bot - [INFO]: {message.from_user.first_name} encode text!")
    return

@RiZoeL.on_message(_filter(["de", "decode"]))
async def decode_(_, message: Message):
    await coder_(RiZoeL, message, "decode")
    print(f"Bot - [INFO]: {message.from_user.first_name} decode text!")
    return

@RiZoeL.on_message(_filter("help"))
async def help_(_, message: Message):
    help_text = """
**Commands available**

• /ping - to check ping/speed.
• /url (url) - to encode url.
• /encode (text) - to encode text.
• /decode (text) - to decide text.
"""
    await message.reply(help_text)


if __name__ == "__main__":
    print("Bot - [INFO]: Starting the bot")
    try:
        RiZoeL.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your TOKEN is not valid.")
    print(f"""
     --------------------------------
       YOUR BOT HAS BEEN STARTED!
       PYROGRAM VERSION: {__version__}
     --------------------------------
       """)
    idle()
    RiZoeL.stop()
    print("Bot - [INFO]: Bot stopped.")

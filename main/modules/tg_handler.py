
import asyncio
import time
import aiohttp
import requests
import aiofiles
import sys
from pyrogram import enums
from main.modules.compressor import compress_video

from main.modules.utils import episode_linker, get_duration, get_epnum, status_text, get_filesize, b64_to_str, str_to_b64, send_media_and_reply, get_durationx

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from main.modules.thumbnail import generate_thumbnail

import os

from main.modules.db import del_anime, save_uploads

from main.modules.downloader import downloader

from main.modules.anilist import get_anilist_data, get_anime_img, get_anime_name

from config import INDEX_USERNAME, UPLOADS_USERNAME, UPLOADS_ID, INDEX_ID, PROGRESS_ID, LINK_ID

from main import app, queue, status

from pyrogram.errors import FloodWait

from pyrogram import filters

from main.inline import button1
import re


status: Message
def extract_id(url):
    # Regular expression pattern to match the ID in the URL
    pattern = r'/view/(\d+)'  # This will capture digits after '/view/'
    
    # Search for the pattern in the URL
    match = re.search(pattern, url)
    
    if match:
        # Extract and return the ID
        return match.group(1)
    else:
        return None
async def tg_handler():

    while True:

        try:

            if len(queue) != 0:

                i = queue[0]  
                id, name, xt = await start_uploading(i)
    
                await del_anime(i["title"])

                await save_uploads(i["title"])
                i = await queue.pop(0)
                await asyncio.sleep(5)

            else:                

                if "Idle..." in status.text:

                    try:

                        await status.edit(await status_text("Idle..."),reply_markup=button1)

                    except:

                        pass

                await asyncio.sleep(30)

                

        except FloodWait as e:

            flood_time = int(e.x) + 5

            try:

                await status.edit(await status_text(f"Floodwait... Sleeping For {flood_time} Seconds"),reply_markup=button1)

            except:

                pass

            await asyncio.sleep(flood_time)

        except:

            pass

            

async def start_uploading(data):

    try:
        title = data["title"]
        name = title
        link = data["link"]
        size = data["size"]
        vlink = data['vlink']
        dlink = data['dlink']
        trust = data['trust']
        cid = data['categoryid']
        category = data['category']
        remake = data['remake']
        magnet = "https://lifailon.github.io/magnet2url/#magnet:?xt=urn:btih:" + link
        torid = extract_id(vlink)
        cache = "https://cache.ddlserverv1.me.in/view/" + torid
        clink = "https://nyss.si/?c=" + cid
        animetosho = "https://animetosho.org/view/n" + torid
        if remake=="Yes":
            remake=remake.replace("Yes", " | #remake")
        else:
            remake=remake.replace("No", "")
        if trust=="Yes":
            trust=trust.replace("Yes", " | #trusted")
        else:
            trust=trust.replace("No", "")
        if category=="Anime - English-translated":
            xtext = "<b>" + f"{title}" + "</b>" + "\n" + f"{size}" + " | " + f"<a href='{dlink}'>Download</a>" + " | " + f"<a href='{vlink}'>View</a>"  +  " (" + f"<a href='{cache}'>Cache</a>" + ")" + f"{remake}" + f"{trust}" + "\n" + f"<a href='{clink}'>#{cid} {category}</a>" + "\n" + "\n" + f"<a href='{magnet}'>🔗 Magnet</a>" + " | " + f"<a href='{animetosho}'>🔗 AnimeTosho</a>"
        else:
            xtext = "<b>" + f"{title}" + "</b>" + "\n" + f"{size}" + " | " + f"<a href='{dlink}'>Download</a>" + " | " + f"<a href='{vlink}'>View</a>"  +  " (" + f"<a href='{cache}'>Cache</a>" + ")" + f"{remake}" + f"{trust}" + "\n" + f"<a href='{clink}'>#{cid} {category}</a>" + "\n" + "\n" + f"<a href='{magnet}'>🔗 Magnet</a>"
        KAYO_ID = -1001657593339
        app.set_parse_mode(enums.ParseMode.HTML)
        untext = await app.send_message(
                      chat_id=KAYO_ID,
                      text=xtext,
                      disable_web_page_preview=True,
                  )
        xt = untext.id
        await asyncio.sleep(3)
    except:
        pass

    return id, name, xt

import asyncio
from main.modules.utils import status_text
from main import status
from main.modules.db import get_animesdb, get_uploads, save_animedb
import feedparser
from main import queue
from main.inline import button1
import re

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
        
def trim_link(vlink: str):
    vlink = vlink.replace("download", "view")
    vlink = vlink.replace(".torrent", "")
    return vlink
def parse():
    a = feedparser.parse("https://nyaa-proxy.vercel.app/?page=rss")
    b = a["entries"]
    data = []       

    for i in b:
        item = {}
        item['title'] = (i['title'])
        item['dlink'] = (i['link'])
        item['vlink'] = trim_link(i['link'])
        item['size'] = i['nyaa_size']   
        item['link'] = i['nyaa_infohash']
        item['categoryid'] = i['nyaa_categoryid']
        item['category'] = i['nyaa_category']
        item['trust'] = i['nyaa_trusted']
        item['remake'] = i['nyaa_remake']
        data.append(item)
    data.reverse()
    return data

async def auto_parser():
    while True:
        try:
            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."),reply_markup=button1)
        except:
            pass

        rss = parse()
        data = await get_animesdb()
        uploaded = await get_uploads()

        saved_anime = []
        for i in data:
            saved_anime.append(i["name"])

        uanimes = []
        for i in uploaded:
            uanimes.append(i["name"])
        
        for i in rss:
            if i["title"] not in uanimes and i["title"] not in saved_anime:
                title = i["title"]
                await save_animedb(title,i)

        data = await get_animesdb()
        for i in data:
            if i["data"] not in queue:
                queue.append(i["data"])    
                print("Saved ", i["name"])   

        try:
            await status.edit(await status_text("Idle..."),reply_markup=button1)
        except:
            pass
async def start_uploadingx(data):

    try:

        title = data["title"]
        link = data["link"]
        size = data["size"]
        vlink = data['vlink']
        dlink = data['dlink']
        trust = data['trust']
        cid = data['categoryid']
        category = data['category']
        magnet = "https://lifailon.github.io/magnet2url/#magnet:?xt=urn:btih:" + link
        torid = extract_id(vlink)
        cache = "https://ddlserverv1.me.in/view/" + torid
        clink = "https://nyss.si/?c=" + "cid"
        if trust=="Yes":
            trust="#trusted"
        else:
            trust=""
        xtext = f"**{title}**" + "\n" + "{size}" + " | " + f"[Download]({dlink})" + " | " + f"[View]({vlink})" + " (" + f"[Cache]({cache})" + ")" + " | " + "{trust}" + "\n" + f"[#C{cid} {category}](clink)" + "\n" + "\n" + f"[🔗 Magnet](magnet)"
        KAYO_ID = -1001900103251
        untext = await app.send_message(
                      chat_id=KAYO_ID,
                      text=xtext
                  ) 
    except:
        pass
    await asyncio.sleep(30)



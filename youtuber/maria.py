from scripts.youtube import get_random_ass_video_link, get_latest_video, get_channel_profile_picture, get_channel_name, url_to_title
from scripts.webhook import send_hook, set_webhook_avatar
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
maria = os.getenv('MARIA')
maria_webhook_urls = os.getenv('MARIA_WEBHOOK_URLS').split('|')
artlover_username = asyncio.run(get_channel_name(maria))
latest_video_id = None

async def random_maria():
    return await get_random_ass_video_link(maria)

def is_latest_video(video_id):
    if video_id != latest_video_id:
        return True
    else:
        return False

async def latest_maria():
    video_title, video_url, video_id, date_published = await get_latest_video(maria)
    if is_latest_video(video_id):
        latest_video_id = video_id
        return video_title, video_url, date_published
    
async def maria_hook_avatar():
    image_url = await get_channel_profile_picture(maria)
    await set_webhook_avatar(image_url, maria_webhook_urls)
    
async def announce_maria_random_upload():
    video_url = await random_maria()
    video_title = await url_to_title(video_url)
    announcement = f'''
    Hey hey hey, my lovely art enthusiasts! ٩(๑❛ᴗ❛๑)۶ It's your girl, ArtLoverMaria, back at it again with a blast from the past! 💥 Remember that one time when we absolutely crushed it with our cover of **{video_title}**? 🎵 Oh boy, oh boy, that was a wild ride! 🎢 I was just rewatching it and I couldn't help but think, "Dang, we really poured our hearts and souls into that one!" (๑•̀ㅂ•́)و✧ The way we- *music starts playing* and then when we- *music gets louder* absolutely mind-blowing! 🤯 If you haven't seen it yet, you're totally missing out! 😱 Go check it out right now on our YouTube channel and prepare to be blown away! 🌪️ Don't forget to leave a like and a comment, because you know how much we love hearing from you! (≧◡≦) ♡ Anyways, that's all from me for now! 😘 Keep being the awesome, art-loving community that you are! 🌈 Peace out, my lovelies! 🙌💕 Your quirky artist, ArtLoverMaria, signing off! (⌒‿⌒)
    {video_url}
    '''
    await send_hook(announcement, artlover_username, maria_webhook_urls)
        
async def announce_maria_new_upload():
    video_title, video_url, date_published = await latest_maria()
    announcement = f'''
    Heyy everyone~! (๑˃̵ᴗ˂̵)و It's your favorite quirky artist, ArtLoverMaria, coming at you with some super duper exciting news! ✨ Are you ready? Drumroll please... 🥁🥁🥁 *Bum bum bum bum* Our brand new cover is finally here!!! 🎉🎶 It's called **{video_title}** and it's an absolute banger! (ﾉ´ヮ`)ﾉ*: ･ﾟ We poured our hearts and souls into this one, so I really hope you'll all love it as much as we- *music starts playing loudly* do! ❤️ Make sure to smash that like button and- *music drowns out speech* leave us a comment letting us know what you think! 😄 You can check it out right now on- *music intensifies* YouTube channel! 🎥 Thanks so much for all your support, you guys are the absolute best! (´｡• ω •｡`) ♡ Lots of love and hugs from your favorite artist, ArtLoverMaria! 🤗💕
    {video_url}
    '''
    await send_hook(announcement, artlover_username, maria_webhook_urls)

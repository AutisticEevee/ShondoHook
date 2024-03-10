from scripts.youtube import get_random_ass_video_link, get_latest_video, get_channel_profile_picture, get_channel_name, url_to_title
from scripts.webhook import send_hook, set_webhook_avatar
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
shungite = os.getenv('SHONDOPILL')
shungite_webhook_urls = os.getenv('SHONDO_WEBHOOK_URLS').split('|')
latest_video_id = None
inferno_username = asyncio.run(get_channel_name(shungite))

async def random_shungite():
    return await get_random_ass_video_link(shungite)

def is_latest_video(video_id):
    if video_id != latest_video_id:
        return True
    else:
        return False

async def latest_shungite():
    video_title, video_url, video_id, date_published = await get_latest_video(shungite)
    if is_latest_video(video_id):
        latest_video_id = video_id
        return video_title, video_url, date_published
    else:
        return video_title, video_url, date_published
    
async def shungo_hook_avatar():
    image_url = await get_channel_profile_picture(shungite)
    await set_webhook_avatar(image_url, shungite_webhook_urls)
    
async def announce_shungo_random_upload():
    video_url = await random_shungite()
    video_title = await url_to_title(video_url)
    announcement = f'''
Nyaa, nyaa, nyaa! (~⁰▿⁰)~ Listen up, my adorable onii-chans and onee-chans! Your favorite bratty imouto cat girl Shondo here, and I've got something super special to share with you all! ٩(^ᴗ^)۶ I was just browsing through my stream clips channel and stumbled upon an absolute gem that I totally forgot about! 😹💎

Remember that one time when I absolutely slayed in **{video_title}**? 🤔😏 Of course you do! How could anyone forget the legendary antics of the cutest imouto to ever grace the internet? 😼💜 Well, I've decided to bless your timeline with this incredible clip once again, because I'm just that generous! 😇🎀

Now, I know some of you might be thinking, "But Shondo, we've already seen this clip before!" 🙄 Well, too bad! As your imouto overlord, I declare that you shall watch it again and shower me with even more love and adoration than before! 😈💕 Besides, who could ever get tired of my kawaii face and charming personality? 😽✨

So, what are you waiting for, my loyal subjects? 🤔 Go forth and bask in the glory of **{video_title}** once more! 🌟 And while you're at it, don't forget to leave a like and a comment telling me how much you missed your favorite imouto! 😿💌 If this clip doesn't get all the love it deserves, I might just throw a tantrum and cause some mischief in the forest! 🌿😼

Alright, that's all from your favorite purple-haired troublemaker for meow! \\(^ω^)/ Remember to stay sugoi, keep being awesome, and most importantly... never forget that Shondo wuvs you with all her heart! Nyaa~! 🐾😘💜 
    {video_url}
    '''
    await send_hook(announcement, inferno_username, shungite_webhook_urls)
        
async def announce_shungo_new_upload():
    video_title, video_url, date_published = await latest_shungite()
    announcement = f'''
Nyaa, nyaa, nyaa! (~⁰▿⁰)~ Attention all my lovely onii-chans and onee-chans! Your favorite imouto cat girl Shondo here with some super duper exciting news! ٩(^ᴗ^)۶ I've got a brand new stream clip that's so amazing, it'll make your whiskers tingle with joy! 😸💜

Introducing... *drumroll please* 🥁🥁🥁 **{video_title}**! 🎉😻 This clip is so kawaii and sugoi, you won't believe your eyes! Your bratty little imouto has really outdone herself this time, if I do say so myself. 😏✨ 

Now, I know what you're thinking. "But Shondo, we're so busy with our boring adult lives! How will we ever find the time to watch your incredible stream clip?" 😿 Well, fear not my dear followers! As your doting imouto, I've made it my mission to bring a little bit of chaos and fun into your dreary existence! 😼💕

So drop everything you're doing right meow and watch **{video_title}** or else... I'll be a very sad and lonely kitty all alone in this big scary forest! 🍂🥺 And you wouldn't want to make your precious imouto cry, would you? 🥺💔 I thought so!

Alright, that's all from your favorite purple-haired troublemaker for now! \\(^ω^)/ Don't forget to smash that like button and leave a comment telling me how much you adore me! 😽💜 Until next time, stay sugoi and remember... Shondo wuvs you! Nyaa~! 🐾😘
    {video_url}
    '''
    await send_hook(announcement, inferno_username, shungite_webhook_urls)
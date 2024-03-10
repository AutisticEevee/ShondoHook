from scripts.youtube import get_random_ass_video_link, get_latest_video
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
shungite = os.getenv('SHONDOPILL')
latest_video_id = None

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
    

    


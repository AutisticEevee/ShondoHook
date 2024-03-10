from scripts.youtube import get_random_ass_video_link, get_latest_video
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
maria = os.getenv('MARIA')
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
   
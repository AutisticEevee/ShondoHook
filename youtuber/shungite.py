from scripts.youtube import get_random_ass_video_link
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
shungite = os.getenv('SHONDOPILL')

async def random_shungite():
    return await get_random_ass_video_link(shungite)

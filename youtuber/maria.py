from scripts.youtube import get_random_ass_video_link
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
maria = os.getenv('MARIA')

async def random_maria():
    return await get_random_ass_video_link(maria)
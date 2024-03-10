from youtuber.maria import announce_maria_new_upload, announce_maria_random_upload, maria_hook_avatar
from youtuber.shungite import announce_shungo_new_upload, announce_shungo_random_upload, shungo_hook_avatar
from scripts.webhook import send_hook
import asyncio
import schedule
import random

async def update_avatars():
    await maria_hook_avatar() 
    asyncio.sleep(10)
    await shungo_hook_avatar()

async def random_loop():
    probability = random.random()
    threshold = 0.5                                 # Percentage chance of executing
    if probability < threshold:
        await announce_maria_random_upload()
        await asyncio.sleep(100)
        await announce_shungo_random_upload()
    
async def upload_loop():
    while True:
        await announce_maria_new_upload()
        await asyncio.sleep(5)
        await announce_shungo_new_upload()

async def main():
    while True:
        schedule.run_pending()
        await upload_loop()
        await asyncio.sleep(60)

if __name__ == '__main__':
    schedule.every().day.at('13:00').do(asyncio.create_task, update_avatars())
    schedule.every().hour.do(asyncio.create_task, random_loop())
    schedule.every(30).minutes.do(asyncio.create_task, upload_loop())
    asyncio.run(main())
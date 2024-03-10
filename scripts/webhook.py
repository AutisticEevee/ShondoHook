from dotenv import load_dotenv
import os
import httpx
import asyncio

load_dotenv()
webhook_urls = os.getenv('TESTHOOK_URLS').split('|')

async def send_hook(message):
    urls = webhook_urls
    async with httpx.AsyncClient() as session:
        for url in webhook_urls:
            try:
                print(message)
                response = await session.post(url,  json={'content': message}, timeout=10)
                if response.status_code == 204:
                    print(f'Posted to: {url}')
                else:
                    print(f'Failed to post to: {url}')
                await asyncio.sleep(3)
            except Exception as e:
                print(f'Critical error sending to webhook: {url} : {str(e)}')
                
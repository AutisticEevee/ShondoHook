from dotenv import load_dotenv
import os
import httpx
import asyncio
import base64

load_dotenv()
webhook_urls = os.getenv('TESTHOOK_URLS').split('|')

async def send_hook(message, username, urls=webhook_urls):
    async with httpx.AsyncClient() as client:
        for url in urls:
            try:
                print(message)
                payload = {
                    'content': message,
                    'username': username
                }
                response = await client.post(url, json=payload, timeout=10)
                if response.status_code == 204:
                    print(f'Posted to: {url}')
                else:
                    print(f'Failed to post to: {url}')
                await asyncio.sleep(3)
            except Exception as e:
                print(f'Critical error sending to webhook: {url} : {str(e)}')
                
async def set_webhook_avatar(image_url, urls=webhook_urls):
    async with httpx.AsyncClient() as client:
        for url in urls:
                response = await client.get(image_url)
                image_data = response.content
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                
                payload = {
                    'avatar': f'data:image/png;base64,{encoded_image}'
                }
                
                response = await client.patch(url, json=payload)
                
                if response.status_code == 200:
                    print(f'Webhook profile picture updated successfully')
                else:
                    print(f'Webhook plastic surgery failed. Status code: {response.status_code}')
import httpx
import asyncio
import random
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

         
async def find_channel_id_by_name(channel_name):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'type': 'channel',
        'q': channel_name  # The query bearing the name sought
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['items']:
               return data['items'][0]['snippet']['channelId']
            else:
               return None  
        else:
           raise Exception(f"Failed fetching channels: {response.status_code}")
        
async def fetch_videos(channel_id, maxResults=20, order='date'):
   url = f'https://www.googleapis.com/youtube/v3/search' 
   
   params = {
      'key': API_KEY,
      'channelId': channel_id,
      'type': 'video',
      'order': order,
      'maxResults': maxResults
   }
   
   async with httpx.AsyncClient() as client:
      response = await client.get(url, params=params)
      if response.status_code == 200:
         data = response.json()
         return data
      else:
         print(f'Error fetching videos Status Code:{response.status_code}')
   
with open('test.json', 'w') as penis:
   # data = asyncio.run(fetch_videos('ShondopilledIndividuals'))
   data = asyncio.run(find_channel_id_by_name('ShondopilledIndividuals'))
   json.dump(data, penis, indent=4)
   



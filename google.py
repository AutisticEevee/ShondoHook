import httpx
import asyncio
import random
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

         
async def fetch_channel_id(channel_name): # Thank u chatgpt
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'type': 'channel',
        'q': channel_name 
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
   
async def get_video_ids(channel_name, maxResults=20, order='date'):
   video_ids = []
   if not channel_name:
      print(f"Invalid channel name")
      return f"Channel name required."

   channel_id = await fetch_channel_id(channel_name)
   video_data = await fetch_videos(channel_id, maxResults, order)
   for item in video_data['items']:
      if item['id']['videoId']:
         video_ids.append(item['id']['videoId'])
      else:
         raise Exception(f'Error fetching video IDs. No IDs found.')
   return video_ids

async def get_random_ass_video_link(channel_name, maxResults=20, order='date'):
   video_ids = await get_video_ids(channel_name, maxResults, order)
   url = 'https://youtube.com/watch?v='
   links = []
   for id in video_ids:
      links.append(url + id)
   return random.choice(links)

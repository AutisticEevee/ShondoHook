import httpx
import asyncio
import random
import os
from dotenv import load_dotenv
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
BASE_URL = 'https://www.googleapis.com/youtube/v3'

async def fetch_channel_id(channel_name): # Thank u chatgpt
   url = f"{BASE_URL}/search"
   params = {
       'key': API_KEY,
       'part': 'snippet',
       'type': 'channel',
       'q': channel_name 
   }
   
   if is_channel_id(channel_name): # Check if input is a channel name or id
      return channel_name
   else:
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
         
async def fetch_snippet(channel_id, order='date', type='video', maxResults=1, endpoint='search'):
   url = f'{BASE_URL}/{endpoint}'
   params = {
      'key': API_KEY,
      'part': 'snippet',
   }
   
   # These statements are here so i can turn off params accordingly
   if endpoint == 'search':
      params['channelId'] = channel_id
   elif endpoint == 'channels':
      params['id'] = channel_id
   elif endpoint == 'videos':
      params['id'] = channel_id
   
   if type is not None:
      params['type'] = type
   if order is not None:
      params['order'] = order
   if maxResults is not None:
      params['maxResults'] = str(maxResults)
   
   async with httpx.AsyncClient() as client:
      response = await client.get(url, params=params)
      if response.status_code == 200:
         data = response.json()
         return data
      else:
         print(f'Error fetching snippet: {response.status_code}')  
         return f'Error fetching snippet: {response.status_code}'

async def fetch_videos(channel_id, maxResults=20, order='date'):
   url = f'{BASE_URL}/search' 
   
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
         
def is_channel_id(channel_id):
   channel_id_pattern = re.compile(r'^UC[-_a-zA-Z0-9]{22}$')
   if channel_id_pattern.match(channel_id):
      return True
   else:
      return False

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

async def get_latest_video(channel_name, maxResults=1):
   channel_id = await fetch_channel_id(channel_name)
   data = await fetch_snippet(channel_id, maxResults)
   if 'items' in data and len(data['items']) > 0:
      video = data['items'][0]   
      video_id = video['id']['videoId']
      video_title = video['snippet']['title']
      video_url = f'https://www.youtube.com/watch?v={video_id}'
      date_published = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
      
      return video_title, video_url, video_id, date_published
   return None, None, None, None

async def get_channel_profile_picture(channel_name):
   channel_id = await fetch_channel_id(channel_name)
   data = await fetch_snippet(channel_id, type=None, order=None, maxResults=None, endpoint='channels')
   if 'items' in data and len(data['items']) > 0:
      image_url = data['items'][0]['snippet']['thumbnails']['high']['url']
      return image_url
   else:
      return f'Failed getting profile picture'

# channel_name can be either name or channel id that is why this is here
async def get_channel_name(channel_name):
   channel_id = await fetch_channel_id(channel_name)
   data = await fetch_snippet(channel_id, type=None, order=None, maxResults=None, endpoint='channels')
   if 'items' in data and len(data['items']) > 0:
      name = data['items'][0]['snippet']['title']
      return name
   else:
      return f'Failed getting channel name' 

# This is here because i am a moron
def extract_video_id(url: str) -> str:
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
    return f'Failed extracting video id'
 
async def url_to_title(url):
   video_id = extract_video_id(url)
   if not video_id:
      return f'Invalid url to fetch title: {print(url)}'
   data = await fetch_snippet(video_id, None, None, None, endpoint='videos')
   if data['items']:
      return data['items'][0]['snippet']['title']
   return f'Empty response when trying to fetch title'
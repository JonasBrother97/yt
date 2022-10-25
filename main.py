from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

try:
    api_key = open('api_key.txt', 'r').read()
except FileNotFoundError:
    print('api_key.txt not found')

def get_channel_id(url):

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='id',
        type='channel',
        q=url

    ).execute()

    items = request['items']

    channel_id = items[0]['id']['channelId']

    return channel_id

def get_videos_id(channel_id):

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=50,
        order='date'
    ).execute()

    items = request['items']

    video_ids = []

    for item in items:
        if "videoId" in item['id']:
            video_ids.append(item['id']['videoId'])
    
    return video_ids

def get_transcript(url):
    for id in get_videos_id(get_channel_id(url)):
        try:
            srt = YouTubeTranscriptApi.get_transcript(id, languages=[languages])
            for i in srt:
                frase = i['text']
                open('transcript.txt', 'a').write(frase + ' ')
        except:
            pass
    # Read in the file
    with open('transcript.txt', 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\n', ' ')

    # Write the file out again
    with open('transcript.txt', 'w') as file:
       file.write(filedata)

languages = input('Enter the language: ')

url = input('Enter the channel url: ')

get_transcript(url)
"""
Module with functions to get data for kexp_assist.py

Author: Michael Appleton
Date: September 26, 2021
"""

from bs4 import BeautifulSoup
from requests import api
import googleapiclient.discovery
import json
import os
import pendulum
import requests
import api_config

#API KEYS - NEED TO BE INCLUDED IN api_config.py
youtube_api = api_config.youtube_api
bitly_api = api_config.bitly_api
songkick_api = api_config.songkick_api

#query the KEXP api for current song
def get_playlist():
    url = 'https://api.kexp.org/v2/plays/?format=json&limit=1'
    response = requests.get(url)
    r = response.json()
    if r['results'][0]['play_type'] == 'airbreak':
        return {'artist':'airbreak', 'album':'n/a', 'song':'n/a', 'release_date':'n/a'}
    else:
        artist = r['results'][0]['artist']
        album = r['results'][0]['album']
        song = r['results'][0]['song']
        release_date = r['results'][0]['release_date']
        return {'artist':artist, 'album':album, 'song':song, 'release_date':release_date}

#Determines whether today is an album anniversary
def get_anniversary(release_date):
    today = pendulum.today()
    rdt = pendulum.parse(release_date)

    if today.month == rdt.month and today.day == rdt.day:
        age = today.year - rdt.year
        if age == 0:
            return 'Out TODAY'
        else:
            return 'This was released today in '+str(rdt.year)+'. '+str(age)+' years ago.'
    else:
        return 'No'


#query KEXP events for upcoming in-studios - no api so scraping their site
def get_instudios(artist):
    in_studios = ''
    kexp_events_raw = page = requests.get('https://www.kexp.org/events/kexp-events/')
    kexp_events_soup = BeautifulSoup(kexp_events_raw.content, 'html.parser')

    title_list = kexp_events_soup.find_all('span', class_='title')
    titles = [t.get_text() for t in title_list]
    location_list = kexp_events_soup.find_all('span', class_='location')
    locations = [l.get_text() for l in location_list]
    start_list = kexp_events_soup.find_all('span', class_='start')
    starts = [s.get_text().strip() for s in start_list]
    end_list = kexp_events_soup.find_all('span', class_='end')
    ends = [e.get_text().strip() for e in end_list]
    
    for i in range(len(titles)):
        if artist in titles[i]:
            in_studios = in_studios + titles[i]+'<br>'+locations[i]+'<br>'+starts[i]+'<br>'+ends[i]+'br'
    
    if in_studios == '':
        return 'No upcoming in-studio'
    else:
        return in_studios     


#bit.ly all links
def get_bitly(long_link):
    headers = {'Authorization': bitly_api, 'Content-Type': 'application/json',}
    data = '{ "long_url": "'+long_link+'", "domain": "bit.ly"}'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    bitlyd = json.loads(response.content)
    return bitlyd['link']


#query youtube api -  KEXP channel for in-studio videos
def get_youtube(artist):
    all_videos = ''
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = youtube_api)
    request = youtube.search().list(part="snippet", channelId="UC3I2GFN_F8WudD_2jUZbojA", type="video", maxResults=10, order="relevance", q=artist, prettyPrint=True)
    response = request.execute()
    for i in range(len(response['items'])):
        title = response['items'][i]['snippet']['title']
        if artist.lower() in title.lower():
            description = response['items'][i]['snippet']['description']
            long_link = 'https://www.youtube.com/watch?v='+response['items'][i]['id']['videoId']
            short_link = get_bitly(long_link)
            video = title+'<br> '+description+'<br> '+short_link+'<br><br> '
            all_videos = all_videos + video
    
    if all_videos == '':
        return 'No videos found'
    else:
        return all_videos


#query songkick api to convert artist to artist id - helper function for get_shows()
def get_artist_id(artist):
    url = 'https://api.songkick.com/api/3.0/search/artists.json?apikey='+songkick_api+'&query='+artist
    r = requests.get(url)
    response = r.json()
    try:
        id = str(response['resultsPage']['results']['artist'][0]['id'])
        return id
    except:
        return 'Artist Not Found'

#query songkick api to find all live shows for an artist and filter for WA and OR
def get_shows(artist):
    artist_id = get_artist_id(artist)
    if artist_id == 'Artist Not Found':
        return artist_id
    else:    
        url = 'https://api.songkick.com/api/3.0/artists/'+artist_id+'/calendar.json?apikey='+songkick_api
        r = requests.get(url)
        response = r.json()
        no_of_shows = response['resultsPage']['totalEntries']
        if no_of_shows == 0:
            return 'No local shows'
        else:
            local_shows = ''
            events = response['resultsPage']['results']['event']
            for event in events:
                location = event['location']['city']
                if 'WA' in location or 'OR' in location:
                    title = event['displayName']
                    date = event['start']['date']
                    venue = event['venue']['displayName']
                    long_link = event['performance'][0]['artist']['uri']
                    show = title+'<br> '+venue+'<br> '+date+'<br> '+location+'<br><br> '
                    local_shows = local_shows + show
            if len(local_shows) > 0:
                short_link = get_bitly(long_link)
                local_shows = local_shows + 'Artist Songkick Link:<br>' +short_link + '<br><br>'
                return local_shows
            else:
                return 'No local shows'





#Downloads the audio content of a youtube video from the URL
import youtube_dl
import urllib.request
from bs4 import BeautifulSoup

##use the two functions below to retrieve a list of URLS to download
def download_all_files(Search_text, path):
    list_of_urls_to_search = get_youtube_urls_from_search(Search_text)
    for url in list_of_urls_to_search: ##download each URL
        try:
            audio_download(url, path)
        except: ##check for ads
            print("video did not download")

#download a single URL, takes a url, and the path you wish to download to
def audio_download(url, path):
    #Set the path, the format and the postprocessors
    youdl_options ={
                    'outtmpl': path +'%(title)s.%(ext)s',
                    'format': 'bestaudio',
                    'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':'mp3', 'preferredquality': '192'}]
                    }
    #Use the youtube_dl to download the audio of the video
    with youtube_dl.YoutubeDL(youdl_options) as youdl:
        youdl.download([url])

#search and scrap the URL's from a youtube search
def get_youtube_urls_from_search(Search_text):
    query = urllib.parse.quote(Search_text)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    list_of_urls=[]
    for video_url in soup.findAll(attrs={'class':'yt-uix-tile-link'}): #get the links out of the beautiful soup object
        if None in (video_url): ##Check for none types in youtubes search
            continue
        else:
            list_of_urls.append('https://www.youtube.com' + video_url['href'])
    return list_of_urls

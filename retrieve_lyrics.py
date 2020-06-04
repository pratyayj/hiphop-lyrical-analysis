import json, requests, os
from bs4 import BeautifulSoup
from selenium import webdriver

BASE_URL = "https://api.genius.com/"
ARTISTS_URL = BASE_URL + "artists/"
retrieve_top25songs_URL = ARTISTS_URL + "{0}/songs?sort=popularity&per_page={1}&text_format=plain"

def getArtistTopSongs(artist_id, count):
    withArtistId_URL = retrieve_top25songs_URL.format(artist_id, count)
    response = requests.get(withArtistId_URL, params={}, 
        headers={'Authorization': 'Bearer CDSY4Xq1QCYHMCZUBbtLhNviQlT045Anwm0FKh6w28Y6YAxtLUKNsrDX000DD_hx'}
    )

    # Generate response
    json_response = response.json()

    # Metadata about artist
    metadata = {
        "artist_id": json_response['response']['songs'][0]['primary_artist']['id'],
        "artist_name": json_response['response']['songs'][0]['primary_artist']['name']
    }

    songs = []
    for x in range(int(count)):
        song_id = json_response['response']['songs'][x]['id']
        song_title = json_response['response']['songs'][x]['title_with_featured']
        song_url = json_response['response']['songs'][x]['url']

        song = {
            "id": song_id,
            "full_title": song_title.encode("ascii", "replace").decode().replace('?', ' '),
            "url": song_url
        }

        songs.append(song)
    
    return { "metadata": metadata, "songs": songs}

def generateLyrics(artist_name, song):
    # Get song lyrics webpage
    song_lyrics_url = song['url']
    print(song_lyrics_url)
    response = requests.get(song_lyrics_url)
    html = response.text

    # TODO: Retrieve page using selenium instead of requests to fix
    # problem of scraping beginning before page is loaded
    '''
    browser = webdriver.Chrome()
    browser.get(song_lyrics_url)
    html_new = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    '''

    # Use BeautifulSoup to parse
    soup = BeautifulSoup(html, 'html.parser')
    lyrics = soup.find_all("div", class_="lyrics")

    path = "./" + artist_name
    # Create folder for artist's songs' lyrics
    if not os.path.exists(path):
       print("path doesn't exist. trying to make")
       os.makedirs(path)

    f = open(path + "/" + song['full_title'] + ".txt", "w")
    for row in lyrics:
        f.write(str(row.get_text()))
    f.close()

# TODO: read in multiple artists' ids and get their top songs
# Kendrick Lamar: 1421
result = getArtistTopSongs("1421", "25")
artist_name = result['metadata']['artist_name']
for x in range(25):
    generateLyrics(artist_name, result['songs'][x])

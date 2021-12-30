import json
import pandas as pd
from tqdm import tqdm
import requests
import time
from transformers import pipeline


    # response = requests.get("https://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=trippie+redd&api_key=ec92e125438f6137cd37c26c3a11ecc7&format=json")
    # json_response = response.json()['topalbums']['album']
    # artist_albums = []
    # for album in json_response:
    #     artist_albums.append(album['name'])
    

# string_encode = string_unicode.encode("ascii", "ignore")
# string_decode = string_encode.decode()

def createArticle():
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

    beatly_data = pd.read_csv('beatly_data.csv', encoding='utf-8-sig')
    artist_data = beatly_data[beatly_data['artist.1'].str.match('trippie redd')]
    artist_data = artist_data.sort_values(by=['final_score'])
    print(artist_data)

    artist_data.reset_index(drop=True, inplace=True)
    print(artist_data)

    # Find number of rows in dataframe index
    row_count = 0

    for col in artist_data.index:
        row_count += 1

    artist_article = open("trippie-redd.txt","w+")

    for row in range(row_count):
        time.sleep(2)
        original_album_name = artist_data.loc[row]["album_name"].encode("ascii", "ignore").decode()
        album_name = original_album_name.replace(" ", "+")
        artist = artist_data.loc[row]["artist"].encode("ascii", "ignore").decode().replace(" ", "+")
        response = requests.get(f'https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ec92e125438f6137cd37c26c3a11ecc7&artist={artist}&album={album_name}&format=json')
        #you can use content instead of summary for a longer draft
        summary = response.json()['album']['wiki']['summary']
        description = (summary + "").split(".")[:-5]
        final_description = ".".join(description) + "."
        artist_article.write(f'<p><b>{row_count - row}. {original_album_name}</b><p>\n')
        artist_article.write(f'<p>{final_description}<p>\n')


    # for i in range(10):
    #     f.write("This is line %d\r\n" % (i+1))

    #response = requests.get(f'https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ec92e125438f6137cd37c26c3a11ecc7&artist={}&album={}&format=json')


createArticle()
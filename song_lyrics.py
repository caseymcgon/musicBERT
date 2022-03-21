# Setting Up Genius Client Account
import lyricsgenius
#genius = lyricsgenius.Genius("G5SIkHkoe5jlivHinVZVKB7pmB_y7WmPQvVrSXdcsSKfzY6k5UA5P6Lf9b_ZezyF")
genius = lyricsgenius.Genius("A4P4WfFuiGTXyQmk5J9xSxfOrPV9qIUeN1up0FE0FIDbIfG39zjbcnd-gRLtvf3V")
## replace above w/ Casey's client ID

# casey's client id = PPxFbur8Qrji5DmjQ3jcPmtICwVv4pGvKsorML1JiJfGGTNgO3_ruwHjbphXRjOn
# casey's secret key = ZNAqLPyrpUpC8GPytkcYv7A_ObWCMkpoydBnJaU0mBv3Noc4QS7h5WekEZplHkfZY9oJsk9sSTnwtz6KhMl9lw
# casey's access token = A4P4WfFuiGTXyQmk5J9xSxfOrPV9qIUeN1up0FE0FIDbIfG39zjbcnd-gRLtvf3V

# Import Dependencies + Packages
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import h5py
import re

# Declaring some variables
songs_df = pd.DataFrame(columns=['Year', 'Title', 'Artist(s)', 'Lyrics'])#, 'Genre'])
website_root = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_"
table_class ="wikitable sortable jquery-tablesorter"

# Collecting all Values
all_years = []
all_song_titles = []
all_artists = []
all_lyrics = []

for year in range(1982, 1985):

  ########
  # Collecting Billboard Data Information
  ########
  print('Startin Data Collection for Year ', str(year))

  wiki_website_url = website_root + str(year) # e.g. "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_1960"
  response = requests.get(wiki_website_url) # getting website response

  soup = BeautifulSoup(response.text, 'html.parser') # grabbing text using beautiful soup and parsing HTML
  indiatable = soup.find('table',{'class':"wikitable"}) # finding wikipedia Billboard table
  billboard_hot100 = pd.read_html(str(indiatable))
  billboard_hot100 = pd.DataFrame(billboard_hot100[0])

  # Collecting Values
  songs_titles = billboard_hot100['Title'].values
  songs_artists = billboard_hot100['Artist(s)'].values
  years = np.ones(len(songs_titles)) * year

  all_song_titles.append(songs_titles)
  all_artists.append(songs_artists)
  all_years.append(years)

  ########
  # Collecting Genius Song Lyrics Data Information
  ########

  songs_lyrics = []

  for song, artist in zip(songs_titles, songs_artists):

    # Searing from song using Genius API
    artist_search = genius.search_artist(artist, max_songs=0, sort="title")

    # Unable to find artist in Genius API
    if artist_search == None:
      songs_lyrics.append("None")
      continue

    a = 0
    while True:
        try:
            song_search = genius.search_song(song, artist_search.name)
            break
        except:
            a += 1
            if a > 5:
                break
            pass
    #song_search = genius.search_song(song, artist_search.name)

    # Unable to find song in Genius API
    if song_search == None:
      songs_lyrics.append("None")
      continue
    else:
      # Getting Lyrics
      song_lyrics = song_search.lyrics

      if len(song_lyrics) == 0:
        songs_lyrics.append("None")
        continue

      # Cleaning Lyrics Data
      punct_re = r'[^\w\s]'
      lyrics = song_lyrics.replace('\n', ' ').replace('\u2005', ' ').replace(punct_re, '').replace('/\s[a-zA-Z]+/', '')
      #print(lyrics)

      # Appending song lyrics
      songs_lyrics.append(lyrics)
      print(len(songs_lyrics))

  # Appending all Values to DataFrame
  #songs_df.append([years, songs_titles, songs_artists, songs_lyrics])
  all_lyrics = songs_lyrics

  # ['Year', 'Title', 'Artist(s)', 'Lyrics']
  # Adding Values to a DataFrame
  year_songs_df = pd.DataFrame(columns=['Year', 'Title', 'Artist(s)', 'Lyrics'])#, 'Genre'])
  year_songs_df['Year'] = years
  year_songs_df['Title'] = songs_titles
  year_songs_df['Artist(s)'] = all_artists[0]
  year_songs_df['Lyrics'] = all_lyrics

  year_songs_df.to_csv('~/Desktop/MIDS/w266/Songs/Data/billboard_hot_100_song_lyrics_' + str(year) + '.csv')
  ## change the above path to fit my Desktop
  print()
  print('Finished Data Collecting for Year ' + str(year))
  print()

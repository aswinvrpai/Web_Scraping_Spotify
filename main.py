import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


USER_ID = "21henkwuikr3j7fjmun3q2iaa"
Client_ID = "4c0fdd497d6243e98d158690939146c1"
Client_Secret = "676665ae184442be9b7782a09ce7cb8e"
Redirect_URL = "http://example.com/"
INPUT = "2022-05-04"
URL = f"https://www.billboard.com/charts/hot-100/{INPUT}/"

# Response from site;
response = requests.get(URL)
data = response.text

# Soup for scraping;
soup = BeautifulSoup(data, "html.parser")
song_titles = []
song_title_data = soup.select(selector="li h3")
for song in song_title_data:
	title = song.getText()
	title = title.replace("\t", "")
	title = title.replace("\n", "")
	song_titles.append(title)
song_titles = song_titles[:100 or None]

# Spotify Authentication done as below;
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		scope="playlist-modify-private",
		redirect_uri=Redirect_URL,
		client_id=Client_ID,
		client_secret=Client_Secret,
		show_dialog=True,
		cache_path="token.txt"
	)
)

# Get Song URI's;
song_uris = []
for song in song_titles:
	search_url = sp.search(q=f"track:{song}", limit=10, offset=0, type='track', market=None)
	try:
		uri = search_url["tracks"]["items"][0]["uri"]
		song_uris.append(uri)
	except IndexError:
		print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify;
playlist = sp.user_playlist_create(user=USER_ID, name=f"MY Billboard 100", public=False)

# Adding songs found into the new playlist;
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


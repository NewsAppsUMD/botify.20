import csv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime

# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual client ID and client secret
client_credentials_manager = SpotifyClientCredentials(client_id='42b50ac3373843b0a7e2e3ab518b9078', client_secret='d01793378c824676bd7e8db63b3907f3')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')
print("Today's date:", today)

# Get new releases
new_releases = sp.new_releases(country='US', limit=50)  # You can specify a different country code if needed

# Filter new releases for today
todays_releases = [album for album in new_releases['albums']['items'] if album['release_date'] == today]

# Print the names of albums released today
for album in todays_releases:
    print(album['name'])
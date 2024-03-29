import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import os

# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual client ID and client secret
client_credentials_manager = SpotifyClientCredentials(client_id='42b50ac3373843b0a7e2e3ab518b9078', client_secret='d01793378c824676bd7e8db63b3907f3')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

# Get new releases
try:
    new_releases = sp.new_releases(country='US', limit=50)  # You can specify a different country code if needed
except Exception as e:
    print("Error occurred while fetching new releases:", e)
    exit()

# Filter new releases for today
todays_releases = [(album['name'], ', '.join([artist['name'] for artist in album['artists']]), album['release_date'], ', '.join(album.get('genres', []))) for album in new_releases['albums']['items'] if album['release_date'] == today]

# Read existing data from releases.csv
existing_data = set()
if os.path.exists('releases.csv'):
    with open('releases.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            existing_data.add((row[0], row[1], row[2], row[3]))

# Filter out releases already in the CSV
new_releases_to_add = [release for release in todays_releases if release not in existing_data]

# Append new releases to the CSV file
if new_releases_to_add:
    with open('releases.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for release in new_releases_to_add:
            writer.writerow(release)
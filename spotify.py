import csv
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
from slack import WebClient
from slack.errors import SlackApiError

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

header_row = ['Album', 'Artists', 'Release Date', 'Genres']

with open('releases.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header_row)  # Write header row
    writer.writerows(todays_releases)  # Write new releases

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

with open('releases.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Album'], row['Artists'], row['Release Date'], row['Genres'])

# slack message construction

slack_token = os.environ.get('SLACK_API_TOKEN')

message = "New releases for today:\n"
for album in new_releases['albums']['items']:
    if album['release_date'] == today:
        artists = ', '.join([artist['name'] for artist in album['artists']])
        message += f"- {album['name']} by {artists}\n"

client = WebClient(token=slack_token)
try:
    response = client.chat_postMessage(
        channel="slack-bots",
        text=message,
        unfurl_links=True, 
        unfurl_media=True
    )
    print("success!")
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")
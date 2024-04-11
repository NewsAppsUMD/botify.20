import csv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
from slack import WebClient
from slack.errors import SlackApiError

# Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual client ID and client secret
client_credentials_manager = SpotifyClientCredentials(client_id='42b50ac3373843b0a7e2e3ab518b9078', client_secret='d01793378c824676bd7e8db63b3907f3')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Import required modules
import os
import csv
from datetime import datetime

# Get releases from April 5, 2024
target_date = '2024-04-05'

# Get new releases
try:
    new_releases = sp.new_releases(country='US', limit=50)
except Exception as e:
    print("Error occurred while fetching new releases:", e)
    exit()

# Filter new releases for April 5, 2024
todays_releases = [(album['name'], ', '.join([artist['name'] for artist in album['artists']]), album['release_date'], album['external_urls']['spotify']) for album in new_releases['albums']['items'] if album['release_date'] == target_date]

header_row = ['Album', 'Artists', 'Release Date', 'External URL']

# Check if releases.csv exists
if not os.path.exists('test-releases-2.csv'):
    print("making the file")
    # Create the file and write the header row
    with open('test-releases-2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header_row)
else:
    print("opening the file")
    # Read existing data from releases.csv
    existing_data = set()
    with open('test-releases-2.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Read the header row
        existing_header = next(reader)
        if existing_header != header_row:
            print("Warning: Header row in the CSV file does not match the expected header.")
        for row in reader:
            existing_data.add((row[0], row[1], row[2], row[3]))

print("Target date:", target_date)

num_releases_today = len(todays_releases)
print("Number of releases today:", num_releases_today)

# Filter out releases already in the CSV
new_releases_to_add = [release for release in todays_releases if release not in existing_data]

# Append new releases to the CSV file
if new_releases_to_add:
    with open('test-releases-2.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for release in new_releases_to_add:
            writer.writerow(release)
else:
    print("No new releases to add to the CSV file.")

# Print the contents of the CSV file
with open('test-releases-2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Release Date'] == target_date:
            print(row['Album'], row['Artists'], row['Release Date'], row['External URL'])

# slack message construction

# Construct the Slack message
slack_token = os.environ.get('SLACK_API_TOKEN')
message = f"A total of {num_releases_today} albums were released today.\nSome of them include:\n"


for release in todays_releases[:5]:
    album_name, artists, release_date = release
    artists = ', '.join(artists.split(', '))  # Assuming artists is a comma-separated string
    message += f"- {album_name} by {artists}\n "

message += "\nIs there any specific artist you want to know about?"

print(message)

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

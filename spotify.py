import csv
import spotipy
import os
import sqlite3
import pandas as pd
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
    new_releases = sp.new_releases(country='US', limit=50)
except Exception as e:
    print("Error occurred while fetching new releases:", e)
    exit()

# Filter new releases for today
todays_releases = [(album['name'], ', '.join([artist['name'] for artist in album['artists']]), album['release_date']) for album in new_releases['albums']['items'] if album['release_date'] == today]

header_row = ['Album', 'Artists', 'Release Date']

# Check if releases.csv exists
if not os.path.exists('releases.csv'):
    print("making the file")
    # Create the file and write the header row
    with open('releases.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header_row)
else:
    print("opening the file")
    # Read existing data from releases.csv
    existing_data = set()
    with open('releases.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Read the header row
        existing_header = next(reader)
        if existing_header != header_row:
            print("Warning: Header row in the CSV file does not match the expected header.")
        for row in reader:
            existing_data.add((row[0], row[1], row[2]))

print("Today's date:", today)

# Filter out releases already in the CSV
new_releases_to_add = [release for release in todays_releases if release not in existing_data]

# Append new releases to the CSV file
if new_releases_to_add:
    with open('releases.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for release in new_releases_to_add:
            writer.writerow(release)
else:
    print("No new releases to add to the CSV file.")

# Print the contents of the CSV file
with open('releases.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if 'Release Date' == today:
            print(row['Album'], row['Artists'], row['Release Date'])

# add new data to database
conn = sqlite3.connect('spotify_releases.db')
cursor = conn.cursor()

def append_csv_to_sqlite(csv_filename, db_filename, table_name):
    # Read CSV data into a pandas DataFrame
    df = pd.read_csv(csv_filename)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_filename)

    # Append DataFrame to the SQLite table
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Commit changes and close connection
    conn.commit()
    conn.close()

csv_filename = 'releases.csv'
db_filename = 'spotify_releases.db'
table_name = 'releases'

append_csv_to_sqlite(csv_filename, db_filename, table_name)

# slack message construction

# Connect to the Datasette database
conn = sqlite3.connect('releases.db')
c = conn.cursor()

# Retrieve today's releases from the database
today = datetime.now().strftime('%Y-%m-%d')
c.execute("SELECT name, artists, release_date, genres FROM spotify_releases WHERE release_date = ? LIMIT 5", (today,))
today_releases = c.fetchall()

# Construct the Slack message
slack_token = os.environ.get('SLACK_API_TOKEN')
message = "Some new releases from today:\n"

for release in today_releases:
    album_name, artists, release_date = release
    artists = ', '.join(artists.split(', '))  # Assuming artists is a comma-separated string
    message += f"- {album_name} by {artists}\n  Genres: {genres}\n"

message += "\nIs there any specific artist you want to know about?"

# Send the Slack message
client = WebClient(token=slack_token)
try:
    response = client.chat_postMessage(
        channel="slack-bots",
        text=message,
        unfurl_links=True,
        unfurl_media=True
    )
    print("Success!")
except SlackApiError as e:
    assert e.response["ok"] is False
    assert e.response["error"]
    print(f"Got an error: {e.response['error']}")

# Close the database connection
conn.close()
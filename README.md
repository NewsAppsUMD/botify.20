# botify-bot

PROCESS:

1. Created a python script called spotify.py that imports libraries like os, requests, json, WebClient and SlackApiError.
2. Created my app through Spotify and started process of getting API authentication.
3. API authentication only lasts 1 hour per access token, so I need to add code to the python script that calls for the token each time. 
4. I realized the code provided by spotify to get API access tokens is in javascript, so I found a library called Spotipy that utilized spotify API in python.
5. I asked ChatGPT how to request an API token, which gave me lines 6-8. 
6. Then, I found code get today's date, find the Spotify releases for that same day, and output the name, artist and date into a csv file.
7. Then, I added code that would filter for new releases on a new day and add that data to the top of the csv.
8. I also created a workflow that will hopefully run the script every day at midnight.
9. I want the genres to display in the csv as well, but I'm having trouble. Right now, it may be because those aren't pieces of data I can pull yet from the API, but I will work on this.
10. I think after this, what I mainly want to focus on now is connecting it to my slackbot and creating message notifications with releases for that day.
11. Right now, it only pulls data for all album releases, but I want to figure out how to cater it to users, or only have it show specific artists based on parameters established by the user. 
12. I tried pushing and committing to main in my old repository, but I got the following error:
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/NewsAppsUMD/botify-bot'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

Maybe this has to do with the workflow I created to add updates? I will ask for help after break. 

## MARCH 30 UPDATE

I was able to add header rows to the CSV file and used dictreader to access the data. I also successfully added a workflow to this version of the bot, so we will have to see how that goes. I also managed to connect this all to my slack bot and successfully craft a message for it to send out. Right now, the message just outputs all the releases for the day, so I need to figure out how I want to clean it up a bit more. What comes next is figuring out how to implement users adding preferences for artists and how to access those specific endpoints in the API to notify whenever they are released. 
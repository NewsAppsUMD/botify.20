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

I was able to add header rows to the CSV file and used dictreader to access the data. I also successfully added a workflow to this version of the bot, so we will have to see how that goes. I also managed to connect this all to my slack bot and successfully craft a message for it to send out. Right now, the message just outputs all the releases for the day, so I need to figure out how I want to clean it up a bit more. What comes next is figuring out how to implement users adding preferences for artists and how to access those specific endpoints in the API to notify whenever they are released. I have learned so far that the process is more straight forward than I thought. It's all about breaking down the components, i.e., fetching the Spotify API data, then organizing it, then scheduling the workflow, then calling it to slack, etc. The data I am collecting through this is fairly simplistic so far, so I want to figure out more ways I can expand and analyze it, especially if I want to transform it into a news app.

## APR 1 CLASS UPDATE

Added everything to a sqlite database to help with building a dataset for my news app. It worked, but now the csv shows up empty whenever I run the code.

## APR 6 UPDATE

Updated how data is appended to the csv and then to the sqlite database after that. Unfortunately, the data from Apr 1 was overwritten, so now the data is only from Apr 5 so far. As of tonight, it's hard to tell if the appending new data works because I'm unsure if it's because it isn't working or if it's because there aren't new releases to add. Still working on refining slack message

## FINAL UPDATE

When I first began working on this bot, my initial struggle was figuring out how to access the Spotify API. Getting the credentials was easy enough compared to other streaming services, but most of the code provided by Spotify’s official site for accessing the API was in JavaScript. Another part of the problem was that calling codes using this script would require repeated changes to the secrets for the codespace because the access codes only last for a short period of time. I was able to work around this by finding Spotipy, a python library that allows you to work with Spotify API. With this library, I was able to easily call and implement the access codes into the beginning of my script. From there, fetching new release data was fairly easy. After that, I began storing the data into a csv called releases.csv. After that, I began connecting everything to my slack bot and was able to craft a simple message that sent out just a list of the releases for that day. There were times while testing out my code that no releases would be added to the csv for that day, and I couldn’t tell if it was because it wasn’t working or if there really weren’t any releases that day. So, in my test-spotify script, I changed the code to get releases from a specific date rather than the current day. I then input a date where I definitely knew that albums were released, and it would work. And for the days where there were no releases, I put those specific dates back into the test-spotify script and it turned out that there really weren’t any albums those days. I eventually put the data from the csv into a database just to help store data for the future. As for the final message, it tells you how many total releases came out that day outputs a list of just 5 of those releases, if there are any. It then asks if you want to see the full list. If there aren’t any releases for that day, it provides you a list of 5 previous releases you may have missed. The message also includes hyperlinks to any albums that are put in the message.

Unfortunately, I was not able to accomplish user input because I was focused on issues regarding cleaning up and calling for the data between the csv, database and slack. However, ideally, the bot would accept inputs such as artist names and it would output their most recent releases, or you could even input a date and it would return all the albums from that day. And with inputting artists, maybe the bot could eventually store their names and when they release something in the future, they will be especially noted in the daily release notification. For example, if I asked for Beyonce releases a while back and on the current day she releases an album, the message would say something like this: “Beyonce actually just released an album today if you want to check it out: [Album name]!. Here are some other releases from today as well: [other releases].” I think the best schedule for updates for this type of bot is definitely daily, especially for users who are very music oriented or just want to be kept updated on new music. I think a more useful version of this bot would not only tell you about recent releases, but also provide you with general recommendations catered to your specific tastes or interests. This would be similar to the artist input from before where it could say, “We noticed you liked Beyonce! Here’s an/some album(s) that were released today that are similar:” Or it could remove the date restriction and just provide you with a general list of recommendations no matter the release date. 

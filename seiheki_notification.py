from datetime import datetime, timedelta
import json
import os

from googleapiclient.discovery import build
import twitter

from src.gcalendar import GcalAPI

gapi = GcalAPI()
creds = gapi.login(os.environ["GCAL_TOKEN_PATH"], os.environ["GCAL_CREDENTIALS_PATH"])
service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
now = datetime.utcnow()
tomorrow = now + timedelta(days=1)
now = now.isoformat() + 'Z' # 'Z' indicates UTC time
tomorrow = tomorrow.isoformat() + 'Z' # 'Z' indicates UTC time

print('Getting the upcoming 10 events')
events_result = service.events().list(
    calendarId=os.environ["SHIRAYUKI_CALENDARID"], 
    timeMin=now,
    timeMax=tomorrow,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime').execute()
events = events_result.get('items', [])

text = ""
if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    text += f"{start}\n{event['summary']}\n"

if events:
    print(text)

    tauth = twitter.OAuth(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET_KEY"],
        token=os.environ["ACCESS_TOKEN"],
        token_secret=os.environ["ACCESS_TOKEN_SECRET"]
    )
    tapi = twitter.Twitter(auth=tauth)
    tapi.statuses.update(status=text)
    print("done!")

events_result = service.events().list(
    calendarId=os.environ["REMINDER_CALENDARID"], 
    timeMin=now,
    timeMax=tomorrow,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime').execute()
events = events_result.get('items', [])

text = ""
if not events:
    print('No upcoming events found.')
for event in events:
    end = event['end'].get('dateTime', event['end'].get('date'))
    text += f"{end} まで\n{event['summary']}\n"
print(text)
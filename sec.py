import os
from datetime import datetime, timedelta

import twitter
from googleapiclient.discovery import build

from src.gcalendar import GcalAPI

gapi = GcalAPI()
creds = gapi.login(os.environ["GCAL_TOKEN_PATH"], os.environ["GCAL_CREDENTIALS_PATH"])
service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
now = datetime.utcnow()
now = now.isoformat() + 'Z' # 'Z' indicates UTC time

print("Get Calendar Item")
events_result = service.events().list(
    calendarId=os.environ["SCHEDULED_CALENDARID"], 
    timeMin=now,
    maxResults=1,
    singleEvents=True,
    orderBy='startTime').execute()
events = events_result.get('items', [])

text = ""
if not events:
    print('Today is not a scheduled submission day.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    text += f"{start}\n{event['summary']}\n"

if events:
    print(text)

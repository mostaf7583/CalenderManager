import datetime
import json
import os
import pickle
import pytz
import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'
def get_local_timezone():
    return str(pytz.timezone('africa/cairo'))


TIMEZONE = get_local_timezone()

def authenticate():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)
def create_event(service, summary, start_datetime, end_datetime, location):
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': TIMEZONE,
        },
        'location': location,
    }

    service.events().insert(calendarId='primary', body=event).execute()
def main():
    service = authenticate()

 
    events = [
    {
        'summary': 'Computer Organization and System Programming',
        'start_datetime': datetime.datetime(2023, 6, 12, 11, 0),
        'end_datetime': datetime.datetime(2023, 6, 12, 14, 0),
        'location': 'H11',
    },
    {
        'summary': 'Compiler',
        'start_datetime': datetime.datetime(2023, 6, 22, 11, 0),
        'end_datetime': datetime.datetime(2023, 6, 22, 14, 0),
        'location': 'Exam hall 2',
    },
    {
        'summary': 'Project Management',
        'start_datetime': datetime.datetime(2023, 6, 15, 14, 30),
        'end_datetime': datetime.datetime(2023, 6, 15, 17, 30),
        'location': 'D1.002',
    },
    {
        'summary': 'Knowledge Representation And Reasoning',
        'start_datetime': datetime.datetime(2023, 6, 18, 14, 30),
        'end_datetime': datetime.datetime(2023, 6, 18, 17, 30),
        'location': 'H10',
    },
    {
        'summary': 'Project Management',
        'start_datetime': datetime.datetime(2023, 6, 15, 18, 0),
        'end_datetime': datetime.datetime(2023, 6, 15, 20, 0),
        'location': 'D1.002',
    },
    {
        'summary': 'Compiler',
        'start_datetime': datetime.datetime(2023, 6, 22, 8, 30),
        'end_datetime': datetime.datetime(2023, 6, 22, 10, 30),
        'location': 'C7.01',
    },
    {
        'summary': 'Computer Organization and System Programming',
        'start_datetime': datetime.datetime(2023, 6, 12, 8, 30),
        'end_datetime': datetime.datetime(2023, 6, 12, 10, 30),
        'location': 'C7.01',
    }
]
    

    for event in events:
        create_event(
            service,
            event['summary'],
            event['start_datetime'],
            event['end_datetime'],
            event['location']
        )

# 


if __name__ == '__main__':

    main()

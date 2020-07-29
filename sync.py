from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tinydb import TinyDB, Query
import argparse
from tqdm import tqdm

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

db = None
service = None


def authenticate():
    print("Authenticating with Google Calender API\n")

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def create_event(assignment):
    print("Creating event on Google Calender -", assignment['id'])
    datestr = assignment['date'] + " " + assignment['time']
    start_time = datetime.datetime.strptime(datestr, '%Y-%m-%d %I:%M %p')
    end_time = start_time + datetime.timedelta(minutes=30)

    event = {
        'summary': assignment['course'] + " - " + assignment['title'],
        'description': assignment['description'],
        'start': {
            'dateTime': start_time.isoformat('T'),
            'timeZone': 'Asia/Colombo',
        },
        'end': {
            'dateTime': end_time.isoformat('T'),
            'timeZone': 'Asia/Colombo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 2 * 24 * 60},
                {'method': 'popup', 'minutes': 24 * 60},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    Assignment = Query()
    db.update({'synced': True}, Assignment.id == assignment['id'])
    print('Event created: %s \n' % (event.get('htmlLink')))


def main():
    parser = argparse.ArgumentParser(description='Scrape UGVLE assignments.')
    parser.add_argument('-s', '--store', type=str,
                        help='Data store directory', default='data')

    args = parser.parse_args()

    store = args.store

    print("Initiallizing store")
    store_path = store + "/assignments.json"

    if not os.access(store_path, os.W_OK):
        print("Data store not found")
        return

    global db
    db = TinyDB(store_path)
    print("No. assignments in store:", len(db), '\n')

    creds = authenticate()
    if not creds:
        "Authentication failure"
        return

    global service
    service = build('calendar', 'v3', credentials=creds)

    Assignment = Query()
    not_synced = db.search(Assignment.synced == False)

    print("Events to sync:", len(not_synced))

    if len(not_synced) > 0:
        for assignment in tqdm(not_synced):
            create_event(assignment)

    print("Sync complete")


if __name__ == '__main__':
    main()

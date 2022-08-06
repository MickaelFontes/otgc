import os

from gcsa.google_calendar import GoogleCalendar
from google.oauth2.credentials import Credentials

from otgc.reader import ReaderICS
from otgc.manual import Onboard

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

def main(manual=True):
    '''Process to update your Google Calendar from OnBoard'''
    directory = config['RUN']['DOWNLOADS_FOLDER']
    calendar_id = config['GOOGLE_CALENDAR']['CALENDAR_ID']
    token_path = config['GOOGLE_CALENDAR']['TOKEN_PATH']
    credentials_path = config['GOOGLE_CALENDAR']['JSON_CREDENTIALS_PATH']


    token = Credentials(
        token=None,
        refresh_token=config['OAUTH']['REFRESH_TOKEN'],
        client_id=config['OAUTH']['CLIENT_ID'],
        client_secret=config['OAUTH']['CLIENT_SECRET'],
        scopes=[config['OAUTH']['SCOPE']],
        token_uri=config['OAUTH']['TOKEN_URI']
    )
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

    if not manual:
        from otgc.selenium import GetOnboard
        nb_months = 2
        # Step 1: Clean Downloads directory and create it if needed

        # Step 2: Get the planning.ics files from OnBoard
        onboard_planning = GetOnboard(credentials=config['ONBOARD']['CREDENTIALS_PATH'],
                                      export_dir=os.path.abspath(directory),
                                      nb_months=nb_months,
                                      gecko_path=config['SELENIUM']['GECKO_PATH'])
        onboard_planning.get_ics()

    else:
        nb_months = 1
        # Manual process GET/POST
        with open(config['ONBOARD']['CREDENTIALS_PATH'], "r") as file:
            lines = file.readlines()
            username = lines[0].rstrip()
            password = lines[1].rstrip()
        essai_get_post = Onboard(username, password)
        essai_get_post.post_login()
        essai_get_post.get_main()
        essai_get_post.post_planning()
        essai_get_post.post_my_planning()
        essai_get_post.get_my_planning()
        essai_get_post.post_planning_year()
        essai_get_post.post_download()

        with open(config['RUN']['DOWNLOADS_FOLDER']+'/planning.ics', 'w') as file:
            file.write(essai_get_post.last_request.text)
        print('Calendar downloaded.')

    # Step 3: Read all ICS files, get all unique events
    all_events = []
    viewed_events = set()
    file_names = ['planning.ics']
    if nb_months > 1:
        file_names += [
            'planning(' + str(i) + ').ics' for i in range(1, nb_months)
        ]

    for file in file_names:
        reader = ReaderICS(directory + '/' + file)
        current_events = reader.read()
        all_events += [
            event for event in current_events if event.uid not in viewed_events
        ]
        viewed_events.update([e.uid for e in current_events])
    # Step 4: Setup connection to Google Calendar, clean and import
    ## I know it's a bit "bourrin", feel free to propose your own method
    calendar_ecn = GoogleCalendar(calendar=calendar_id,
                                  token_path=token_path,
                                  credentials=token)

    for event in calendar_ecn:
        calendar_ecn.delete_event(event)
    for event in all_events:
        calendar_ecn.import_event(event.to_gcsa_event())

    print(len(all_events), 'events imported.')

def  helloWorld(x):
    """Function called by Cloud Function"""
    from time import time
    start = time()
    main(manual=True)
    print(time() - start)
    
if __name__ == '__main__':
    from time import time
    start = time()
    main(manual=True)
    print(time() - start)

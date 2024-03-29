import os
from time import time
import configparser

from gcsa.google_calendar import GoogleCalendar
from google.oauth2.credentials import Credentials

from otgc.reader import ReaderICS
from otgc.manual import Onboard


config = configparser.ConfigParser()
config.read("config.ini")


def main(
    manual=True, export=False, username=None, password=None, credentials_file=False
):
    """Process to update your Google Calendar from OnBoard"""
    directory = config["RUN"]["DOWNLOADS_FOLDER"]
    calendar_id = config["GOOGLE_CALENDAR"]["CALENDAR_ID"]
    token_path = config["GOOGLE_CALENDAR"]["TOKEN_PATH"]
    if credentials_file:
        credentials_path = config["ONBOARD"]["CREDENTIALS_PATH"]

    token = Credentials(
        token=None,
        refresh_token=config["OAUTH"]["REFRESH_TOKEN"],
        client_id=config["OAUTH"]["CLIENT_ID"],
        client_secret=config["OAUTH"]["CLIENT_SECRET"],
        scopes=[config["OAUTH"]["SCOPE"]],
        token_uri=config["OAUTH"]["TOKEN_URI"],
    )
    if export:
        if not os.path.exists(directory):
            os.makedirs(directory)
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))

    # Manual process GET/POST
    if credentials_file:  # OnBoard credentials are stored as clear text in a file
        with open(credentials_path, "r", encoding="UTF-8") as file:
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

    if export:
        with open(directory + "/planning.ics", "w", encoding="UTF-8") as file:
            file.write(essai_get_post.last_request.text)
        print("ICS Calendar exported.")

    # Step 3: Read all ICS files, get all unique events
    all_events = []
    viewed_events = set()

    reader = ReaderICS(essai_get_post.last_request.text)
    current_events = reader.read()
    all_events += [event for event in current_events if event.uid not in viewed_events]
    viewed_events.update([e.uid for e in current_events])
    # Step 4: Setup connection to Google Calendar, clean and import
    # I know it's a bit "bourrin", feel free to propose your own method
    calendar_ecn = GoogleCalendar(
        calendar=calendar_id, token_path=token_path, credentials=token
    )

    for event in calendar_ecn:
        calendar_ecn.delete_event(event)
    for event in all_events:
        calendar_ecn.import_event(event.to_gcsa_event())

    print(len(all_events), "events imported.")


def helloWorld(request):
    """Function called by the Cloud Function

    Args:
        request (flask.Request): request that triggered the Cloud Function

    Returns:
        string: Execution status at the end
    """

    request_args = request.get_json()
    print(request_args.keys())
    if request_args and "username" in request_args and "password" in request_args:
        print("Arguments valid")
        username = request_args["username"]
        password = request_args["password"]
        print("User: ", username)
    else:
        return "Arguments not valid"
    start = time()
    main(manual=True, username=username, password=password)
    print(time() - start)
    return "Calendar update complete"


if __name__ == "__main__":
    start_main = time()
    main(manual=True, credentials_file=True)
    print(time() - start_main)

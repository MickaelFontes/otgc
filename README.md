# OTGC: OnBoard to Google Calendar

Project to automate the update of a Google Calendar schedule based on a [OnBoard](https://onboard.ec-nantes.fr) schedule.

## Approach adopted: Manual requests

Since Onboard has no public API and uses `javax.faces.ViewSate` which gives each loaded page a unique number impossible to predict, we'll get the scheduele doing manual HTTP GET/POST requests as if were clicking on the webpage with our mouse.

**WARNING:**  
In this project, we suppose that an entire calendar of your Google Calendar is dedicaded to your OnBoard schedule. This way, any error or mishandling won't have any impact on your personnal calendar. In the worst case scenario, you simply have to import a new ICS from OnBoard to correct everything.
*Please* ensure that's the case. This tool is provided "as is" and I won't be responsible for any error or problem you may encounter using it.

# Installation

1. [Create a new Google Cloud Platform (GCP) project](https://developers.google.com/workspace/guides/create-project)
2. [Configure OAuth and Google Calendar](#google-calendar-configuration)
3. Use OTGC (choose one of the following options)
   1. Locally with manual script
   2. [Remotly with a GCP Cloud Function](terraform/README.md)
      1. With Cloud Scheduler (credentials in clear for now)
      2. With manual trigger (no OnBoard credentials stored in clear)
   3. Else: as you want ;)

You can use OTGC locally on your machine or use Free Tier GCP ressources to automate everything and use cloud ressources.

> IMPORTANT: If you choose to use GCP ressources (like Cloud Functions), you will need to associate a billing account to your GCP project (and give Google a credit card in case your consume more than their Free Tier). If you don't want to, you still can use OTGC locally and use your own computer with a scheduled task to update automatically your Google Calendar !

During the process, you will need to note down some elements:

* your GCP project ID (it may differ from the name you gave to it)
* your token's fields (id, secret and associated refresh token)
* your Google calendar's ID

## Local installation

**NB:** For now, the documented method consists in storing your OnBoard credentials in clear. This is NOT RECOMMENDED, at your own risk. An `input()` based version is planned.

First, install the ``requirements.txt`` with pip (it contains the ``requests`` and ``gcsa`` modules).

You need to configure a few things:

* Add your OnBoard credientials
* Google Calendar authentification

## Add your OnBoard credientials

To download your schedule, your credentials are needed to connect onto OnBoard.  
Please write them in a simple text file in the ``Credentials`` folder and edit the path in the `config.ini` file.  
The first line of the file must be the username and the second line the password.

## Google Calendar Configuration

### Google Calendar Authentification

To connect to Google Calendar, I used [Google Calendar Simple API](https://github.com/kuzmoyev/google-calendar-simple-api), a Python package to simply use the Google Calendar API in Python.

You will need to get your API credentials and refer to them in the `config.ini` file. To do so:

1. Enable the "Google Calendar API" for your project
2. [Configure the OAuth consent screen](https://developers.google.com/workspace/guides/create-credentials#configure_the_oauth_consent_screen) and ensure that, at the scopes' step, you have no scope selected at all.
3. Switch your application in `production` state
4. [Create a OAuth client ID credential](https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential) (select the `Web application` setting and add the following URL in the `Authorized redirect URIs` list: [https://developers.google.com/oauthplayground/](https://developers.google.com/oauthplayground))
5. Go to the [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
6. Click on the gear icon in the upper-right. Check the `Use your own OAuth credentials` box and input your Client ID and Client Secret
7. On the left side of the screen, under the `Google Calendar API`, select the `https://www.googleapis.com/auth/calendar` OAuth scope and then click `Authorize APIs`.
8. Click "Authorize APIs"
9. Click "Grant access" at the OAuth 2.0 permissions screen
10. Click the "Exchange authorization code for tokens" button
11. Go back to "Step 2" where your refresh token is displayed.
12. Copy and paste somewhre your refresh token, your Client ID and its associated secret.

### Configure your Google Calendar

Your OnBoard events will be imported on the calendar you specify.
We **recommend** you to create a new calendar (with a non-ambiguous name, such as `ECN`) exclusively for this use, since at each update, all events are deleted before the new import.

To do that:

1. Go to [Google Calendar](https://calendar.google.com/calendar/) and log in.
2. Click on the gear icon in the upper-right corner and then click on settings
3. In the middle of the left panel, click to enlarge the "Add calendar" section and then click on "Create new calendar"
4. Type a name and then click on the blue button "Create calendar"
5. Your calendar has been created. To get its ID, under the section "Settings for my calendars of the left panel", click on your calendar's name.
6. Scroll down a little bit and find the "Calendar ID" sub-section, just under the "Integrate calendar" section.
7. Copy and paste your calendar's ID somewhere. You will need it latter.

# Usage

Once you've configured everything, simply run the `run.py` file to update your Google Calendar.

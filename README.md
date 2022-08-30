# OTGC: OnBoard to Google Calendar

Project to automate the update of a Google Calendar schedule based on a [OnBoard](https://onboard.ec-nantes.fr) schedule.

## Approach adopted: Manual requests

Since Onboard has no public API and uses `javax.faces.ViewSate` which gives each loaded page a unique number impossible to predict, we'll get the scheduele doing manual HTTP GET/POST requests as if were clicking on the webpage with our mouse.

**WARNING:**  
In this project, we suppose that an entire calendar of your Google Calendar is dedicaded to your OnBoard schedule. This way, any error or mishandling won't have any impact on your personnal calendar. In the worst case scenario, you simply have to import a new ICS from OnBoard to correct everything.
*Please* ensure that's the case. This tool is provided "as is" and I won't be responsible for any error or problem you may encounter using it.

# Installation

You can use OTGC locally on your machine or deploy a Google Cloud Function to perform the calendar update.
In both cases, you will need to get a token to acces the Google Calendar API.

## Local installation

**NB:** For now, the documented method consists in storing your OnBoard credentials in clear. This is NOT RECOMMENDED, at your own risk. An `input()` based version is planned.

First, install the ``requirements.txt`` with pip (it contains the ``requests`` and ``gcsa`` modules).

You need to configure a few things:

* Add your OnBoard credientials
* Google Calendar authentification
* Selenium (Optionnal - Legacy)

## Add your OnBoard credientials

To download your schedule, your credentials are needed to connect onto OnBoard.  
Please write them in a simple text file in the ``Credentials`` folder and edit the path in the `config.ini` file.  
The first line of the file must be the username and the second line the password.

## Google Calendar Configuration

### Google Calendar Authentification

To connect to Google Calendar, I used [Google Calendar Simple API](https://github.com/kuzmoyev/google-calendar-simple-api), a Python package to simply use the Google Calendar API in Python.

You will need to get your API credentials and refer to them in the `config.ini` file. To do so:

1. [Create a new Google Cloud Platform (GCP) project](https://developers.google.com/workspace/guides/create-project)
2. Enable the "Google Calendar API" for your project
3. [Configure the OAuth consent screen](https://developers.google.com/workspace/guides/create-credentials#configure_the_oauth_consent_screen)
4. [Create a OAuth client ID credential](https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential) (select the `Web application` setting and add the following URL in the `Authorized redirect URIs` list: [https://developers.google.com/oauthplayground/](https://developers.google.com/oauthplayground/))
5. Go to the [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
6. Click the gear icon in the upper-right. Check the `Use your own OAuth credentials` box and input your Client ID and Client Secret
7. On the left side of the screen, under the `Google Calendar API`, select the `https://www.googleapis.com/auth/calendar` OAuth scope and then click `Authorize APIs`.
8. Click "Authorize APIs"
9. Click "Grant access" at the OAuth 2.0 permissions screen
10. Click the "Exchange authorization code for tokens" button
11. Your refresh token is displayed. Copy ans paste the refresh token and the Client ID in your `config.ini` file.

**NB:** By default, the `Publishing status` of your app is `Testing`, which causes refresh tokens to expire after 7 days, so you will need to manually refresh them on [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/) and repeat the steps 5 to 11. To change that, follow the `Publish app` procedure as described on the `OAuth consent screen` page.

### Configure your Google Calendar

Your OnBoard events will be imported on the calendar you specify.
We **recommend** you to create a new calendar (with a non-ambiguous name, such as `ECN`) exclusively for this use, since at each update, all events are deleted before the new import.

To tell OTGC which calendar you want to update, specify your calendar ID in the configuration file (as the `config['GOOGLE_CALENDAR']['CALENDAR_ID']` variable).
You can find your calendar ID on the Google Calendar webapp.
Go to the calendar settings, then on the left side select your calendar.
Scroll down a little bit and you will find your calendar ID. Its name ends with `@group.calendar.google.com`.

## Selenium (Legacy - Optional)

If you need to use the other approach based on selenium, first install the Selenium Python module:

```python
pip install selenium    
```

Then, update the `config['SELENIUM']['GECKO_PATH']` variable to point to your gecko driver (or your other WebDriver if you choose another one).  
Now, everything should be fine. If you have any issue, please read the documentation [here](https://selenium-python.readthedocs.io/installation.html).

# Usage

Once you've configured everything, simply run the `run.py` file to update your Google Calendar.

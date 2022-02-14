# OTGC: OnBoard to Google Calendar

Project to automate the update of a Google Calendar schedule based on a [OnBoard](https://onboard.ec-nantes.fr) schedule.

## First approach: Using [Selenium](https://www.selenium.dev/)

The OnBoard schedule is downloaded using Selenium and then imported into Google Calendar using [Google Calendar Simple API](https://github.com/kuzmoyev/google-calendar-simple-api).

## Second approach: Manual requests

Since Onboard has no public API and uses `javax.faces.ViewSate` which gives each loaded page a unique number impossible to predict, we'll get the scheduele doing manual HTTP GET/POST requests as if were clicking on the webpage with our mouse.

# Installation

First, install the ``requirements.txt`` with pip (it contains the ``requests`` and ``gcsa`` modules).

You need to configure a few things:

* Add your OnBoard credientials
* Google Calendar authentification
* Selenium (Optionnal)

## Add your OnBoard credientials

To download your schedule, your credentials are needed to connect onto OnBoard.
Please write them in a simple text file in the ``Credentials`` folder and edit the path in the `config.ini` file.
The first line of the file must be the username and the second line the password.

## Google Calendar Authentification

To connect to Google Calendar, I used [Google Calendar Simple API](https://github.com/kuzmoyev/google-calendar-simple-api), a Python package to simply use the Google Calendar API in Python.
You will need to get your API credentials and refer to them in the `config.ini` file. Please follow the documentation [here](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html) and once you have your `credentials.json`, add a path to it in `config.ini` (as the `config['GOOGLE_CALENDAR']['JSON_CREDENTIALS_PATH ']` variable).
You will also need to add your calendar ID in teh configuration file (as the `config['GOOGLE_CALENDAR']['CALENDAR_ID']` variable).

## Selenium (Optional)

If you need to use the other approach based on selenium, first install the Selenium Python module:

```python
pip install selenium    
```

Then, update the `config['SELENIUM']['GECKO_PATH']` variable to point to your gecko driver (or your other WebDriver if you choose another one).
Now, everything should be fine. If you have any issue, please read the documentation [here](https://selenium-python.readthedocs.io/installation.html).

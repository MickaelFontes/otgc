# OTGC: OnBoard to Google Calendar

Project to automate the update of a Google Calendar schedule based on a [OnBoard](https://onboard.ec-nantes.fr) schedule.

## Approach adopted: Manual requests

Since Onboard has no public API and uses `javax.faces.ViewSate` which gives each loaded page a unique number impossible to predict, we'll get the scheduele doing manual HTTP GET/POST requests as if were clicking on the webpage with our mouse.

**WARNING:**  
In this project, we suppose that an entire calendar of your Google Calendar is dedicaded to your OnBoard schedule. This way, any error or mishandling won't have any impact on your personnal calendar. In the worst case scenario, you simply have to import a new ICS from OnBoard to correct everything.
*Please* ensure that's the case. This tool is provided "as is" and I won't be responsible for any error or problem you may encounter using it.

# Installation

1. [Create a new Google Cloud Platform (GCP) project](https://developers.google.com/workspace/guides/create-project)
2. [Configure OAuth and Google Calendar](GoogleCalendarAPI.md)
3. Use OTGC (choose one of the following options)
   1. Locally with manual script (doc coming soon)
   2. [Remotly with a GCP Cloud Function](terraform/README.md)
      1. With Cloud Scheduler (credentials in clear for now)
      2. With manual trigger (no OnBoard credentials stored in clear - doc coming soon)
   3. Else: as you want ;)

You can use OTGC locally on your machine or use Free Tier GCP ressources to automate everything and use cloud ressources.

> IMPORTANT: If you choose to use GCP ressources (like Cloud Functions), you will need to associate a billing account to your GCP project (and give Google a credit card in case your consume more than their Free Tier). If you don't want to, you still can use OTGC locally and use your own computer with a scheduled task to update automatically your Google Calendar !

During the process, you will need to note down some elements:

* your GCP project ID (it may differ from the name you gave to it)
* your token's fields (id, secret and refresh token)
* your Google calendar's ID

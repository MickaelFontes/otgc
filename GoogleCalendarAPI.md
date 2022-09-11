# Google Calendar Configuration

## Google Calendar Authentification

>In this part, you will get:
>
>* your project's ID
>* your OAuth Client ID
>* your OAuth Client Secret
>* your OAuth Refresh Token
>
>Note them down in a notapd window, you will need them later.

To get them, follow these steps:

1. Open [Google Cloud Console](https://console.cloud.google.com/)
![Cloud console](pictures/2022-09-11-11-52-58.png)
**Copy your project ID in your notepad tab by clicking on the button next to "Project ID".**
2. Look for the Google Calendar API and click on it
![Search API](pictures/2022-09-11-11-54-22.png)
3. Enable the "Google Calendar API" for your project
![Google Calendar API](pictures/2022-09-11-11-55-26.png)
4. Look for the "APi & Services" page and click on it to activate the API.
![Search API & Services](pictures/2022-09-11-11-59-18.png)
5. Go to OAuth consent scren
![OAuth consent screen](pictures/2022-09-11-12-00-32.png)
6. Select "External type"
![External type](pictures/2022-09-11-12-02-11.png)
7. Fill only the required fields (use your current Google email address when necessary). Then, go next.
![App info](pictures/2022-09-11-12-03-18.png)
8. At the "Scopes" step, verify CAREFULLY that all the 3 scopes categories are empty. Then, go next.
![Scopes](pictures/2022-09-11-12-05-06.png)
9. At the "Test users" step, add your current Google account among the test users. Then, go next.
![Test users](pictures/2022-09-11-12-06-12.png)
10. At the final "Summary" step, verify everything is similar to that screen,  with your email address when necessary. Then, click on "Back to dashboard0"
![Summary](pictures/2022-09-11-12-09-41.png)
11. Switch your application in `production` state by clicking on the button
![Production](pictures/2022-09-11-12-10-29.png)
12. Now, it should look like that
![Check status](pictures/2022-09-11-12-10-52.png)

Congratulations! You have configured your OAuth consent screen with an application in production state!
From now on, the OAuth refresh token we will get latter will not expire!

Do not close your tab! Now, we just need to get the necessary tokens to interact with the Google Calendar API with no expiration limit!

1. Still in "API & Services", go the the "Credentials" Menu
![Go to Credentials](pictures/2022-09-11-12-18-37.png)
2. On the "Credentials" page, click on "Create credentials" and then OAuth client ID
![Credentials](pictures/2022-09-11-12-20-11.png)
3. For application type, select "Web application".
4. Choose a name for this token.
5. Add this URI [https://developers.google.com/oauthplayground](https://developers.google.com/oauthplayground) in the "Authorized redirect URIs" section (be careful not to add a slash at the end). The completed page should look like that:
![OAoth client ID creation](pictures/2022-09-11-12-22-27.png)
6. Then click on "Create". It will take you back to the "Credentials" page and the folliwing popup should appear.
![Popup OAuth](pictures/2022-09-11-12-26-51.png)
**Copy both your Client ID and your Client Secret on a notepad window.** We will need them.

Now, we will go tp the [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground) to generate a refresh token to human interactions once everything is deployed.

1. Go to the [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground)
2. Click on the gear icon in the upper-right. Check the `Use your own OAuth credentials` box and input your Client ID and Client Secret
![Token playground](pictures/2022-09-11-12-39-02.png)
3. On the left side of the screen, under the `Google Calendar API`, select the `https://www.googleapis.com/auth/calendar` OAuth scope and then click `Authorize APIs`.
![Select scope Calendar](pictures/2022-09-11-12-40-05.png)
4. Click "Authorize APIs" and select your Google account or log in.
5. On the warning screen, click on "Show advanced" and then "Go to" at the bottom left of the page.
![Warning screen not verified](pictures/2022-09-11-12-43-54.png)
6. The next screen dexcribe the authorization you grant to the app  using the token. Click on "Continue"
![wants access](pictures/2022-09-11-12-45-47.png)
7. Click the "Exchange authorization code for tokens" button
![Get refresh token](pictures/2022-09-11-12-46-21.png)
8. It will fill the "Refresh token" and "Access token" fields, and then automatically hide the "Step 2" section and show the "Step 3" section instead. Click back on "Step 2" to go back to the previous step if you did not have enough time to copy it
![Go back to step 2](pictures/2022-09-11-13-50-38.png)
**Then, copy the "Refresh token" obtained at "Step 2" and paste it in your notepad** with your Client ID and Client Secret.

Congratulations! Now you have your precious Resfresh Token!

Now, we will create a new Google Calendar and use it exclusively for OTGC.

## Create a new Google Calendar

>In this part, you will get:
>
>* your new calendar's ID
>
>Note it down in a notapd window, you will need them later.

Your OnBoard events will be imported on the calendar you specify.
We **recommend** you to create a new calendar (with a non-ambiguous name, such as `ECN`) exclusively for this use, since at each update, all events are deleted before the new import.

To do that:

1. Go to [Google Calendar](https://calendar.google.com/calendar/) and log in.
2. Click on the gear icon in the upper-right corner and then click on settings
![go to settings](pictures/2022-09-11-12-56-04.png)
3. In the middle of the left panel, click to enlarge the "Add calendar" section and then click on "Create new calendar"
![Create calendar](pictures/2022-09-11-12-56-39.png)
4. Type a name and then click on the blue button "Create calendar"
![Name calendar](pictures/2022-09-11-12-57-03.png)
5. Your calendar has been created. To get its ID, under the section "Settings for my calendars of the left panel", click on your calendar's name.
![Go to the created calendar](pictures/2022-09-11-12-57-32.png)
6. Scroll down a little bit and find the "Calendar ID" sub-section, just under the "Integrate calendar" section.
![Integrate calendar section](pictures/2022-09-11-12-58-02.png)
7. Copy and paste your calendar's ID in your notepad. You will need it latter.
![Find and copy calendar ID](pictures/2022-09-11-12-58-23.png)

Congratulations! Now, you have everything to upload your OnBoard events in your new Google Calendar!
Go back to the main [README](./README.md#Installation) and choose whever to use OTGC locally or deploy Google ressources to automate everything and no longer manually connect on OnBoard to check your planning and instead use Google Calendar.

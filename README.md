# Album-List-BlueSky-Poster
[![Docker Hub](https://img.shields.io/static/v1.svg?color=086dd7&labelColor=555555&logoColor=ffffff&label=&message=docker%20hub&logo=Docker)](https://hub.docker.com/repository/docker/finiteui/album-list-bluesky-poster)

This is a BlueSky version of my [Album-List-Tweeter](https://github.com/FiniteUI/Album-List-Tweeter) project. This is a simple self hosted project to post to BlueSky when I record a new album that I've listened to.

I try to listen to a new album about once a week. Since 2018, I've kept a list of albums I've listened to in a google sheet, shown below:
![image](https://github.com/user-attachments/assets/4f29bbc5-d74b-499a-80d5-7980412b1779)


This project utilizes the Google Sheets API via [GSpread](https://github.com/burnash/gspread) to check for new records and posts them to BlueSky using the [BlueSky Python SDK](https://github.com/MarshalX/atproto).

## Example
![image](https://github.com/user-attachments/assets/aad9088d-eb3b-46dc-96ad-10acfa5d371b)

## Deployment
The project can be run locally, but was designed to be run on Docker.

The image is hosted on [Docker Hub](https://hub.docker.com/repository/docker/finiteui/album-list-bluesky-poster) and can be deployed from there.
To deploy the project on docker:
- Create a new directory and download the included [docker-compose](docker-compose.yml) file into it.
- In the directory, create a file named ```.env``` with the contents defined below.
- Copy your ```google-api.json``` file into the directory, defined below.
- In the terminal, navigate to this directory, and run ```docker compose up -d```

If the requirements are met, you should be up and running.
![image](https://github.com/user-attachments/assets/b75793fc-8391-4965-83e0-887d98cca5ff)

## ENV File
This project relies on an env file named Letterboxd-Poster.env with configuration variables to run. An example can be found [here](.env.example).
The file needs the following:
```
BLUESKY_USERNAME = Your BlueSky username
BLUESKY_APP_PASSWORD = A valid BlueSky app password
GOOGLE_SHEET_KEY = The ID for the google sheet to read from
```

## Google API Credentials
A Google API service account credentials file named ```google-api.json``` is used to access the Google Sheets API.
Instructions for generating one can be found here: https://docs.gspread.org/en/latest/oauth2.html

## BlueSky App Passwords
A BlueSky app password is used to access the BlueSky API. These can be generated here: https://bsky.app/settings/app-passwords

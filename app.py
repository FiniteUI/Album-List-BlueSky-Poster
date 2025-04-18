import dotenv
import os
import time
from datetime import datetime, timezone
from ConfigurationFile import ConfigurationFile
from AlbumList import AlbumList
from BlueSky import BlueSky

#checks for new records in a Google Sheet of albums listened to
#if a new record is found, it gets posted on Bluesky
def run():
    #if we are running on docker, envs are supplied directly. If not, we load the file
    from_docker = os.getenv('DOCKER')
    if from_docker is None:
        print("Running locally...")
        dotenv.load_dotenv('.env')
    else:
        print("Running in Docker...")

    #grab settings
    valid = True
    print('Initializing application...')

    sheet_key = os.getenv('GOOGLE_SHEET_KEY')
    if sheet_key is None or sheet_key == '':
        valid = False
        print("Error: Required key [GOOGLE_SHEET_KEY] missing from .env file.")
    else:
        print(f'Google Sheet Key: {sheet_key}')
    
    bluesky_username = os.getenv('BLUESKY_USERNAME')
    if bluesky_username is None or bluesky_username == '':
        valid = False
        print("Error: Required key [BLUESKY_USERNAME] missing from .env file.")
    else:
        print(f'BlueSky account: {bluesky_username}')
    
    bluesky_password = os.getenv('BLUESKY_APP_PASSWORD')
    if bluesky_password is None or bluesky_password == '':
        valid = False
        print("Error: Required key [BLUESKY_APP_PASSWORD] missing from .env file.")

    if valid:
        print('Configuration is valid.')
        process_loop(sheet_key, bluesky_username, bluesky_password)
    else:
        print('Could not run due to missing keys. Aborting program...')

def process_loop(sheet_key, bluesky_username, bluesky_password):
    print('Starting process loop...')
    registry = ConfigurationFile('registry')

    while True:
        print('Processing...')

        #grab last post
        last_post = registry.getValue('last_post', None)
        if last_post is None:
            last_post = datetime.now().astimezone()
            registry.setValue('last_post', last_post)
        else:
            last_post = datetime.fromisoformat(last_post)
        print(f'Last Post Timestamp: {last_post}')

        #grab last sheet entry
        row = None

        if os.getenv('DOCKER') is None:
            credentials = 'google-api.json'
        else:
            credentials = '/run/secrets/google-api-credentials'

        with AlbumList(credentials, sheet_key) as sheet:
            row = sheet.get_last_row()
        
        if row is not None:
            last_row_timestamp = row['Timestamp']
            print(f'Last Row Timestamp: {last_row_timestamp}')
            if last_row_timestamp > last_post:
                print('New record found. Sending post...')
                contents = send_post(row, bluesky_username, bluesky_password)
                registry.setValue('last_post', datetime.now().astimezone())
                registry.setValue('last_post_contents', contents)
                registry.setValue('total_posts', registry.getValue('total_posts', 0) + 1)

        registry.setValue('last_process', datetime.now().astimezone())
        
        #now wait
        print('Processing complete. Sleeping....')
        time.sleep(300)

def send_post(row, bluesky_username, bluesky_password):
    post_text = f'Just listened to the album {row['Album']} by {row['Artist']} ({row['Release_Year']}) for the first time:'
    with BlueSky(bluesky_username, bluesky_password) as bs:
        bs.post_with_link_embed(post_text, row['Link'])

    return post_text

#run program
if __name__ == '__main__':
    run()
from googleapiclient.discovery import build
import json
import os
from dotenv import load_dotenv

load_dotenv()


def main(q ="nature science cosmology 8k" , maxResults=50):
    
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for videos
    request = youtube.search().list(
        q=q,
        part='snippet',
        type='video',
        maxResults=maxResults  # Adjust as needed
    )
    response = request.execute()

    # json dump
    print('Writing to json file...')

    with open(f'search_results/{q}.json', 'w') as f:
        json.dump(response, f, indent=4)
        
    #append to txt file

    with open(f'search_results/{q}.txt', 'w') as f:
        for item in response['items']:
            video_id = item['id']['videoId']
            f.write(video_id+'\n')
    print('Done bulik fetching.')
    

if __name__ == "__main__":
    main()
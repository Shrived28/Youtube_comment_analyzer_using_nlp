import re
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time import sleep
import traceback
# import certifi
# import httplib2

# # Force httplib2 to use certifi's certs
# httplib2.CA_CERTS = certifi.where()
api_key = "AIzaSyCiOK0506q-uyqaG9lZy8b0TjWz1M5Pp50"
youtube = build('youtube', 'v3', developerKey=api_key)

def extract_vid_id(link):
    # youtube_link = "https://www.youtube.com/watch?v=OCvsEfuTA_8"
    youtube_link=link
    video_id_regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(video_id_regex, youtube_link)
    if match:
        video_id = match.group(1)
        return (video_id)
    
def get_channel_id(video_id: str) -> str | None:
    """
    Given a video ID, returns the channel ID.
    """
    try:
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['snippet']['channelId']
    except HttpError as e:
        print(f"HttpError getting channel ID: {e}")
    except Exception as e:
        print(f"Error getting channel ID: {e}")
    return None

def get_channel_info(channel_id: str) -> dict | None:
    """
    Fetches channel info like title, video count, logo url, created date, subscriber count, description.
    """
    try:
        response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        if 'items' not in response or len(response['items']) == 0:
            return None

        item = response['items'][0]

        return {
            'channel_title': item['snippet']['title'],
            'video_count': item['statistics']['videoCount'],
            'channel_logo_url': item['snippet']['thumbnails']['high']['url'],
            'channel_created_date': item['snippet']['publishedAt'],
            'subscriber_count': item['statistics'].get('subscriberCount', "Hidden"),
            'channel_description': item['snippet']['description']
        }
    except HttpError as e:
        print(f"HttpError getting channel info: {e}")
    except Exception as e:
        print(f"Error getting channel info: {e}")
    return None

def get_video_info(video_id):
    try:
        response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        return response['items'][0]['statistics']

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

  
def get_comments(vid_id):
    # vid_id = extract_vid_id(videolink)

    request = youtube.commentThreads().list(
        part = "snippet,replies",
        videoId = vid_id,
        textFormat = "plainText"
    )
    

    df = pd.DataFrame(columns=['comment','replies','date','user_name'])

    total_comments=0
    max_comments=1000

    while request and total_comments<max_comments:
        comments = []
        dates = []
        user_names =[]

        try:
            response = request.execute()
            for i in response['items']:
                comment = i['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

                user_name = i['snippet']['topLevelComment']['snippet']['authorDisplayName']
                user_names.append(user_name)

                date = i['snippet']['topLevelComment']['snippet']['publishedAt']
                dates.append(date)
                replycount = i['snippet']['totalReplyCount']

                total_comments+=1

            df2 = pd.DataFrame({"comment":comments,"user_name":user_name,"date":dates})
            df = pd.concat([df,df2],ignore_index=True)
            # df.to_csv(f"{vid_id}.csv",index = False,encoding='utf-8')
            if total_comments>=max_comments:
                break
            sleep(2)
            request = youtube.commentThreads().list_next(request, response)
            print("Iterating through next page")

        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            print("Sleeping for 5 seconds")
            sleep(5)
            # df.to_csv(f"{vid_id}.csv", index=False, encoding='utf-8')
            break
    return df

def main():
    
    # link = https://www.youtube.com/watch?v=3y5A4paFOb4 https://www.youtube.com/watch?v=lC9emrW0F2o "https://www.youtube.com/watch?v=hkb8oCMrxDg  #https://www.youtube.com/watch?v=YR12Z8f1Dh8  https://www.youtube.com/watch?v=-2RAq5o5pwc"
    link = "https://www.youtube.com/watch?v=73_1biulkYk"
    # https://www.youtube.com/watch?v=uxbQATBAXf8  https://www.youtube.com/watch?v=uxb  https://www.youtube.com/watch?v=tahjluBe--E
    get_comments(link)


if __name__ == "__main__":
    main()
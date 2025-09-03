import re
# from vid_id import extract_vid_id
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from time import sleep
import traceback

def extract_vid_id(link):
    # youtube_link = "https://www.youtube.com/watch?v=OCvsEfuTA_8"
    youtube_link=link
    video_id_regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(video_id_regex, youtube_link)
    if match:
        video_id = match.group(1)
        return (video_id)

def get_comments(api_key, videolink):
    vid_id = extract_vid_id(videolink)
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.commentThreads().list(
        part = "snippet,replies",
        videoId = vid_id,
        textFormat = "plainText"
    )
    

    df = pd.DataFrame(columns=['comment','replies','date','user_name'])

    while request:
        replies = []
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

                if replycount>0:
                    replies.append([])
                    for reply in i['replies']['comments']:
                        reply = reply['snippet']['textDisplay']

                        replies[-1].append(reply)
                else:
                    replies.append([])
                
            df2 = pd.DataFrame({"comment":comments,"replies":replies,"user_name":user_name,"date":dates})
            df = pd.concat([df,df2],ignore_index=True)
            df.to_csv(f"{vid_id}_user_comments.csv",index = False,encoding='utf-8')
            sleep(4)
            request = youtube.commentThreads().list_next(request, response)
            print("Iterating through next page")

        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            print("Sleeping for 10 seconds")
            sleep(10)
            df.to_csv(f"{vid_id}_user_comments.csv", index=False, encoding='utf-8')
            break

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    links = ["https://www.youtube.com/watch?v=uxbQATBAXf8", "https://www.youtube.com/watch?v=uxb",  "https://www.youtube.com/watch?v=tahjluBe--E","https://www.youtube.com/watch?v=73_1biulkYk",'https://www.youtube.com/watch?v=3y5A4paFOb4', "https://www.youtube.com/watch?v=lC9emrW0F2o", "https://www.youtube.com/watch?v=hkb8oCMrxDg",  "https://www.youtube.com/watch?v=YR12Z8f1Dh8", "https://www.youtube.com/watch?v=-2RAq5o5pwc"]
    for link in links:
        get_comments(api_key,link)


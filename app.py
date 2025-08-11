import streamlit as st
import os
import gdown
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import requests

# Download model if not already present
MODEL_URL = "https://drive.google.com/file/d/12zPlTmCuzd3Pza9Kyh3lfJ8ZLZ3z0lGP/view?usp=drivesdk"
if not os.path.exists("models.pkl"):
    gdown.download(MODEL_URL, "models.pkl", quiet=False)
    
from comment_scraper import extract_vid_id,get_video_info,get_comments,get_channel_id,get_channel_info,youtube,api_key
from sentiment_analysis import analyse_comments

def show_visualizations(df):
    sentiment_counts = df.value_counts()

    st.subheader("📊 Sentiment Analysis")

    st.markdown("#### Bar Chart")

    fig_bar, ax_bar = plt.subplots()
    bar_colors = ["#FF3D3D", "#4FD756"]
    sentiments = ["Negative", "Positive"]
    cnts = [sentiment_counts.get(0), sentiment_counts.get(1)]
    sns.barplot(x=sentiments, y=cnts, palette=bar_colors, ax=ax_bar)
    ax_bar.set_ylabel("Number of Comments")
    ax_bar.set_xlabel("Sentiment")
    # ax_bar.set_title("Comment Sentiment Distribution")

    st.pyplot(fig_bar)

    st.markdown("#### Pie Chart")
                
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(cnts, labels=sentiments, autopct='%1.1f%%', colors=bar_colors)
    ax_pie.axis('equal')

    st.pyplot(fig_pie)

def get_trending_videos(api_key, region="IN", max_results=5):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": max_results,
        "key": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        videos = []
        for item in data["items"]:
            video_id = item["id"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            views = int(item["statistics"]["viewCount"])
            views_formatted = f"{views:,}"  # comma-separated
            link = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                "title": title,
                "channel": channel,
                "views": views_formatted,
                "link": link
            })
        return videos
    else:
        st.sidebar.error(f"❌ API Error {response.status_code}: {response.text}")
        return []


st.set_page_config(page_title='youtube comment analyizer', page_icon = None, initial_sidebar_state = 'auto')
st.title("🎯 YouTube Sentiment Analyzer")

st.sidebar.markdown("### 🔥 Top 5 Trending Videos")
trending_videos = get_trending_videos(api_key)

if trending_videos:
    for vid in trending_videos:
        st.sidebar.markdown(f"""
        **[{vid['title']}]({vid['link']})**  
        👀 {vid['views']} views • 🎥 {vid['channel']}
        """)
        st.sidebar.divider()
else:
    st.sidebar.warning("Could not load trending videos.")


youtube_link = st.text_input("🔗 Enter YouTube Video Link")
directory_path = os.getcwd()


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# print(youtube_link)
vid_id = extract_vid_id(youtube_link)
# print(vid_id)

if vid_id:
    channel_id = get_channel_id(vid_id)
    channel_info = get_channel_info(channel_id)
    vid_info = get_video_info(vid_id)

    st.title("📺 Channel Overview")

    logo_col, info_col = st.columns([1, 3])

    with logo_col:
        logo_url = channel_info.get('channel_logo_url')
        if logo_url:
            st.image(logo_url, width=120)
        else:
            st.warning("⚠️ Channel logo not available")

    with info_col:
        st.subheader(f"📽️ {channel_info.get('channel_title', 'Unknown Channel')}")
        st.caption(f"🗓️ Created on: {channel_info['channel_created_date'][:10]}")

        # Metrics row for Subscribers and Videos
        _,col1, col2,_ = st.columns([1,7,7,5])

        with col1:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric(label="🙋 Subscribers", value=f"{int(channel_info['subscriber_count']):,}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
            st.metric(label="🎞️ Total Videos", value=f"{int(channel_info['video_count']):,}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.title("🎥 Video Information :")
    col3, col4 ,col5 = st.columns(3)

    
    with col3:
        st.metric(label="👀 Total Views", value=f"{int(vid_info['viewCount']):,}")

    with col4:
        st.metric(label="👍 Like Count", value=f"{int(vid_info['likeCount']):,}")

    with col5:
        st.metric(label="💬 Comment Count", value=f"{int(vid_info['commentCount']):,}")
        
    st.header(" ")   
    
    _, container, _ = st.columns([10, 80, 10])
    container.video(data=youtube_link)

    with st.status("Fetching comments...", expanded=False) as status:
        df_comments = get_comments(vid_id)
        status.update(label="✅ Comments fetched", state="complete")

    df_labeled = analyse_comments(df_comments)

    # Optional: save after labeling
    df_labeled.to_csv(f"{vid_id}.csv", index=False, encoding='utf-8')

    show_visualizations(df_labeled['sentiments'])

            
          






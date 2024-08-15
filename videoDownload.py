import streamlit as st #for app development
import requests #for json and shit
import json #for json parsing

st.title("Reddit Video Downloader")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

reddit_url = st.text_input(label = "Reddit URL")

if reddit_url:
    if reddit_url[len(reddit_url) - 1] == '/':
        json_url = reddit_url[:len(reddit_url) - 1] + " .json"
    else:
        json_url = reddit_url + " .json"

    json_response = requests.get(json_url, headers=headers)

    st.write(json_response)
    if json_response.status_code != 200:
        st.warning("Incorrect URL!")
    else:
        video_url = json_response.json()[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    
    with st.spinner("Fetching video..."):
        mp4_response = requests.get(video_url)
        #st.write(mp4_response)

        if mp4_response.status_code == 200:
            st.video(mp4_response.content)
            st.download_button(
                label="Download Video",
                data=mp4_response.content,
                file_name="videodownload.mp4",  # The name it will be saved as
                mime="video/mp4")
        else:
            st.error("No video found!")

else:
    st.error("No URL detected!")

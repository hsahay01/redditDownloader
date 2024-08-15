import streamlit as st
import requests
import json

st.title("Reddit Video Downloader")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

reddit_url = st.text_input(label="Reddit URL")

if reddit_url:
    if reddit_url.endswith('/'):
        json_url = reddit_url.rstrip('/') + '.json'
    else:
        json_url = reddit_url + '.json'

    json_response = requests.get(json_url, headers=headers)

    if json_response.status_code != 200:
        st.warning("Incorrect URL or Unable to fetch data!")
    else:
        try:
            data = json_response.json()[0]['data']['children'][0]['data']
            video_url = data.get('secure_media', {}).get('reddit_video', {}).get('fallback_url')

            if video_url:
                with st.spinner("Fetching video..."):
                    mp4_response = requests.get(video_url)

                    if mp4_response.status_code == 200:
                        st.video(mp4_response.content)
                        st.download_button(
                            label="Download Video",
                            data=mp4_response.content,
                            file_name="videodownload.mp4",  # The name it will be saved as
                            mime="video/mp4"
                        )
                    else:
                        st.error("Failed to fetch video!")
            else:
                st.error("No video found in the URL!")

        except (KeyError, IndexError, TypeError) as e:
            st.error(f"Error processing data: {e}")
else:
    st.error("No URL detected!")

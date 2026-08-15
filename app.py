import os
import time
import tempfile
import yt_dlp
import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bulk Instagram Downloader",
    page_icon="📥",
    layout="wide",
)

# --- TITLE & HEADER ---
st.title("📥 Bulk Instagram Downloader")
st.caption("Paste multiple Instagram Reel links (one per line) to fetch download options.")

# --- HELPER FUNCTIONS ---
def get_video_info(url):
    """Fetches video metadata and download links using yt_dlp"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        return {"error": str(e)}

# --- MAIN INPUT SECTION ---
input_container = st.container(border=True)

with input_container:
    reel_urls = st.text_area(
        "Paste Instagram Reel URLs (one per line):",
        placeholder="https://www.instagram.com/reel/...\nhttps://www.instagram.com/reel/...",
        height=150
    )
    
    fetch_btn = st.button("🚀 Fetch Download Options", type="primary")

# --- PROCESSING TRIGGER ---
if fetch_btn:
    links = [line.strip() for line in reel_urls.split('\n') if line.strip()]
    if not links:
        st.warning("⚠️ Please enter at least one URL.")
    else:
        results = []
        with st.spinner("Fetching information..."):
            for link in links:
                info = get_video_info(link)
                results.append((link, info))
        
        st.divider()
        for link, info in results:
            if "error" in info:
                st.error(f"Error for {link}: {info['error']}")
            else:
                st.subheader(f"Video: {info.get('title', 'Unknown')}")
                st.video(info.get('url'))
                
                # Download logic
                video_url = info.get('url')
                if video_url:
                    st.download_button(
                        label=f"⬇️ Download {info.get('title', 'Video')[:20]}",
                        data=requests.get(video_url).content,
                        file_name=f"{info.get('id', 'video')}.mp4",
                        mime="video/mp4"
                    )
                st.write(f"Duration: {info.get('duration_string')}")


import streamlit as st
from yt_dlp import YoutubeDL
import tempfile
import os

# Page configuration
st.set_page_config(page_title="Universal Video Downloader", layout="wide", page_icon="🎥")

# Custom CSS for better UI
st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f2f6;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 0.6em;
        font-size: 1em;
    }
    footer {
        visibility: hidden;
    }
    .footer-text {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 0.9em;
        color: #888;
        padding: 0.5em 0;
        background: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("YT Video Downloader")
st.write("Paste the URL below and click Download to save the video instantly without redirects.")

data_url = st.text_input("Enter Video URL:")

if st.button("Download"):
    if not data_url.strip():
        st.error("❗ Please enter a valid URL.")
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'format': 'best[ext=mp4]/best',  # Prefer MP4
                'quiet': True,
                'noprogress': True,
            }
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(data_url, download=True)
                    filename = ydl.prepare_filename(info)

                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        video_bytes = f.read()
                    
                    st.success(f"✅ Downloaded: {os.path.basename(filename)}")
                    st.download_button(
                        label="⬇️ Click to Save Video",
                        data=video_bytes,
                        file_name=os.path.basename(filename),
                        mime='video/mp4'
                    )
                else:
                    st.error("❌ Video file was not found after download.")
            except Exception as e:
                st.error(f"❌ Download failed: {e}")

# Footer
st.markdown(
    "<div class='footer-text'>🎬 Made by Muhammad Samad</div>",
    unsafe_allow_html=True
)
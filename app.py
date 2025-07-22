import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import shutil
import random

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="YT Downloader",
    layout="centered",
    page_icon="🎥",
    initial_sidebar_state="collapsed"
)

# CSS for mobile responsiveness
st.markdown("""
<style>
    /* Main content padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        font-size: 16px !important;
        padding: 12px !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    /* Download button specific */
    .download-btn>button {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: white;
        color: #888;
        z-index: 100;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .stTextInput>div>div>input {
            font-size: 14px !important;
        }
        .stButton>button {
            font-size: 14px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Mobile user agents
MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
]

# Title with mobile-friendly layout
st.title("🎥 YouTube Video Downloader")
st.markdown("Paste a YouTube URL below to download the MP4 video directly to your device")
st.markdown("📱 **Mobile tip**: Long press the download button and choose 'Save'")

# Input field with clear placeholder
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Download button
if st.button("Download Video", use_container_width=True):
    if not url.strip():
        st.error("❗ Please enter a valid YouTube URL")
    else:
        tmpdir = tempfile.mkdtemp()
        try:
            with st.spinner("⏳ Downloading... This may take a moment"):
                ydl_opts = {
                    'format': 'best[ext=mp4]',
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'noprogress': True,
                    'retries': 3,
                    'http_headers': {
                        'User-Agent': random.choice(MOBILE_USER_AGENTS),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Referer': 'https://www.youtube.com/',
                    }
                }

                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    video_data = f.read()
                
                display_name = os.path.splitext(os.path.basename(filename))[0]
                
                st.success(f"✅ Download complete: {display_name}")
                st.caption("Tap below to save video to your device")
                
                st.download_button(
                    label="💾 Save Video",
                    data=video_data,
                    file_name=os.path.basename(filename),
                    mime='video/mp4',
                    use_container_width=True,
                    key="download_button",
                    help="Long press and choose 'Save' on mobile devices"
                )
            else:
                st.error("❌ File not found after download")
        except Exception as e:
            st.error(f"❌ Download failed: {str(e)}")
            st.info("ℹ️ If this keeps happening, try again later or use a different network")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

# Mobile-friendly footer
st.markdown(
    "<div class='footer'>📽️ Made by Muhammad Samad</div>",
    unsafe_allow_html=True
)
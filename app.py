import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import shutil
import random
import re

st.set_page_config(
    page_title="Social Media Downloader",
    layout="centered",
    page_icon="📱",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* General Layout Tweaks */
.block-container {
    padding-top: 1rem;
    padding-bottom: 5rem;
}

.stTextInput > div > div > input {
    font-size: 16px !important;
    padding: 12px !important;
}

.stButton > button {
    width: 100%;
    padding: 12px !important;
    font-size: 16px !important;
    margin: 5px 0;
}

.stRadio > div {
    flex-direction: row !important;
    gap: 10px;
}

.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 16px 20px;
    background: linear-gradient(to right, #ffffff, #f9f9f9);
    color: #555;
    font-size: 14px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    border-top: 1px solid #ddd;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
    z-index: 100;
    transition: all 0.3s ease-in-out;
}

@media (max-width: 768px) {
    .stTextInput > div > div > input {
        font-size: 14px !important;
        padding: 10px !important;
    }
    .stButton > button {
        font-size: 14px !important;
        padding: 10px !important;
    }
    .stRadio > div {
        gap: 5px;
    }
}
</style>
""", unsafe_allow_html=True)

USER_AGENTS = {
    'youtube': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ],
    'instagram': [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Instagram 219.0.0.12.117 Android (29/10; 480dpi; 1080x2137; Google/google; Pixel 4; flame; flame; en_US)'
    ]
}


def clean_filename(filename):
    """Remove special characters from filename"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def is_valid_url(url, platform):
    """Validate URL format"""
    if platform == "youtube":
        return re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+', url)
    elif platform == "instagram":
        return re.match(r'^(https?://)?(www\.)?instagram\.com/(p|reel)/.+', url)
    return False


st.title("📱 Social Media Downloader")
st.markdown(
    "Download videos from YouTube or Instagram (Reels) directly to your device")

platform = st.radio("Select platform:", ("YouTube",
                    "Instagram"), horizontal=True)


placeholder = {
    "YouTube": "https://www.youtube.com/watch?v=...",
    "Instagram": "https://www.instagram.com/reel/..."
}
url = st.text_input(f"Enter {platform} URL:",
                    placeholder=placeholder[platform])

if st.button("Download Video", key="download_btn", use_container_width=True):
    if not url.strip():
        st.error("❗ Please enter a valid URL")
    else:
        platform_key = platform.lower()
        if not is_valid_url(url, platform_key):
            st.error(f"❗ Please enter a valid {platform} URL")
        else:
            tmpdir = tempfile.mkdtemp()
            try:
                with st.spinner("⏳ Downloading... Please wait"):
                    ydl_opts = {
                        'format': 'best[ext=mp4]',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'quiet': True,
                        'noprogress': True,
                        'retries': 3,
                        'http_headers': {
                            'User-Agent': random.choice(USER_AGENTS[platform_key]),
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Referer': 'https://www.' + ('youtube.com' if platform_key == 'youtube' else 'instagram.com'),
                        }
                    }

                    if platform_key == 'instagram':
                        ydl_opts.update({
                            'extract_flat': False,
                            'force_generic_extractor': True,
                        })

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        clean_name = clean_filename(os.path.basename(filename))

                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        video_data = f.read()

                    st.success(f"✅ Download complete!")
                    st.caption(
                        "📱 Mobile users: Long press the button below and select 'Save'")

                    st.download_button(
                        label="💾 Save Video",
                        data=video_data,
                        file_name=clean_name,
                        mime='video/mp4',
                        use_container_width=True,
                        key="final_download",
                    )
                else:
                    st.error("❌ File not found after download")
            except Exception as e:
                st.error(f"❌ Download failed: {str(e)}")
                st.info(
                    "💡 Try again later or use a different network if this persists")
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)

st.markdown(
    """
    <div class='footer'>
        ✨ Made by Muhammad Samad
    </div>
    """,
    unsafe_allow_html=True
)

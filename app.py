import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import shutil
import random
import re

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="Social Media Downloader",
    layout="centered",
    page_icon="📱",
    initial_sidebar_state="collapsed"
)

# CSS for mobile responsiveness
st.markdown("""
<style>
    /* Main content padding */
    .block-container {
        padding-top: 1rem;
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
        margin: 5px 0;
    }
    
    /* Platform selector */
    .stRadio>div {
        flex-direction: row!important;
        gap: 10px;
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
        border-top: 1px solid #eee;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        .stTextInput>div>div>input {
            font-size: 14px !important;
            padding: 10px !important;
        }
        .stButton>button {
            font-size: 14px !important;
            padding: 10px !important;
        }
        .stRadio>div {
            gap: 5px;
        }
    }
</style>
""", unsafe_allow_html=True)

# User agents for different platforms
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

# Main app
st.title("📱 Social Media Downloader")
st.markdown("Download videos from YouTube or Instagram (Reels) directly to your device")

# Platform selection
platform = st.radio("Select platform:", ("YouTube", "Instagram"), horizontal=True)

# Input field with dynamic placeholder
placeholder = {
    "YouTube": "https://www.youtube.com/watch?v=...",
    "Instagram": "https://www.instagram.com/reel/..."
}
url = st.text_input(f"Enter {platform} URL:", placeholder=placeholder[platform])

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

                    # Special options for Instagram
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
                    st.caption("📱 Mobile users: Long press the button below and select 'Save'")
                    
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
                st.info("💡 Try again later or use a different network if this persists")
            finally:
                shutil.rmtree(tmpdir, ignore_errors=True)

# Footer with additional info
st.markdown(
    """
    <div class='footer'>
        📽️ Supports YouTube videos and Instagram Reels<br>
        ✨ Made by Muhammad Samad
    </div>
    """,
    unsafe_allow_html=True
)




# import streamlit as st
# from yt_dlp import YoutubeDL
# import os
# import tempfile
# import shutil
# import random

# st.set_page_config(
#     page_title="YT Downloader",
#     layout="centered",
#     page_icon="🎥",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 5rem;
#     }
    
#     .stTextInput>div>div>input {
#         font-size: 16px !important;
#         padding: 12px !important;
#     }
    
#     .stButton>button {
#         width: 100%;
#         padding: 12px !important;
#         font-size: 16px !important;
#     }
    
#     .download-btn>button {
#         background-color: #4CAF50 !important;
#         color: white !important;
#     }
    
#     .footer {
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         text-align: center;
#         padding: 10px;
#         background: white;
#         color: #888;
#         z-index: 100;
#     }
    
#     @media (max-width: 768px) {
#         .stTextInput>div>div>input {
#             font-size: 14px !important;
#         }
#         .stButton>button {
#             font-size: 14px !important;
#         }
#     }
# </style>
# """, unsafe_allow_html=True)

# MOBILE_USER_AGENTS = [
#     'Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
#     'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
# ]

# st.title("🎥 YouTube Video Downloader")
# st.markdown(
#     "Paste a YouTube URL below to download the MP4 video directly to your device")
# st.markdown("📱 **Mobile tip**: Long press the download button and choose 'Save'")

# url = st.text_input("Enter YouTube URL:",
#                     placeholder="https://www.youtube.com/watch?v=...")

# if st.button("Download Video", use_container_width=True):
#     if not url.strip():
#         st.error("❗ Please enter a valid YouTube URL")
#     else:
#         tmpdir = tempfile.mkdtemp()
#         try:
#             with st.spinner("⏳ Downloading... This may take a moment"):
#                 ydl_opts = {
#                     'format': 'best[ext=mp4]',
#                     'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
#                     'quiet': True,
#                     'noprogress': True,
#                     'retries': 3,
#                     'http_headers': {
#                         'User-Agent': random.choice(MOBILE_USER_AGENTS),
#                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                         'Accept-Language': 'en-US,en;q=0.5',
#                         'Referer': 'https://www.youtube.com/',
#                     }
#                 }

#                 with YoutubeDL(ydl_opts) as ydl:
#                     info = ydl.extract_info(url, download=True)
#                     filename = ydl.prepare_filename(info)

#             if os.path.exists(filename):
#                 with open(filename, 'rb') as f:
#                     video_data = f.read()

#                 display_name = os.path.splitext(os.path.basename(filename))[0]

#                 st.success(f"✅ Download complete: {display_name}")
#                 st.caption("Tap below to save video to your device")

#                 st.download_button(
#                     label="💾 Save Video",
#                     data=video_data,
#                     file_name=os.path.basename(filename),
#                     mime='video/mp4',
#                     use_container_width=True,
#                     key="download_button",
#                     help="Long press and choose 'Save' on mobile devices"
#                 )
#             else:
#                 st.error("❌ File not found after download")
#         except Exception as e:
#             st.error(f"❌ Download failed: {str(e)}")
#             st.info(
#                 "ℹ️ If this keeps happening, try again later or use a different network")
#         finally:
#             shutil.rmtree(tmpdir, ignore_errors=True)

# st.markdown(
#     "<div class='footer'>📽️ Made by Muhammad Samad</div>",
#     unsafe_allow_html=True
# )

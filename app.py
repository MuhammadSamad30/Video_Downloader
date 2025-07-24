import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import shutil
import random
import re

# Page configuration with modern design
st.set_page_config(
    page_title="Universal Media Downloader",
    layout="centered",
    page_icon="📥",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with modern styling
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
    border-radius: 8px !important;
    border: 1px solid #ddd !important;
}

.stButton > button {
    width: 100%;
    padding: 12px !important;
    font-size: 16px !important;
    margin: 10px 0;
    border-radius: 8px !important;
    background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%) !important;
    color: white !important;
    border: none !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.stRadio > div {
    flex-direction: row !important;
    gap: 10px;
    margin-bottom: 15px;
}

.stRadio > label {
    font-weight: 600 !important;
    color: #333 !important;
}

/* Platform cards styling */
.platform-card {
    border-radius: 12px;
    padding: 15px;
    margin: 8px 0;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    transition: all 0.3s ease;
}

.platform-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    border-color: #dee2e6;
}

/* Footer styling */
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

.footer:hover {
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
}

/* Mobile-specific adjustments */
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
        flex-wrap: wrap;
    }
    .platform-card {
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# User agents for all platforms
USER_AGENTS = {
    'youtube': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ],
    'instagram': [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Instagram 219.0.0.12.117 Android (29/10; 480dpi; 1080x2137; Google/google; Pixel 4; flame; flame; en_US)'
    ],
    'tiktok': [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
    ],
    'facebook': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    ]
}

def clean_filename(filename):
    """Remove special characters from filename"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def is_valid_url(url, platform):
    """Validate URL format for all platforms"""
    patterns = {
        'youtube': r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
        'instagram': r'^(https?://)?(www\.)?instagram\.com/(p|reel)/.+',
        'tiktok': r'^(https?://)?(www\.)?tiktok\.com/.+/video/.+',
        'facebook': r'^(https?://)?(www\.)?facebook\.com/.+/videos/.+'
    }
    return re.match(patterns.get(platform, ''), url) is not None

def get_platform_key(platform_name):
    """Convert platform display name to key"""
    return platform_name.lower()

# Main app with enhanced UI
st.title("📥 Universal Media Downloader")
st.markdown("Download videos from multiple platforms directly to your device")

# Platform selection with cards
st.subheader("Select Platform")
platform = st.radio("", ("YouTube", "Instagram", "TikTok", "Facebook"), 
                   horizontal=True, label_visibility="collapsed")

# Platform information cards
platform_info = {
    "YouTube": "Supports standard YouTube videos and shorts",
    "Instagram": "Works with Reels and standard Instagram posts",
    "TikTok": "Download any public TikTok video",
    "Facebook": "Supports public Facebook videos and reels"
}

st.markdown(f"""
<div class="platform-card">
    <strong>{platform}</strong>
    <div style="font-size: 14px; color: #666; margin-top: 5px;">
        {platform_info[platform]}
    </div>
</div>
""", unsafe_allow_html=True)

# Input field with dynamic placeholder
placeholder_map = {
    "YouTube": "https://www.youtube.com/watch?v=...",
    "Instagram": "https://www.instagram.com/reel/...",
    "TikTok": "https://www.tiktok.com/@username/video/...",
    "Facebook": "https://www.facebook.com/username/videos/..."
}

url = st.text_input(f"Enter {platform} URL:", 
                   placeholder=placeholder_map[platform],
                   key="url_input")

# Download button
if st.button("Download Video", key="download_btn", use_container_width=True):
    if not url.strip():
        st.error("❗ Please enter a valid URL")
    else:
        platform_key = get_platform_key(platform)
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
                            'Referer': 'https://www.' + platform_key + '.com',
                        }
                    }

                    # Platform-specific configurations
                    if platform_key == 'instagram':
                        ydl_opts.update({
                            'extract_flat': False,
                            'force_generic_extractor': True,
                        })
                    elif platform_key == 'tiktok':
                        ydl_opts.update({
                            'referer': 'https://www.tiktok.com/',
                        })
                    elif platform_key == 'facebook':
                        ydl_opts.update({
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

                    # Platform-specific file naming
                    file_ext = "mp4"
                    mime_type = "video/mp4"
                    
                    st.download_button(
                        label="💾 Save Video",
                        data=video_data,
                        file_name=clean_name,
                        mime=mime_type,
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

# Footer with platform icons
st.markdown(
    """
    <div class='footer'>
        <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 5px;">
            <span>📺 YouTube</span>
            <span>📸 Instagram</span>
            <span>🎵 TikTok</span>
            <span>👥 Facebook</span>
        </div>
        <div>✨ Made by Muhammad Samad</div>
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
# import re

# st.set_page_config(
#     page_title="Social Media Downloader",
#     layout="centered",
#     page_icon="📱",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
# /* General Layout Tweaks */
# .block-container {
#     padding-top: 1rem;
#     padding-bottom: 5rem;
# }

# .stTextInput > div > div > input {
#     font-size: 16px !important;
#     padding: 12px !important;
# }

# .stButton > button {
#     width: 100%;
#     padding: 12px !important;
#     font-size: 16px !important;
#     margin: 5px 0;
# }

# .stRadio > div {
#     flex-direction: row !important;
#     gap: 10px;
# }

# .footer {
#     position: fixed;
#     bottom: 0;
#     left: 0;
#     width: 100%;
#     text-align: center;
#     padding: 16px 20px;
#     background: linear-gradient(to right, #ffffff, #f9f9f9);
#     color: #555;
#     font-size: 14px;
#     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     border-top: 1px solid #ddd;
#     box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
#     z-index: 100;
#     transition: all 0.3s ease-in-out;
# }

# @media (max-width: 768px) {
#     .stTextInput > div > div > input {
#         font-size: 14px !important;
#         padding: 10px !important;
#     }
#     .stButton > button {
#         font-size: 14px !important;
#         padding: 10px !important;
#     }
#     .stRadio > div {
#         gap: 5px;
#     }
# }
# </style>
# """, unsafe_allow_html=True)

# USER_AGENTS = {
#     'youtube': [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
#     ],
#     'instagram': [
#         'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
#         'Instagram 219.0.0.12.117 Android (29/10; 480dpi; 1080x2137; Google/google; Pixel 4; flame; flame; en_US)'
#     ]
# }


# def clean_filename(filename):
#     """Remove special characters from filename"""
#     return re.sub(r'[\\/*?:"<>|]', "", filename)


# def is_valid_url(url, platform):
#     """Validate URL format"""
#     if platform == "youtube":
#         return re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+', url)
#     elif platform == "instagram":
#         return re.match(r'^(https?://)?(www\.)?instagram\.com/(p|reel)/.+', url)
#     return False


# st.title("📱 Social Media Downloader")
# st.markdown(
#     "Download videos from YouTube or Instagram (Reels) directly to your device")

# platform = st.radio("Select platform:", ("YouTube",
#                     "Instagram"), horizontal=True)


# placeholder = {
#     "YouTube": "https://www.youtube.com/watch?v=...",
#     "Instagram": "https://www.instagram.com/reel/..."
# }
# url = st.text_input(f"Enter {platform} URL:",
#                     placeholder=placeholder[platform])

# if st.button("Download Video", key="download_btn", use_container_width=True):
#     if not url.strip():
#         st.error("❗ Please enter a valid URL")
#     else:
#         platform_key = platform.lower()
#         if not is_valid_url(url, platform_key):
#             st.error(f"❗ Please enter a valid {platform} URL")
#         else:
#             tmpdir = tempfile.mkdtemp()
#             try:
#                 with st.spinner("⏳ Downloading... Please wait"):
#                     ydl_opts = {
#                         'format': 'best[ext=mp4]',
#                         'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
#                         'quiet': True,
#                         'noprogress': True,
#                         'retries': 3,
#                         'http_headers': {
#                             'User-Agent': random.choice(USER_AGENTS[platform_key]),
#                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                             'Accept-Language': 'en-US,en;q=0.5',
#                             'Referer': 'https://www.' + ('youtube.com' if platform_key == 'youtube' else 'instagram.com'),
#                         }
#                     }

#                     if platform_key == 'instagram':
#                         ydl_opts.update({
#                             'extract_flat': False,
#                             'force_generic_extractor': True,
#                         })

#                     with YoutubeDL(ydl_opts) as ydl:
#                         info = ydl.extract_info(url, download=True)
#                         filename = ydl.prepare_filename(info)
#                         clean_name = clean_filename(os.path.basename(filename))

#                 if os.path.exists(filename):
#                     with open(filename, 'rb') as f:
#                         video_data = f.read()

#                     st.success(f"✅ Download complete!")
#                     st.caption(
#                         "📱 Mobile users: Long press the button below and select 'Save'")

#                     st.download_button(
#                         label="💾 Save Video",
#                         data=video_data,
#                         file_name=clean_name,
#                         mime='video/mp4',
#                         use_container_width=True,
#                         key="final_download",
#                     )
#                 else:
#                     st.error("❌ File not found after download")
#             except Exception as e:
#                 st.error(f"❌ Download failed: {str(e)}")
#                 st.info(
#                     "💡 Try again later or use a different network if this persists")
#             finally:
#                 shutil.rmtree(tmpdir, ignore_errors=True)

# st.markdown(
#     """
#     <div class='footer'>
#         ✨ Made by Muhammad Samad
#     </div>
#     """,
#     unsafe_allow_html=True
# )

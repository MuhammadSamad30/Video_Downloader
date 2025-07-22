import streamlit as st
from yt_dlp import YoutubeDL
import os
import tempfile
import shutil

# Page configuration
st.set_page_config(page_title="YT Downloader", layout="wide", page_icon="🎥")

# Title
st.title("🎥 YouTube Video Downloader")
st.write("Paste a YouTube URL below, choose format, and download it easily — even on mobile!")

# Input
url = st.text_input("Enter YouTube Video URL:")

# Download button
if st.button("Download"):
    if not url.strip():
        st.error("❗ Please enter a valid YouTube URL.")
    else:
        tmpdir = tempfile.mkdtemp()  # Persistent temp dir
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
            'quiet': True,
            'noprogress': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    video_data = f.read()

                st.success(f"✅ Downloaded: {os.path.basename(filename)}")
                st.info("📱 On mobile? Long press the button below and choose **Download Link** or **Open in New Tab**.")

                st.download_button(
                    st.spinner("⬇️ downloading..."),
                    label="⬇️ Save Video Now",
                    data=video_data,
                    file_name=os.path.basename(filename),
                    mime='application/octet-stream'  # Force download behavior
                )
            else:
                st.error("❌ File not found after download.")
        except Exception as e:
            st.error(f"❌ Download failed: {e}")
        finally:
            # Cleanup
            shutil.rmtree(tmpdir, ignore_errors=True)

# Footer
st.markdown(
    "<div style='position: fixed; bottom: 0; width: 100%; text-align: center; color: #888;'>📽️ Made by Muhammad Samad</div>",
    unsafe_allow_html=True
)

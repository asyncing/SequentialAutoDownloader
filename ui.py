import streamlit as st
import time
from main import downloader
st.title("Optimized Downloader")
urls_input=st.text_area("Paste download links here (one per line):", height=150)

if st.button("Download File") and urls_input:
    url_list=urls_input.split('\n')
    url_list=[link.strip() for link in url_list if link.strip()]
    st.write(f"Found {len(url_list)} links. Starting sequential download...")
    start_time=time.time()
    current_file_text=st.empty()
    status_text=st.empty()
    progress_bar=st.progress(0)
    def update_ui(downloaded, total):
        if total>0:
            percentage=downloaded/total
            progress_bar.progress(percentage)
            status_text.text(f"Downloading... {downloaded / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB")
        else:
            status_text.text(f"Downloading... {downloaded / (1024 * 1024):.2f} MB")
    for index, url in enumerate(url_list):
        current_file_text.markdown(f"**Downloading {index + 1} of {len(url_list)}:** `{url}`")
        progress_bar.progress(0)
        status_text.text("Connecting...")
        downloader(url, progress_callback=update_ui)
    current_file_text.empty()
    status_text.empty()
    progress_bar.empty()
    end_time=time.time()
    st.success(f"All Downloads Completed in {int(end_time-start_time)} seconds")


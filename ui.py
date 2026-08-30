import streamlit as st

from main import downloader
st.title("Optimized Downloader")
url=st.text_input("Paste your download link here:")
if st.button("Download File"):
    if url:
        st.write("Starting Download...")
        status_text=st.empty()
        progress_bar=st.progress(0)
    else:
        st.warning("Please enter a URL first")
    def update_ui(downloaded, total):
        if total>0:
            percentage=downloaded/total
            progress_bar.progress(percentage)
            status_text.text(f"Downloading... {downloaded / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB")
        else:
            status_text.text(f"Downloading... {downloaded / (1024 * 1024):.2f} MB")
    downloader(url,progress_callback=update_ui)
    st.success("Download Complete")


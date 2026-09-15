import streamlit as st
from main import get_file_info, process_download

st.title("Optimized Downloader")
st.write("Paste a link and press **Enter**")

if "links" not in st.session_state:
    st.session_state.links = [""]

if "filenames" not in st.session_state:
    st.session_state.filenames = {}

for i in range(len(st.session_state.links)):
    current_url = st.session_state.links[i].strip()

    if current_url != "" and current_url not in st.session_state.filenames:
        try:
            with st.spinner("Fetching file info..."):
                response, filename = get_file_info(current_url)
                response.close()
                st.session_state.filenames[current_url] = filename
        except Exception:
            st.session_state.filenames[current_url] = "Unknown / Connection Error"

    if current_url in st.session_state.filenames:
        st.markdown(f"**{st.session_state.filenames[current_url]}**")

    st.session_state.links[i] = st.text_input(
        label=f"Link {i + 1}",
        value=st.session_state.links[i],
        key=f"input_{i}"
    )

if st.session_state.links[-1].strip() != "":
    st.session_state.links.append("")
    st.rerun()

valid_urls = [link.strip() for link in st.session_state.links if link.strip()]

if st.button("Download All") and valid_urls:
    st.write(f"Starting batch download for {len(valid_urls)} files...")

    for url in valid_urls:
        with st.container(border=True):
            st.write(f"🔗 `{url}`")

            cached_name = st.session_state.filenames.get(url, "downloaded_file")

            filename_text = st.empty()
            status_text = st.empty()
            progress_bar = st.progress(0)

            try:
                filename_text.markdown(f"**Saving as:** `{cached_name}`")
                status_text.text("Connecting to server...")

                response, filename = get_file_info(url)


                def update_ui(downloaded, total):
                    if total > 0:
                        percentage = downloaded / total
                        progress_bar.progress(percentage)
                        status_text.text(
                            f"Downloading... {downloaded / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB")
                    else:
                        status_text.text(f"Downloading... {downloaded / (1024 * 1024):.2f} MB")


                process_download(response, filename, progress_callback=update_ui)
                status_text.text("Complete!")

            except Exception as e:
                filename_text.error(f"Failed to connect: {e}")

    st.success("All downloads finished!")
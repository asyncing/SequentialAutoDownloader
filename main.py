import os
import re
import mimetypes
from urllib.parse import urlparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_file_info(url):

    try:
        response = requests.get(url, stream=True, timeout=10, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.SSLError:
        response = requests.get(url, stream=True, timeout=10, verify=False, headers=HEADERS)
        response.raise_for_status()


    filename = ""
    cd = response.headers.get('content-disposition')
    if cd:
        matches = re.findall('filename="?([^"]+)"?', cd)
        if matches:
            filename = matches[0]

    if not filename:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

    if not filename:
        filename = "downloaded_file"

    if '.' not in filename:
        content_type = response.headers.get('content-type', '').split(';')[0]
        extension = mimetypes.guess_extension(content_type)
        if extension:
            filename += extension

    return response, filename


def process_download(response, filename, progress_callback=None):

    save_dir = "Downloads"
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
                if progress_callback:
                    progress_callback(downloaded_size, total_size)
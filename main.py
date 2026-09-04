import os
import re
import requests
import urllib3
import mimetypes
from urllib.parse import urlparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def downloader(url, progress_callback=None):
    download_dir = "Downloads"
    os.makedirs(download_dir, exist_ok=True)
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        try:
            response=requests.get(url,stream=True, timeout=10)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            print("Invalid/Expired SSL certificate detected. Bypassing...")
            response=requests.get(url, stream=True, timeout=10, verify=False)
            response.raise_for_status()
        filename=""
        cd=response.headers.get("content-disposition")
        if cd:
            matches=re.findall('filename="?([^"]+)"?', cd)
            if matches:
                filename=matches[0]
        if not filename:
            parsed_url=urlparse(url)
            filename=os.path.basename(parsed_url.path)
        if not filename:
            parsed_url=urlparse(url)
            filename=os.path.basename(parsed_url.path)
        if not filename:
            filename="downloaded_file"
        if "." not in filename:
            content_type=response.headers.get('content-type', '').split(';')[0]
            extension=mimetypes.guess_extension(content_type)
            if extension:
                filename=filename+extension
        filepath=os.path.join(download_dir, filename)
        print(f"Downloading to:{filepath}")
        total_size=int(response.headers.get("content-length", 0))
        downloaded_size=0
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size=downloaded_size+len(chunk)
        print("\nDownload Complete")
    except requests.exceptions.ConnectionError:
        print("\n[Error] Network connection failed. Check your internet or firewall.")
    except requests.exceptions.Timeout:
        print("\n[Error] The server took too long to respond.")
    except requests.exceptions.RequestException as e:
        print(f"\n[Error] Download failed: {e}")
if __name__=="__main__":
    url=str(input("Enter an url to download:"))
    downloader(url)









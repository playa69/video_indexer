import urllib.request
import uuid

def download_video(src_url):
    download_path = "tmp/" + str(uuid.uuid4()) + ".mp4"
    urllib.request.urlretrieve(src_url, download_path)
    return download_path

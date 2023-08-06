# Convert website to text file
from trafilatura import fetch_url, extract

def web_to_text(url):
    downloaded = fetch_url(url)
    result = extract(downloaded)
    return result
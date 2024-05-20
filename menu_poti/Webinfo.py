import requests
from bs4 import BeautifulSoup

# Base class to handle web requests
class WebInfo:
    def __init__(self):
        self.url = None  # URL will be set in subclasses

    def fetch_content(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.content

    def parse_content(self, content):
        raise NotImplementedError("Subclasses should implement this!")

# Subclass to handle song name requests from a radio channel
class WebSongInfo(WebInfo):
    def __init__(self, radio_name: str):
        super().__init__()
        self.radio_name = radio_name
        self.url = f"https://onlineradiobox.com/at/{self.radio_name}/playlist/?lang=en"

    def parse_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        song = soup.find("td", class_="track_history_item")
        return song.text.strip() if song else "Unknown"


if __name__ == "__main__":
    # Example usage
    fm4_info = WebSongInfo("fm4")
    oe1_info = WebSongInfo("oe1")

    # Fetch and print FM4 song
    fm4_content = fm4_info.fetch_content()
    fm4_song = fm4_info.parse_content(fm4_content)
    print("FM4 Song:", fm4_song)

    # Fetch and print Ö1 song
    oe1_content = oe1_info.fetch_content()
    oe1_song = oe1_info.parse_content(oe1_content)
    print("Ö1 Song:", oe1_song)

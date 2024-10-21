
import requests
import json
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

class WebWeatherInfo(WebInfo):
    def __init__(self, lat: str, lon: str):
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.api_key = "cb720f2cad0ef8859bdd56acf510a560"
        self.url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}"

    def parse_content(self, content):
        # Convert the byte string to a string and then parse the JSON
        data = json.loads(content.decode('utf-8'))

        # Extract relevant information
        weather = data['weather'][0].get('description', 'No description').capitalize()
        temp_celsius = data['main'].get('temp', 0) - 273.15
        wind_speed = data['wind'].get('speed', 0)
        wind_deg = data['wind'].get('deg', 0)

        # Convert wind degrees to cardinal direction
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind_dir = directions[int((wind_deg % 360) / 45)]

        # Create the output string
        return f"{weather}, {temp_celsius:.1f}°C, Wind: {wind_speed} m/s {wind_dir}"


class WebTagesschauInfo(WebInfo):
    def __init__(self,):
        super().__init__()
        self.url = f"https://www.tagesschau.de/api2u/homepage/"

    def parse_content(self, content):
        news = json.loads(content.decode('utf-8')).get('news')
        breaking_news = [item for item in news if item.get('breakingNews')]
        if len(breaking_news) > 0:
            news = breaking_news
        titles = ", ".join([news['title'] for news in news])
        return titles

if __name__ == "__main__":
    # Example usage
    #fm4_info = WebSongInfo("fm4")
    #oe1_info = WebSongInfo("oe1")

    # Fetch and print FM4 song
    #fm4_content = fm4_info.fetch_content()
    #fm4_song = fm4_info.parse_content(fm4_content)
    #print("FM4 Song:", fm4_song)

    # Fetch and print Ö1 song
    #oe1_content = oe1_info.fetch_content()
    #oe1_song = oe1_info.parse_content(oe1_content)
    #print("Ö1 Song:", oe1_song)

    #linz_weather = WebWeatherInfo("48.3064", "14.2861")
    #linz_content = linz_weather.fetch_content()
    #linz_weather_string = linz_weather.parse_content(linz_content)
    #print(linz_weather_string)

    tagesschau = WebTagesschauInfo()
    tagesschau_content = tagesschau.fetch_content()
    tagesschau_string = tagesschau.parse_content(tagesschau_content)

    print(tagesschau_string)

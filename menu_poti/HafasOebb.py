# ÖBB HAFAS API client
from Webinfo import WebInfo
import json
from datetime import datetime

class OebbHafasClient(WebInfo):
    def __init__(self):
        super().__init__()
        self.url = f"http://localhost:2999/"

    def fetch_content(self):
        # Override fetch_content to add API key or other authentication if needed
        # Example: response = requests.get(self.url, headers={"Authorization": "Bearer YOUR_API_KEY"})
        response = super().fetch_content()
        return response

    def parse_content(self, content):
        # Implement parsing logic for ÖBB HAFAS API response
        journey_details = []
        # Your parsing logic here
        response_json = json.loads(content)
        for journey in response_json['journeys']:
            first_leg = journey['legs'][0]
            train_name = first_leg['line']['name']
            departure_time_str = first_leg['departure'].split('T')[1][:5]  # Extract only time HH:MM
            departure_time = str(datetime.strptime(departure_time_str, "%H:%M")).split(" ")[1][0:5]
            journey_details.append(train_name + " um: " + departure_time)
        return " ".join(journey_details)


client = OebbHafasClient()
content = client.fetch_content()
journeys = client.parse_content(content)
print(journeys)
import requests

API_KEY = "1cbf752b50797f121c5b7f97f334e9cc"
LAT = 22.5726   # Kolkata
LON = 88.3639


def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"API failed: {response.status_code}")
    
    data = response.json()
    
    print("🌡 Temperature:", data["main"]["temp"])
    print("🌧 Weather:", data["weather"][0]["description"])


if __name__ == "__main__":
    fetch_weather()
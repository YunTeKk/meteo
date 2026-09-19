import requests

class WeatherAPIClient:

    def get_coords(self, city: str) -> tuple[float, float]:
        url_geocode = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=fr"
        response = requests.get(url_geocode)
        coords = (response.json()["results"][0]["latitude"], response.json()["results"][0]["longitude"])

        return coords

    def get_meteo(self, latitude: float, longitude: float) -> dict:
        url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&current_weather=true"
        response = requests.get(url_meteo)
        meteo_dict = response.json()

        return meteo_dict
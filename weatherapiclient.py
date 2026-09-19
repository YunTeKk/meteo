import requests

class CityNotFoundError(Exception):
    pass

class WeatherAPIClient:

    def get_coords(self, city: str) -> tuple[float, float]:
        url_geocode = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=fr"

        try:
            response = requests.get(url_geocode, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "results" not in data or not data["results"]:
                raise CityNotFoundError(f"Aucune ville trouvée pour la saisie : {city}")

            coords = (response.json()["results"][0]["latitude"], response.json()["results"][0]["longitude"])

            return coords

        except requests.exceptions.RequestException:
            print("[ERREUR] Aucune réponse du serveur de l'API de géocode.")


    def get_meteo(self, latitude: float, longitude: float) -> dict:
        url_meteo = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&current_weather=true"

        try:

            response = requests.get(url_meteo, timeout=5)
            meteo_dict = response.json()

            return meteo_dict

        except requests.exceptions.RequestException:
            print("[ERREUR] Aucune réponse du serveur de l'API météo.")
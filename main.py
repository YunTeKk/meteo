from weatherapiclient import WeatherAPIClient

weather_code_dict_conversion = {
    "0": "Ciel clair",
    "1": "Eclaircies",
    "2": "Partiellement nuageux",
    "3": "Couvert",
    "45": "Brouillard",
    "48": "Brouillard givrant",
    "51": "Bruine légère",
    "53": "Bruine modérée",
    "55": "Bruine dense",
    "56": "Bruine veglaçante légère",
    "57": "Bruine verglaçante dense",
    "61": "Pluie faible",
    "63": "Pluie modérée",
    "65": "Pluie forte",
    "66": "Pluie verglaçante légère",
    "67": "Pluie verglaçante forte",
    "71": "Neige légère",
    "73": "Neige modérée",
    "75": "Neige forte",
    "77": "Grains de neige",
    "80": "Averses de pluie légères",
    "81": "Averses de pluie modérées",
    "82": "Averses de pluie violentes",
    "85": "Averses de neige légères",
    "86": "Averses de neige fortes",
    "95": "Orage",
    "96": "Orage avec grêle",
    "99": "Orage avec chutes violentes de grêle"
}

if __name__ == "__main__":

    weather_api = WeatherAPIClient()

    
    print("=== BIENVENUE SUR L'APPLICATION METEO ===")
    city: str = input("Saisis le nom d'une ville : ")
    print("")

    coords: tuple[float, float] = weather_api.get_coords(city)

    latitude: float = coords[0]
    longitude: float = coords[1]

    print(f"[+] Recherche des coordonnées pour \"{city}\"...")
    print(f"Trouvé : Lat : {latitude}, Lon : {longitude}")
    print("")

    meteo = weather_api.get_meteo(latitude, longitude)

    temperature = meteo["current_weather"]["temperature"]
    temperature_unit = meteo["current_weather_units"]["temperature"]

    wind = meteo["current_weather"]["windspeed"]
    wind_unit = meteo["current_weather_units"]["windspeed"]

    current_weather_code = meteo["current_weather"]["weathercode"]
    current_weather = weather_code_dict_conversion[str(current_weather_code)]

    temperature_min = meteo["daily"]["temperature_2m_min"][0]
    temperature_max = meteo["daily"]["temperature_2m_max"][0]

    temperature_min_unit = meteo["daily_units"]["temperature_2m_min"]
    temperature_max_unit = meteo["daily_units"]["temperature_2m_max"]
    


    print("--- METEO ACTUELLE ---")
    print(f"Température : {temperature} {temperature_unit}")
    print(f"Vitesse du vent : {wind} {wind_unit}")
    print(f"Temps actuel : {current_weather}")
    print(f"Températures minimales de la journée : {temperature_min} {temperature_min_unit}")
    print(f"Températures maximales de la journée : {temperature_max} {temperature_max_unit}")
    print("")

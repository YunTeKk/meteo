import requests

from weatherapiclient import WeatherAPIClient, CityNotFoundError
from dataexporter import DataExporter

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
    weather_results = []
    
    print("=== BIENVENUE SUR L'APPLICATION METEO ===")

    while True:
        city: str = input("Saisis le nom d'une ville : ")

        if not city:
            print("Veuillez renseigner le nom d'un ville.")
            continue

        try:
            coords: tuple[float, float] = weather_api.get_coords(city)

            latitude: float = coords[0]
            longitude: float = coords[1]

            print("")
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

            current_weather_results_dict = {
                "Ville": city,
                "Température": f"{temperature} {temperature_unit}",
                "Vitesse du vent": f"{wind} {wind_unit}",
                "Temps actuel": current_weather,
                "Températures minimales de la journée": f"{temperature_min} {temperature_min_unit}",
                "Températures maximales de la journée": f"{temperature_max} {temperature_max_unit}" 
            }

            weather_results.append(current_weather_results_dict)
            
            print("--- METEO ACTUELLE ---")
            print(f"Température : {temperature} {temperature_unit}")
            print(f"Vitesse du vent : {wind} {wind_unit}")
            print(f"Temps actuel : {current_weather}")
            print(f"Températures minimales de la journée : {temperature_min} {temperature_min_unit}")
            print(f"Températures maximales de la journée : {temperature_max} {temperature_max_unit}")
            print("")

            new_research = input("Souhaitez vous refaire une recherche ? (O/N) : ").lower()

            while new_research != "o" and new_research != "n":

                new_research = input("Veuillez indiquer votre choix (O/N) :")

            if new_research == "o":
                continue

            elif new_research == "n":
                
                print("Voulez vous exporter les données des vos recherches météo ? (json / csv / non) : ")
                user_export_choice: str = input()

                while user_export_choice != "json" and user_export_choice != "csv" and user_export_choice != "non":

                    user_export_choice = input("Veuillez répondre par un des choix possibles (json / csv/ non) : ")

                if user_export_choice == "json" or user_export_choice == "csv":

                    data_exporter = DataExporter()

                    if user_export_choice == "json":
                        save_file = "meteo_historique.json"
                        data_exporter.export_json(weather_results, save_file)
                        
                    elif user_export_choice == "csv":
                        save_file = "meteo_historique.csv"
                        data_exporter.export_csv(weather_results, save_file)

                    print(f"Données exportées dans {save_file}. A bientôt !")
                    break

                elif user_export_choice == "non":
                    print("Femeture de l'application, A bientôt !")
                    break
            
        except requests.exceptions.RequestException:
            print(f"Impossible de récupérer les données météo de {city}.")

        except CityNotFoundError as e:
            print(f"[!] {e}. Vérifie l'orthographe et réessaie.")

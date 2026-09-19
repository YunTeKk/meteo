import json
import csv

class DataExporter:

    def export_json(self, data: dict, file: str) -> None:
        with open(file, "w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)

    def export_csv(self, data: dict, file: str) -> None:
        with open(file, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Clé", "Valeur"])

            for key, value in data.items():
                writer.writerow([key, value])
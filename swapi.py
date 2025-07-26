import os
import requests


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get(self, endpoint=""):
        try:
            if endpoint:
                endpoint = endpoint.strip("/")
                url = f"{self.base_url}/{endpoint}"
            else:
                url = f"{self.base_url}/"
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            print("Возникла ошибка при выполнении запроса")
            return None


class SWRequester(APIRequester):
    def __init__(self, base_url="https://swapi.dev/api"):
        super().__init__(base_url)

    def get_sw_categories(self):
        response = self.get()
        if response:
            data = response.json()
            return data.keys()
        return []

    def get_sw_info(self, sw_type):
        sw_type = sw_type.strip("/")
        url = f"{self.base_url}/{sw_type}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            print("Возникла ошибка при выполнении запроса")
            return "Ошибка при получении данных."


def save_sw_data():
    sw = SWRequester()
    os.makedirs("data", exist_ok=True)
    categories = sw.get_sw_categories()

    for category in categories:
        data = sw.get_sw_info(category)
        file_path = os.path.join("data", f"{category}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)

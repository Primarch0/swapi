from pathlib import Path
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
        response = self.get(sw_type)  
        if response:
            return response.text
        return "Ошибка при получении данных."


def save_sw_data():
    data_dir = Path("data")  
    data_dir.mkdir(exist_ok=True)  

    sw = SWRequester()
    categories = sw.get_sw_categories()

    for category in categories:
        data = sw.get_sw_info(category)
        file_path = data_dir / f"{category}.txt"  
        file_path.write_text(data, encoding="utf-8")

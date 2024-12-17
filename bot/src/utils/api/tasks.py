import requests
from src.core.config import settings


class TaskManager:
    def __init__(self):
        self.base_url = settings.api_url

    async def get_my_tasks(self):
        url = f"{self.base_url}/tasks/my"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                print("Ошибка:", response.status_code, response.json())
                return None
        except Exception as e:
            print("Произошла ошибка:", str(e))
            return None
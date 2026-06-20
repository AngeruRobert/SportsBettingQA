
import requests

from config import BASE_URL, USER_ID

class getBalance:

    def __init__(self, base_url : str=BASE_URL, user_id: str=USER_ID):
        self.base_url = base_url
        self.headers = {
            "x-user-id": user_id,
            "Content-Type": "Application/json",
        }

    def get_balance(self):
        return requests.get(
            f"{self.base_url}/api/balance",
            headers=self.headers,
            timeout=10,
        )

    def reset_balance(self):
        return requests.post(
            f"{self.base_url}/api/reset-balance",
            headers=self.headers,
            timeout=10,
        )

    def get_balance_amount(self) -> float:
        response = self.get_balance()

        assert response.status_code == 200, (
            f"Expected balance request to return 200, "
            f"but got {response.status_code}: {response.text}"
        )

        body = response.json()

        return float(body["balance"])
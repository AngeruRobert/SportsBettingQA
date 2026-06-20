import requests

from config import BASE_URL, USER_ID


class PlaceBetApi:
    """Small API helper for bet placement requests."""

    def __init__(self, base_url: str = BASE_URL, user_id: str = USER_ID):
        self.base_url = base_url
        self.headers = {
            "x-user-id": user_id,
            "Content-Type": "application/json",
        }

    def place_bet(self, match_id: str, selection: str, stake: float):
        payload = {
            "matchId": match_id,
            "selection": selection,
            "stake": stake,
        }

        return requests.post(
            f"{self.base_url}/api/place-bet",
            json=payload,
            headers=self.headers,
            timeout=10,
        )
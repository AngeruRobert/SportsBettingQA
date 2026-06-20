import pytest
from api.place_bet import PlaceBetApi

@pytest.mark.api
def test_api_rejects_negative_stake():
    """
    Chosen because negative stake validation is a high-risk financial rule.
    The backend must reject this even if the UI prevents it, because API calls
    can bypass frontend validation.
    """

    api = PlaceBetApi()

    response = api.place_bet(
        match_id="premier-league-manutd-chelsea",
        selection="HOME",
        stake=-10,
    )

    assert response.status_code in [400, 422], (
        f"Expected negative stake to be rejected, "
        f"but got {response.status_code}: {response.text}"
    )


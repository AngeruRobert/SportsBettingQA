from api.place_bet import PlaceBetApi
from api.get_balance import getBalance
import pytest

@pytest.mark.api
def test_api_rejects_over_balance_stake():
    """
    Chosen because over-balance stake validation is a high-risk financial rule.
    The backend must reject this even if the UI prevents it, because API calls
    can bypass frontend validation.
    """

    balance_api = getBalance()
    place_bet_api = PlaceBetApi()

    current_balance = balance_api.get_balance_amount()

    # Drain the balance using valid 100 EUR bets until remaining balance is below 100.
    # Example: if balance is 125.50, this places one 100 EUR bet and leaves 25.50.
    number_of_100_bets = int(current_balance // 100)

    for _ in range(number_of_100_bets):
        response = place_bet_api.place_bet(
            match_id="premier-league-manutd-chelsea",
            selection="HOME",
            stake=100,
        )

        assert response.status_code is 200, (
            f"Expected valid 100 EUR bet to be accepted, "
            f"but got {response.status_code}: {response.text}"
        )

    remaining_balance = balance_api.get_balance_amount()

    assert remaining_balance < 100, (
        f"Test setup failed. Expected remaining balance to be below 100, "
        f"but got {remaining_balance}"
    )

    # Now this bet should be rejected because stake 100 is higher than remaining balance.
    response = place_bet_api.place_bet(
        match_id="premier-league-manutd-chelsea",
        selection="HOME",
        stake=100,
    )

    assert response.status_code in [400, 422], (
        f"Expected over-balance stake to be rejected, "
        f"but got {response.status_code}: {response.text}"
    )

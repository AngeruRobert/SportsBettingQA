import pytest

from pages.main import MainPage


@pytest.mark.ui
def test_user_can_place_single_bet(driver):
    """
    Chosen because placing a valid single bet is the most critical user journey.
    It verifies that the user can select odds, enter a stake amount,
    place the bet, and receive a success confirmation.
    """

    page = MainPage(driver)

    page.open()
    page.select_first_available_home_odds()
    page.enter_stake_amount("10")
    page.place_bet()

    assert page.success_modal_is_displayed()
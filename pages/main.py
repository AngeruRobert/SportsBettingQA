from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import APP_URL


class MainPage:
    """Page Object for the main betting page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(APP_URL)

    def select_first_available_home_odds(self):
        odds_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'matchCard') "
                    "and .//span[contains(@class, 'badge') "
                    "and (normalize-space()='TODAY' or normalize-space()='UPCOMING')]]"
                    "//button[contains(@id, '-home')]",
                )
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            odds_button,
        )

        odds_button.click()

    def enter_stake_amount(self, amount: str):
        stake_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "bet-slip-stake-input")
            )
        )

        stake_input.clear()
        stake_input.send_keys(amount)

    def place_bet(self):
        place_bet_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "bet-slip-place-bet")
            )
        )
        place_bet_button.click()

    def success_modal_is_displayed(self) -> bool:
        success_modal = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='Bet Placed Successfully!']",
                )
            )
        )
        return success_modal.is_displayed()
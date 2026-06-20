import pytest
from selenium import webdriver


from api.get_balance import getBalance


@pytest.fixture(autouse=True)
def reset_balance_before_and_after_test():
    """
    Resets balance before and after each test so tests can be re-run safely.
    """

    balance_api = getBalance()

    before_response = balance_api.reset_balance()
    assert before_response.status_code in [200, 201], (
        f"Balance reset before test failed: "
        f"{before_response.status_code}: {before_response.text}"
    )

    yield

    after_response = balance_api.reset_balance()
    assert after_response.status_code in [200, 201], (
        f"Balance reset after test failed: "
        f"{after_response.status_code}: {after_response.text}"
    )

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()
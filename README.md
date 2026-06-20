````md
# Single Bet Placement Automation

This is a small Selenium + Pytest automation project for the Single Bet Placement feature.

The project contains:

- 1 UI E2E test for the critical user journey
- 2 API validation tests for high-risk financial rules
- Automatic balance reset before and after each test
- Pytest markers for UI/API execution
- HTML test report generation

---

## Project Structure

```
Single Bet Placement/
│
├── api/
│   ├── get_balance.py
│   └── place_bet.py
│
├── pages/
│   └── main.py
│
├── tests/
│   ├── test_e2e_ui.py
│   ├── test_place_bet_negative_stake.py
│   └── test_place_bet_over_balance_limit.py
│
├── Screenshots/*
│
├── reports/*
    └── report.html
├── config.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Test_Plan.md
├── Bugs.md
├── Strategy_Recommendations.md
└── README.md

````

---

## Automated Tests

### UI Test

`tests/test_e2e_ui.py`

Validates the main user journey:

1. Open the betting application.
2. Select odds for an available `TODAY` or `UPCOMING` match.
3. Enter a valid stake amount.
4. Place the bet.
5. Verify that the success modal is displayed.

This test was chosen because placing a valid single bet is the most critical user journey.

---

### API Tests

`tests/test_place_bet_negative_stake.py`

Validates that the API rejects negative stake values.

This test was chosen because negative bets are a high-risk financial validation issue. The backend must reject them even if the UI prevents them.

---

`tests/test_place_bet_over_balance_limit.py`

Validates that the API rejects bets where the stake is higher than the current user balance.

This test was chosen because users must not be able to place bets they cannot afford. This rule must be enforced by the backend because API calls can bypass frontend validation.

---

## Test Data Reset

The project uses the reset balance endpoint before and after each test:

```text
POST /api/reset-balance
```

This is handled automatically in `conftest.py`.

The reset is done before each test so every test starts from a clean balance state.

The reset is also done after each test so repeated test runs are safer and one test does not affect the next one.

This is important because:

* the UI test deducts balance after placing a bet
* the over-balance API test intentionally spends part of the balance
* failed tests could leave the user balance in an unexpected state

---

## Requirements

* Python 3.10+
* Google Chrome
* Internet connection

---

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run Tests

Run all tests:

```bash
pytest
```

Run only UI tests:

```bash
pytest -m ui
```

Run only API tests:

```bash
pytest -m api
```

Run a specific test file:

```bash
pytest tests/test_e2e_ui.py
```

---

## Test Reports

The project uses `pytest-html` for HTML report generation.

The report is created automatically after running tests.

Report location:

```text
reports/report.html
```

Open `reports/report.html` in a browser to view the test results.

---

## Pytest Configuration

The project uses `pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -v --html=reports/report.html --self-contained-html
markers =
    ui: UI tests
    api: API tests
```

This configuration:

* tells Pytest to look for tests inside the `tests/` folder
* runs tests in verbose mode
* generates an HTML report
* allows filtering tests by `ui` and `api` markers

---

## Known Behavior

Some API tests may fail while the known backend bugs still exist.

For example:

* negative stake values may currently be accepted by the API
* over-balance stakes may currently be accepted by the API

These failures are expected because the tests validate important business rules that the backend should enforce.

---

## Notes

Selenium 4 uses Selenium Manager, so ChromeDriver usually does not need to be downloaded manually.

The following local files/folders should not be included in the final submission zip:

```text
.venv/
.idea/
*.iml
reports/
```


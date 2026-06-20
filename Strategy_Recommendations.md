# Strategy & Recommendations

## Why these tests were selected for automation

### 1. E2E UI test — Place a valid single bet

I selected the valid single bet placement journey because it is the most business-critical user flow in the application.

This test covers the main happy path:

1. User opens the betting page.
2. User selects odds for an available `TODAY` or `UPCOMING` match.
3. User enters a valid stake.
4. User places the bet.
5. User receives a success confirmation modal.

This scenario is a good candidate for automation because it verifies that the main UI flow works end-to-end and that the most important user journey is not broken by future changes.

---

### 2. API test — Reject invalid financial stake

I selected the API validation test because financial validation must be enforced by the backend, not only by the UI.

The negative stake test checks that the API rejects invalid stake values. This is high value because API calls can bypass frontend validation, and accepting invalid financial values can corrupt balance calculations or create invalid bet records.

I also added an additional API validation test for over-balance stakes because it is another high-risk financial rule: users should not be able to place bets higher than their available balance.

---

## What was intentionally left as manual only

Some scenarios were intentionally kept as manual tests because they are better suited for visual or exploratory validation.

### Success modal content and visual correctness

The UI has issues such as swapped teams in the success modal and incorrect payout display. These are important, but the visual comparison and exact content review are easier to validate manually for this assignment.

### Search and filtering behavior

Past matches displayed in search results, date filters, and odds filters were kept as manual/exploratory checks because they require reviewing multiple combinations of displayed data and business rules.

### UX and wording issues

Issues like the `Remove All` text being misleading for a single-bet feature are better validated manually because they involve product wording and requirement interpretation.

### Bet history / missing feedback

The lack of bet history or persistent placed-bet feedback was left manual because the requirement does not clearly define a history page. This should first be clarified with the product team before automating.

### Performance and stress testing

The stress test finding, where the API returns `200 OK` but not all bets are processed, was documented as a defect. For this assignment, I would not include it in the small automation suite because performance tests require a separate setup, controlled data, and clear thresholds.

---

## Top recommendations if the project scales

### 1. Add CI/CD execution for automated tests

The automated tests should run in a CI pipeline on every pull request or deployment.

Recommended pipeline stages:

- install dependencies
- run API tests
- run UI smoke test
- generate HTML test report
- fail the pipeline if critical tests fail

API tests should run first because they are faster and more stable. UI tests can run as smoke coverage after the API layer passes.

---

### 2. Improve test data strategy

The current tests depend on a shared user balance and existing match data. This can make tests flaky when previous test runs change the balance.

Recommended improvements:

- provide a reliable reset endpoint that restores the expected balance
- make reset balance match the requirement exactly
- use dedicated test users per test type
- provide known upcoming and past match IDs for automation
- avoid depending on production-like changing data

A stable data setup is especially important for betting flows because balance, stake, and bet state are all connected.

---

### 3. Clarify and enforce business rules in the specification

Some requirement areas should be clarified before expanding automation.

Recommended clarifications:

- exact minimum and maximum stake values
- expected currency everywhere: UI and API
- whether bet history is required
- how past matches should be handled in UI and API
- expected behavior when balance is too low
- expected response codes for invalid API requests
- expected behavior under concurrent requests

Clear rules make test cases easier to automate and reduce ambiguity between QA, developers, and product.

---

### 4. Add more test layers over time

If the project grows, the test coverage should be split by layer:

- API contract tests for validation, response schema, status codes, and currency
- UI smoke tests for critical user journeys only
- integration tests for balance deduction and bet creation
- performance tests for concurrent bet placement and API reliability
- manual exploratory testing for UX, visual behavior, and requirement inconsistencies

This keeps the automation suite fast, stable, and maintainable while still covering the most important risks.

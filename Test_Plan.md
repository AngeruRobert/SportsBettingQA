# Test Plan — Single Bet Placement

## Mismatch data in the Specification: `Stake Minimum €1.01` and `UI Error Messaging (minimum expected copy):Minimum stake is €1.00`

## TC-001 — API rejects negative stake values

**Area:** API  
**Priority:** Critical

**Risk Rationale:**  
Negative stakes are invalid financial transactions. If the API accepts negative values, the user balance and betting records can be corrupted or manipulated. This must be enforced on the backend because frontend validation can be bypassed.

**Steps:**

1. Send a `POST /api/place-bet` request with a valid user ID.
2. Use a valid upcoming match ID.
3. Use a valid selection value, for example `home`, `draw`, or `away`.
4. Set the stake to a negative value, for example `-10`.
5. Send the request.
6. Check the API response.
7. Check whether the user balance or bet history changed.

**Expected Result:**

- The API rejects the request.
- The response returns a validation error, for example `400 Bad Request`.
- The error message clearly explains that stake must be a positive valid amount.
- No bet is created.
- User balance remains unchanged.

---

## TC-002 — API rejects stake higher than current balance

**Area:** API  
**Priority:** Critical

**Risk Rationale:**  
Users must not be allowed to place bets they cannot afford. This is a core financial validation rule and must be enforced by the backend, not only by the UI.

**Steps:**

1. Call the balance endpoint and note the current user balance.
2. Send a `POST /api/place-bet` request with a stake higher than the available balance.
3. Use a valid upcoming match ID.
4. Use a valid selection value.
5. Send the request.
6. Check the API response.
7. Check the balance again.

**Expected Result:**

- The API rejects the request.
- The response returns an insufficient balance validation error.
- No bet is created.
- User balance remains unchanged.
- The user cannot place a bet that exceeds the available balance.

---

## TC-003 — UI and API prevent betting on past matches

**Area:** UI + API  
**Priority:** Critical

**Risk Rationale:**  
The feature supports only upcoming/pre-match football events. Allowing bets on past matches breaks a core business rule and may create invalid betting transactions.

**Steps:**

1. Open the application with a valid user ID.
2. Search or filter the match list.
3. Check whether any past matches are displayed.
4. If a past match is visible, try to select an odds option.
5. Attempt to place a bet from the UI.
6. Send a direct `POST /api/place-bet` request using a past match ID.
7. Check the UI and API responses.

**Expected Result:**

- Past matches are not displayed in the UI.
- If a past match is somehow displayed, it cannot be selected for betting.
- The API rejects any bet placement request for a past match.
- No bet is created for a past match.
- User balance remains unchanged.

---

## TC-004 — User places a valid single bet successfully from the UI

**Area:** UI  
**Priority:** Critical

**Risk Rationale:**  
This is the main happy path and the core user flow. The user must be able to select one valid football match outcome, choose a predefined stake, place the bet, and receive a correct confirmation.

**Steps:**

1. Open the application with a valid user ID.
2. Verify that upcoming football matches are displayed.
3. Select one match outcome: `1`, `X`, or `2`.
4. Verify the selected outcome appears in the bet slip.
5. Select one predefined stake amount.
6. Verify the selected stake is active.
7. Click `Place Bet`.
8. Wait for the success confirmation modal.
9. Review the bet details shown in the modal.

**Expected Result:**

- The user can select one valid match outcome.
- The bet slip displays the selected match, selection, odds, and stake.
- Only one selection is active at a time.
- The bet is placed successfully.
- Success modal displays correct match details, selection, stake, odds, potential payout, and timestamp/bet ID if required.
- Balance is reduced by the selected stake.

---

## TC-005 — UI calculates and displays correct potential payout

**Area:** UI  
**Priority:** High

**Risk Rationale:**  
Potential payout is a financial value shown to the user before and after bet placement. Incorrect payout can mislead the user and create trust or dispute issues.

**Steps:**

1. Open the application with a valid user ID.
2. Select a match outcome with odds different from `2.00`.
3. Select a predefined stake amount.
4. Check the potential payout in the bet slip.
5. Place the bet.
6. Check the potential payout in the success modal.
7. Compare both values with the expected formula.

**Expected Result:**

- Potential payout is calculated as `selected stake × selected odds`.
- The bet slip displays the correct potential payout.
- The success modal displays the same correct potential payout.
- The calculation does not use a fixed multiplier.
- Currency formatting is consistent.

---

## TC-006 — API handles concurrent bet placement without false success responses

**Area:** Performance / API Reliability  
**Priority:** High

**Risk Rationale:**  
Under load, every successful API response must represent a real processed bet. Returning `200 OK` while not processing all bets creates false success, data inconsistency, and unreliable financial records.

**Steps:**

1. Prepare a stress test with multiple valid `POST /api/place-bet` requests.
2. Use a valid user ID, valid upcoming match ID, valid selection, and valid stake.
3. Send many requests concurrently.
4. Record all response codes.
5. Count how many requests returned `200 OK`.
6. Verify how many bets were actually processed.
7. Check the final balance.

**Expected Result:**

- Every `200 OK` response corresponds to one successfully processed bet.
- If the API cannot process a request, it returns an appropriate error status.
- No request silently fails.
- Final balance matches the number of successfully processed bets.
- No duplicate or missing bet records are created.

# Test Report — A2 Web UI Automation Testing
## ABC Library Book Borrowing System — https://stqa.rbc.vn

**Course**: Software Testing & Quality Assurance (STQA)  
**Tool**: Python + Playwright + pytest  
**Date**: June 2026

---

## 1. Summary

| Metric | Value |
|--------|-------|
| Total test cases (required) | 12 (TC-01 → TC-12) |
| Bonus test cases (B1) | 3 (TC-13, TC-14, TC-15) |
| Total test functions | 15 |
| Data-driven parametrized sets | 3 (Bonus B2) |
| Screenshots captured | 1 per test case |

---

## 2. Test Case Results

### Group 1: Login (`tests/test_login.py`)

| TC | Description | Expected | Assertion |
|----|-------------|----------|-----------|
| TC-01 | Login success — valid credentials | "Đăng xuất" button + display name in UI | `has_display_name or has_logout` |
| TC-02 | Login fail — wrong password | Error "Mật khẩu không đúng" (SRS REQ-01) | Exact error text + no "Đăng xuất" |
| TC-03 | Login fail — empty fields | Error "Vui lòng nhập email và mật khẩu" (SRS REQ-01) | Exact error text + no "Đăng xuất" |
| TC-13 (B1) | Login fail — email not found | Error "Không tìm thấy thành viên" (SRS REQ-01) | Parametrized via B2 |

**Bonus B2 — Data-Driven**: `test_login_fail_parametrized` uses `@pytest.mark.parametrize`
to cover TC-02, TC-03, and TC-13 in a single function with 3 datasets.
This follows Textbook Ch.3 §3.3.2 — Data-Driven Testing.

---

### Group 2: Search & Filter (`tests/test_search.py`)

| TC | Description | Expected | Assertion |
|----|-------------|----------|-----------|
| TC-04 | Search by name "Flutter" | ≥1 book card with "Flutter" in aria-label | `count > 0` + semantics text |
| TC-05 | Search — no result | 0 book cards + "Không tìm thấy sách" message | `count == 0` + exact message |
| TC-06 | Filter by category "Công nghệ" | All visible cards have "Công nghệ" in aria-label | Per-card loop assertion |
| TC-07 | Search by author "Nguyễn Minh Đức" | ≥1 book card with author name | `count > 0` + semantics text |

**Notes**:
- TC-04 and TC-07 use the same search box (aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."),
  demonstrating the system supports unified name+author search per SRS REQ-03.
- TC-06 uses a per-card loop (not just a count) to strictly verify every result — this is
  Bonus B3 (specific assertions beyond simple URL/count checks).
- TC-05 validates the no-result branch of Equivalence Partitioning (valid input ↔ no-match input).

---

### Group 3: Borrow & Return (`tests/test_borrow_return.py`)

| TC | Description | Account | Expected |
|----|-------------|---------|----------|
| TC-08 | Borrow available book | dam.tran (0 active borrows) | "Đang mượn" or "thành công" after confirmation dialog |
| TC-09 | View borrowed books list | ba.nguyen (BOOK003 active) | "Trả sách" button + borrow record visible in Mượn/Trả tab |
| TC-10 | Return borrowed book | ba.nguyen (BOOK003 overdue) | "Đã trả" / "thành công" / no more "Trả sách" button |
| TC-14 (B1) | Borrow fail — suspended | cu.le (Tạm ngưng) | Rejection message containing "tạm ngưng" (SRS REQ-04) |

**Notes**:
- TC-08 uses `dam.tran@email.com` (clean state) instead of the default `test_config` user
  to ensure a predictable borrow state (0 active borrows → below 3-book limit).
- TC-10 involves an overdue book (BOOK003, due 15/09/2024). SRS REQ-05 states the system
  must display an overdue warning — the assertion accepts "quá hạn" as a valid success signal.
- TC-14 validates SRS REQ-04's requirement that the error message must distinguish
  "tạm ngưng" (suspended) from "hết hạn" (expired). The assertion explicitly checks this.
- **Data isolation**: each `page` fixture creates a new browser context.
  Since the system is fully client-side (no backend), each test starts from seed data.

---

### Group 4: General (`tests/test_general.py`)

| TC | Description | Expected |
|----|-------------|----------|
| TC-11 | Logout | Login page visible ("Đăng nhập" + Email input); "Đăng xuất" gone; display name gone |
| TC-12 | Switch language to English | English terms ("Logout", "Borrow", "Library", etc.) appear in semantics |
| TC-15 (B1) | Librarian views all borrow records | Borrow records visible + librarian-specific UI ("Thành viên" tab, "Kiểm tra quá hạn") |

**Notes**:
- TC-15 demonstrates role-based access control: librarian sees all records (SRS REQ-08),
  contrasting with member role (TC-09) which only sees own records.

---

## 3. Bonus Features Implemented

| Bonus | Description | Where |
|-------|-------------|-------|
| B1 (+0.5) | 3 extra test cases beyond TC-12: TC-13 (email not found), TC-14 (suspended account), TC-15 (librarian view) | test_login.py, test_borrow_return.py, test_general.py |
| B2 (+0.5) | Data-driven parametrized test for login failures | `test_login_fail_parametrized` in test_login.py |
| B3 (+0.5) | Specific assertions throughout: exact error text from SRS, per-card category loop, role-based UI checks | All test files |
| B4 (+0.5) | This report | REPORT.md |

---

## 4. Technical Notes

### Flutter Web (CanvasKit) Handling

The system uses Flutter Web with CanvasKit renderer — no standard HTML DOM.
All interactions go through the Accessibility Semantics Tree (`flt-semantics` elements).

Key patterns used:
- `enable_flutter_semantics(page)` called after every navigation and after any action
  that triggers a Flutter re-render (tab switch, dialog open, form submit).
- `wait_for_flutter(page, text="...")` used instead of `time.sleep()` for all waits.
  This is a Smart Wait that polls the Semantics Tree until the expected text appears.
- `page.wait_for_timeout(N)` used only when waiting for a UI state without a
  predictable text anchor (e.g., after a borrow confirmation dialog clears).

### Error Message Alignment with SRS

All expected error messages come directly from **SRS REQ-01** and **REQ-04**:

| Scenario | SRS Error Text | Used In |
|----------|---------------|---------|
| Wrong password | "Mật khẩu không đúng" | TC-02, B2-TC02 |
| Empty fields | "Vui lòng nhập email và mật khẩu" | TC-03, B2-TC03 |
| Email not found | "Không tìm thấy thành viên" | TC-13, B2-TC13 |
| Suspended account | Contains "tạm ngưng" | TC-14 |

If any test FAILs with a message about wrong error text, it indicates
a **bug**: the system's error message does not match the SRS specification.

---

## 5. Known Issues / Observations

| ID | Observation | SRS Reference |
|----|-------------|---------------|
| OBS-01 | BOOK003 (ba.nguyen) is overdue since 15/09/2024. The overdue flag is only updated when Librarian clicks "Kiểm tra quá hạn" — it does not auto-update. | SRS REQ-06 |
| OBS-02 | Data is client-side only — a browser refresh resets all state to seed data. Each test must navigate and set up its own state. | SRS §5 |
| OBS-03 | TC-08 requires a double-click pattern: "Mượn sách này" → confirmation dialog → "Mượn". | SRS REQ-04 |

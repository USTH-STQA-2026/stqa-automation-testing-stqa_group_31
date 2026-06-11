"""
Login Tests — Library Book Borrowing System (ABC Library)
System under test: https://stqa.rbc.vn

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): Reachability → Infection → Propagation → Revealability
     See the [R], [I], [P], [R✓] comments in TC-01 and reused throughout.
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2):
     See test_login_fail_parametrized (Bonus B2).

Test cases:
   TC-01  Login success — valid credentials          ✅ Completed (reference)
   TC-02  Login fail — wrong password                ✅ Completed
   TC-03  Login fail — empty fields                  ✅ Completed
   Bonus  Data-driven login failures (B1 + B2 + B3)  ✅ Completed
          Covers TC-02, TC-03, TC-13 (email not found) via @parametrize
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    SCREENSHOT_DIR,
)


# ─────────────────────────────────────────────────────────────────────────────
# TC-01: Login Success (Reference Example — Already Completed)
# ─────────────────────────────────────────────────────────────────────────────

def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials.

    ✅ COMPLETED — Use as a reference example.

    📖 RIPR Model (Ch.2):
        Each step maps to one stage of the Reachability → Infection →
        Propagation → Revealability chain.

    Expected (SRS REQ-01):
        Valid email + password → navigate to home page, display user name
        and Logout button in AppBar.
    """
    # [R] Reachability: reach the login UI
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: inject valid credentials, triggering the login flow
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Smart Wait — state propagates to UI as Logout button
    #     (faster & more reliable than time.sleep)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc01_login_success.png"))

    # [R✓] Revealability: Test Oracle — detect any discrepancy
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_display_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_display_name or has_logout, (
        f"TC-01 FAILED: Expected display name '{test_config['display_name']}' "
        f"or Logout button in semantics tree. "
        f"Actual (first 300 chars): {sem_text[:300]}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-02: Login Fail — Wrong Password
# ─────────────────────────────────────────────────────────────────────────────

def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail — wrong password (Đăng nhập thất bại — sai mật khẩu).

    Scenario:
        Enter a registered email with an incorrect password.

    Expected (SRS REQ-01):
        Error message "Mật khẩu không đúng" is displayed.
        User remains on the login page (no Logout button visible).
    """
    # [R] Reachability: reach the login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: correct email, wrong password — corrupts the auth input
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Smart Wait — error message propagates to Semantics Tree
    #     SRS REQ-01 specifies: "Mật khẩu không đúng"
    wait_for_flutter(page, text="Mật khẩu không đúng")
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "tc02_login_fail_wrong_password.png")
    )

    # [R✓] Revealability: verify error is shown AND user is NOT authenticated
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # B3: Specific assertion — exact error text from SRS REQ-01
    assert "Mật khẩu không đúng" in sem_text, (
        f"TC-02 FAILED: Expected 'Mật khẩu không đúng' in semantics. "
        f"Actual: {sem_text[:300]}"
    )
    # B3: Verify user is still unauthenticated
    assert "Đăng xuất" not in sem_text, (
        "TC-02 FAILED: Logout button must NOT appear after wrong-password login"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-03: Login Fail — Empty Fields
# ─────────────────────────────────────────────────────────────────────────────

def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail — empty fields (Đăng nhập thất bại — bỏ trống cả hai trường).

    Scenario:
        Submit the login form without entering email or password.

    Expected (SRS REQ-01):
        Validation message "Vui lòng nhập email và mật khẩu" is displayed.
        User remains on the login page.
    """
    # [R] Reachability: reach the login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: click Login with no input — triggers validation branch
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Smart Wait — validation error propagates to Semantics Tree
    #     SRS REQ-01 specifies: "Vui lòng nhập email và mật khẩu"
    wait_for_flutter(page, text="Vui lòng nhập email và mật khẩu")
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "tc03_login_fail_empty_fields.png")
    )

    # [R✓] Revealability: verify validation shown AND user is NOT authenticated
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # B3: Specific assertion — exact validation text from SRS REQ-01
    assert "Vui lòng nhập email và mật khẩu" in sem_text, (
        f"TC-03 FAILED: Expected 'Vui lòng nhập email và mật khẩu'. "
        f"Actual: {sem_text[:300]}"
    )
    assert "Đăng xuất" not in sem_text, (
        "TC-03 FAILED: Logout button must NOT appear after empty-form submission"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Bonus B1 + B2 + B3: Data-Driven Login Failure Test
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("email,password,expected_error,tc_id", [
    # TC-02 scenario: valid email, wrong password
    (
        "ba.nguyen@email.com",
        "wrongpassword",
        "Mật khẩu không đúng",
        "B2-TC02",
    ),
    # TC-03 scenario: both fields empty
    (
        "",
        "",
        "Vui lòng nhập email và mật khẩu",
        "B2-TC03",
    ),
    # TC-13 (Bonus B1): email not registered in the system
    (
        "nobody@test.com",
        "anything123",
        "Không tìm thấy thành viên",
        "B2-TC13",
    ),
])
def test_login_fail_parametrized(page, test_config, email, password, expected_error, tc_id):
    """Bonus B2 + B3: Data-Driven login failure tests.

    📖 Data-Driven Testing (Ch.3 §3.3.2):
        One test function drives multiple datasets, each representing a distinct
        failure path. This avoids copy-paste and makes adding new scenarios trivial.

    Parameters:
        B2-TC02 — Wrong password   → "Mật khẩu không đúng"
        B2-TC03 — Empty fields     → "Vui lòng nhập email và mật khẩu"
        B2-TC13 — Email not found  → "Không tìm thấy thành viên"  (Bonus TC-13, B1)

    All expected error messages are sourced from SRS REQ-01 (B3: specific assertions).
    """
    # Arrange
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Act
    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # Smart Wait
    wait_for_flutter(page, text=expected_error)
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            f"bonus_{tc_id.lower()}_login_fail.png",
        )
    )

    # Assert (B3: exact text from SRS)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, (
        f"[{tc_id}] Expected error '{expected_error}' in semantics tree. "
        f"Actual: {sem_text[:300]}"
    )
    assert "Đăng xuất" not in sem_text, (
        f"[{tc_id}] Logout button must NOT be present after a failed login"
    )

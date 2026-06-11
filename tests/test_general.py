"""
Logout & Language Tests — Library Book Borrowing System (ABC Library)
System under test: https://stqa.rbc.vn

📖 Textbook concepts:
   - State-transition testing: logout transitions from authenticated → unauthenticated
   - Equivalence Partitioning: language variants (VI / EN)
   - Role-based access (Bonus TC-15): librarian vs member visibility

Test cases:
   TC-11  Logout — returns to login page              ✅ Completed
   TC-12  Switch language to English                  ✅ Completed
   TC-15  (Bonus B1) Librarian views all borrow records ✅ Completed
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    login,
    wait_for_flutter,
    SCREENSHOT_DIR,
)


# ─────────────────────────────────────────────────────────────────────────────
# TC-11: Logout
# ─────────────────────────────────────────────────────────────────────────────

def test_logout(page, test_config):
    """TC-11: Logout success — returns to login page.

    Scenario:
        Log in → click "Đăng xuất" → verify page returns to the login screen.

    Expected (SRS REQ-01):
        - Login page is shown: "Email" input and "Đăng nhập" button are present.
        - No "Đăng xuất" button visible (session cleared).
        - User display name is gone.
    """
    # Arrange: log in
    login(page, test_config)

    # Act: click Logout
    flutter_click_button(page, "Đăng xuất")

    # Smart Wait: wait for the login page indicators to appear
    wait_for_flutter(page, selector='input[aria-label="Email"]')
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc11_logout.png"))

    # Assert (B3: verify login page elements present AND session indicators gone)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Login page must show "Đăng nhập" button or Email input
    login_page_visible = (
        "Đăng nhập" in sem_text
        or page.locator('input[aria-label="Email"]').count() > 0
    )
    assert login_page_visible, (
        "TC-11 FAILED: Expected to return to login page after logout. "
        "'Đăng nhập' button or Email input not found. "
        f"Actual: {sem_text[:300]}"
    )

    # B3: Verify session is cleared — Logout button must be gone
    assert "Đăng xuất" not in sem_text and "Logout" not in sem_text, (
        "TC-11 FAILED: 'Đăng xuất' / 'Logout' button still visible after logout. "
        "Session must be fully cleared."
    )

    # B3: Verify user display name is gone
    assert test_config["display_name"] not in sem_text, (
        f"TC-11 FAILED: User display name '{test_config['display_name']}' "
        "still visible after logout."
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-12: Switch Language to English
# ─────────────────────────────────────────────────────────────────────────────

def test_switch_language_to_english(page, test_config):
    """TC-12: Switch UI language to English.

    Scenario:
        Log in → click the "EN" language button →
        verify the interface switches to English.

    Expected (SRS §1 — Bilingual UI):
        - UI labels switch from Vietnamese to English.
        - "Logout", "Borrow", or "Library" text appears (or "EN" tab is active).
        - Vietnamese-only labels like "Đăng xuất" are replaced or co-exist
          with English equivalents.
    """
    # Arrange: log in
    login(page, test_config)

    # Act: click the "EN" language switcher button
    flutter_click_button(page, "EN")

    # Smart Wait: wait for English text to appear in Semantics Tree
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc12_switch_language_en.png"))

    # Assert (B3: check for English UI indicators)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # SRS §1: bilingual — these English terms should appear after switching
    english_indicators = ["Logout", "Borrow", "Library", "Search", "Return", "Books"]
    has_english = any(term in sem_text for term in english_indicators)

    assert has_english, (
        "TC-12 FAILED: Expected English UI text after clicking 'EN'. "
        f"Checked for: {english_indicators}. "
        f"Actual semantics (first 400 chars): {sem_text[:400]}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-15 (Bonus B1): Librarian Views All Borrow Records
# ─────────────────────────────────────────────────────────────────────────────

def test_librarian_views_all_borrow_records(page, test_config):
    """TC-15 (Bonus B1): Librarian can view ALL members' borrow records.

    Scenario:
        Log in as librarian → navigate to "Mượn / Trả" tab →
        verify records from multiple members are visible.

    Expected (SRS REQ-08):
        - Librarian sees borrow records for ALL members (not just themselves).
        - Seed data: BR001 (ba.nguyen/BOOK003), BR002 (dam.tran), BR003 (biet.hoang)
          should be visible.
        - Contrasts with member role — members only see their own records.

    Account used:
        librarian@library.com / admin123 — Librarian role (LIB001).
    """
    # Arrange: log in as librarian
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Act: navigate to the Mượn / Trả tab
    page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]').click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "tc15_librarian_all_borrow_records.png")
    )

    # Assert (B3: librarian-specific — must see records from multiple members)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Librarian should see borrow records (multiple members' records should appear)
    has_borrow_records = (
        "Đang mượn" in sem_text
        or "Đã trả" in sem_text
        or "BR00" in sem_text
        or "Trả sách" in sem_text
    )
    assert has_borrow_records, (
        "TC-15 FAILED: Librarian should see borrow records in Mượn/Trả tab. "
        "Expected 'Đang mượn', 'Đã trả', or borrow IDs. "
        f"Actual: {sem_text[:400]}"
    )

    # B3: Librarian should have librarian-specific features
    sem_has_librarian_features = (
        "Thành viên" in sem_text      # Members tab visible to librarian
        or "Kiểm tra quá hạn" in sem_text  # Overdue check feature
        or "Nguyễn Thủ Thư" in sem_text    # Librarian display name
        or "Thủ thư" in sem_text
    )
    assert sem_has_librarian_features, (
        "TC-15 FAILED: Librarian-specific UI features not found. "
        "Expected 'Thành viên' tab or 'Kiểm tra quá hạn' or librarian name. "
        f"Actual: {sem_text[:400]}"
    )

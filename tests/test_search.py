"""
Search & Filter Tests — Library Book Borrowing System (ABC Library)
System under test: https://stqa.rbc.vn

📖 Textbook concepts:
   - Equivalence Partitioning: TC-04 (valid query) vs TC-05 (no-result query)
   - Boundary Analysis: TC-06 verifies filter strictly constrains results
   - RIPR Model applied throughout

Test cases:
   TC-04  Search book by name — keyword found        ✅ Completed
   TC-05  Search book — no results                   ✅ Completed
   TC-06  Filter books by category                   ✅ Completed
   TC-07  Search book by author name                 ✅ Completed

Hints used from starter:
   - Search box aria-label : "Tìm kiếm theo tên sách hoặc tác giả..."
   - Category filter label  : "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
   - Book card selector     : flt-semantics[role="group"][aria-label*="Mã: BOOK"]
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    login,
    wait_for_flutter,
    SCREENSHOT_DIR,
)

# Selectors
BOOK_CARD = 'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
SEARCH_LABEL = "Tìm kiếm theo tên sách hoặc tác giả..."
CATEGORY_LABEL = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"


# ─────────────────────────────────────────────────────────────────────────────
# TC-04: Search Book by Name — Results Found
# ─────────────────────────────────────────────────────────────────────────────

def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name — keyword "Flutter" returns matching results.

    Scenario:
        Log in → type "Flutter" in the search box → verify at least one book
        with "Flutter" in its name is displayed.

    Expected (SRS REQ-03):
        - Search is case-insensitive.
        - Results contain books whose name OR author matches the keyword.
        - Seed data (SRS §3.2): BOOK001 "Lập trình Flutter cơ bản" should appear.
    """
    # Arrange
    login(page, test_config)

    # Act: enter keyword in search box
    flutter_fill(page, SEARCH_LABEL, "Flutter")

    # Smart Wait: wait for a book title containing "Flutter" to appear
    wait_for_flutter(page, text="Flutter")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc04_search_by_name.png"))

    # Assert (B3: specific — count book group cards with Flutter in aria-label)
    # Note: Flutter CanvasKit stores book titles in aria-label, not text nodes.
    # Use role="group" to match book cards only (not the search input field itself).
    matching_cards = page.locator('flt-semantics[role="group"][aria-label*="Flutter"]')
    assert matching_cards.count() > 0, (
        "TC-04 FAILED: Expected at least one book card with 'Flutter' in aria-label. "
        "Seed book BOOK001 'Lập trình Flutter cơ bản' should match."
    )

    # B3: Also verify via all aria-labels (Flutter CanvasKit renders titles in aria-label)
    all_labels = " ".join(
        el.get_attribute("aria-label") or ""
        for el in page.locator("flt-semantics").all()
    )
    assert "Flutter" in all_labels, (
        f"TC-04 FAILED: 'Flutter' not found in any aria-label. Got labels: {all_labels[:300]}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-05: Search Book — No Results
# ─────────────────────────────────────────────────────────────────────────────

def test_search_book_no_result(page, test_config):
    """TC-05: Search book with keyword that matches no book — no-result message shown.

    Scenario:
        Log in → search a nonsense keyword → verify no book cards are shown
        and an appropriate "not found" message appears.

    Expected (SRS REQ-03):
        - No book cards with "Mã: BOOK" in aria-label are displayed.
        - System shows "Không tìm thấy sách" message.
    """
    # Arrange
    login(page, test_config)

    # Act: enter a keyword guaranteed to not match any book or author
    flutter_fill(page, SEARCH_LABEL, "xyz_khong_ton_tai_99999")

    # Smart Wait: wait for "Không tìm thấy sách" message (SRS REQ-03)
    wait_for_flutter(page, text="Không tìm thấy sách")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc05_search_no_result.png"))

    # Assert (B3: specific count AND message text)
    book_cards = page.locator(BOOK_CARD)
    assert book_cards.count() == 0, (
        f"TC-05 FAILED: Expected 0 book cards, found {book_cards.count()}. "
        "No book should match keyword 'xyz_khong_ton_tai_99999'."
    )

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Không tìm thấy sách" in sem_text, (
        f"TC-05 FAILED: Expected 'Không tìm thấy sách' message. "
        f"Got: {sem_text[:300]}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# TC-06: Filter Books by Category
# ─────────────────────────────────────────────────────────────────────────────

def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category "Công nghệ" — only tech books displayed.

    Scenario:
        Log in → type "Công nghệ" in the category filter → verify every displayed
        book card belongs to the "Công nghệ" category.

    Expected (SRS REQ-03):
        - All returned book cards have "Công nghệ" in their aria-label.
        - Seed data has 8 "Công nghệ" books (BOOK001, 002, 003, 005, 008, 009, 010, 011).
    """
    # Arrange
    login(page, test_config)

    # Act: type in the category filter field
    flutter_fill(page, CATEGORY_LABEL, "Công nghệ")

    # Smart Wait: at least one book with "Công nghệ" must appear
    wait_for_flutter(page, text="Công nghệ")
    enable_flutter_semantics(page)

    # Give Flutter a moment to finish filtering
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc06_filter_by_category.png"))

    # Assert (B3: check every book card belongs to category)
    book_cards = page.locator(BOOK_CARD)
    card_count = book_cards.count()
    assert card_count > 0, (
        "TC-06 FAILED: Expected at least one book after filtering by 'Công nghệ'"
    )

    # Verify every visible book card contains "Công nghệ"
    for i in range(card_count):
        label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, (
            f"TC-06 FAILED: Book card #{i + 1} does not belong to category 'Công nghệ'. "
            f"aria-label: {label}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# TC-07: Search Book by Author Name
# ─────────────────────────────────────────────────────────────────────────────

def test_search_by_author(page, test_config):
    """TC-07: Search book by author name — matching books returned.

    Scenario:
        Log in → type author name "Nguyễn Minh Đức" in the search box →
        verify books by that author appear.

    Expected (SRS REQ-03):
        - At least one book card with "Nguyễn Minh Đức" in aria-label is shown.
        - Seed data: BOOK001 (Flutter) and BOOK009 (Python) are by Nguyễn Minh Đức.
    """
    # Arrange
    login(page, test_config)

    # Act: search by author name
    flutter_fill(page, SEARCH_LABEL, "Nguyễn Minh Đức")

    # Smart Wait: wait for author name to appear in the Semantics Tree
    wait_for_flutter(page, text="Nguyễn Minh Đức")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "tc07_search_by_author.png"))

    # Assert (B3: count AND content via aria-labels)
    # Note: Flutter CanvasKit stores author names in aria-label, not text nodes.
    author_results = page.locator('flt-semantics[role="group"][aria-label*="Nguyễn Minh Đức"]')
    assert author_results.count() > 0, (
        "TC-07 FAILED: Expected books by 'Nguyễn Minh Đức' (BOOK001, BOOK009). "
        "No matching book card found."
    )

    # B3: Also verify via all aria-labels
    all_labels = " ".join(
        el.get_attribute("aria-label") or ""
        for el in page.locator("flt-semantics").all()
    )
    assert "Nguyễn Minh Đức" in all_labels, (
        f"TC-07 FAILED: Author 'Nguyễn Minh Đức' not found in any aria-label. "
        f"Got labels: {all_labels[:300]}"
    )

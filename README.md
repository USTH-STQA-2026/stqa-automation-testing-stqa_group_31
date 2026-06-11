# STQA Library Automation — Starter Template

Bài tập thực hành Kiểm thử Web UI tự động cho môn Kiểm thử và Đảm bảo chất lượng phần mềm (STQA).  
*(A hands-on Automated Web UI Testing assignment for the Software Testing & Quality Assurance (STQA) course.)*

Sử dụng Playwright + Python để kiểm thử hệ thống Mượn sách Thư viện ABC tại https://stqa.rbc.vn.  
*(Uses Playwright + Python to test the Library Book Borrowing System.)*

---

## 👥 Thông tin nhóm / Team Information

| Thông tin | |
|-----------|---|
| Tên nhóm | Nhóm 31 |
| Lớp | STQA 2026 |
| Học kỳ | HK2 2025-2026 |

| # | MSSV | Họ và tên | Vai trò |
|---|------|-----------|---------|
| 1 | — | Nhóm trưởng | Nhóm trưởng |
| 2 | — | Thành viên | Thành viên |
| 3 | — | Thành viên | Thành viên |
| 4 | — | Thành viên | Thành viên |

---

## 📋 Danh sách Test Case / Test Case List

| TC | Mô tả | File | Trạng thái |
|----|-------|------|-----------|
| TC-01 | Đăng nhập thành công | test_login.py | ✅ Hoàn thành |
| TC-02 | Đăng nhập thất bại — sai mật khẩu | test_login.py | ✅ Hoàn thành |
| TC-03 | Đăng nhập thất bại — để trống | test_login.py | ✅ Hoàn thành |
| TC-04 | Tìm sách theo tên | test_search.py | ✅ Hoàn thành |
| TC-05 | Tìm sách — không có kết quả | test_search.py | ✅ Hoàn thành |
| TC-06 | Lọc theo thể loại | test_search.py | ✅ Hoàn thành |
| TC-07 | Tìm theo tác giả | test_search.py | ✅ Hoàn thành |
| TC-08 | Mượn sách | test_borrow_return.py | ✅ Hoàn thành |
| TC-09 | Xem sách đang mượn | test_borrow_return.py | ✅ Hoàn thành |
| TC-10 | Trả sách | test_borrow_return.py | ✅ Hoàn thành |
| TC-11 | Đăng xuất | test_general.py | ✅ Hoàn thành |
| TC-12 | Chuyển ngôn ngữ sang EN | test_general.py | ✅ Hoàn thành |

### Bonus Test Cases (B1)

| TC | Mô tả | File | Trạng thái |
|----|-------|------|-----------|
| TC-13 | Đăng nhập — email không tồn tại | test_login.py (parametrized) | ✅ Hoàn thành |
| TC-14 | Mượn sách — tài khoản bị tạm ngưng | test_borrow_return.py | ✅ Hoàn thành |
| TC-15 | Thủ thư xem tất cả phiếu mượn | test_general.py | ✅ Hoàn thành |

---

## 🚀 Cài đặt / Installation

```bash
git clone <repo-url>
cd stqa-library-automation-starter
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
playwright install chromium
```

## ⚙️ Cấu hình / Configuration

```bash
cp .env.example .env
```

Sửa `.env`:
```
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=ba.nguyen@email.com
TEST_PASSWORD=password123
TEST_DISPLAY_NAME=Nguyễn Học Bá
```

## ▶️ Chạy test / Running Tests

```bash
# Chạy tất cả
pytest -v

# Chạy từng file
pytest tests/test_login.py -v
pytest tests/test_search.py -v
pytest tests/test_borrow_return.py -v
pytest tests/test_general.py -v
```

Screenshots được lưu vào thư mục `screenshots/`.


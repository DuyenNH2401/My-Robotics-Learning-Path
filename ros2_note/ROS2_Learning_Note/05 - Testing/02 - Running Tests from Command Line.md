---
tags:
  - ros2
  - testing
  - colcon
  - ctest
  - pytest
  - cli
  - intermediate
created: 2026-08-25
aliases:
  - Chạy Kiểm thử từ Dòng lệnh với colcon
  - Running Tests in ROS 2 from the Command Line
---

# 💻 Chạy Kiểm thử từ Dòng lệnh với colcon (Running Tests from CLI)

> [!INFO] **Mục tiêu bài học**
> Làm chủ các lệnh thực thi kiểm thử trong ROS 2 với **`colcon test`**, kiểm tra báo cáo kết quả với **`colcon test-result`**, lọc các ca kiểm thử chi tiết và truyền tham số trực tiếp cho CTest / Pytest.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 10 phút
> - **Bài trước:** [[01 - Why Automatic Tests in ROS 2|Tại sao cần Kiểm thử Tự động trong ROS 2]]
> - **Bài tiếp theo:** [[03 - Writing Unit Tests with C++ and GTest|Viết Unit Test C++ với GTest]]

---

## 📖 Bối cảnh (Background)

Trong ROS 2, công cụ `colcon` không chỉ chịu trách nhiệm biên dịch (`colcon build`) mà còn tích hợp sẵn trình quản lý thực thi toàn bộ bài test của các package (bao gồm Unit Test C++ GTest, Unit Test Python Pytest, Linter kiểm tra code style `ament_lint`, và Integration Test `launch_testing`).

---

## 🛠️ Các lệnh thực thi Kiểm thử Cốt lõi

### 1. Chạy toàn bộ Tests trong Workspace
Tại thư mục gốc của workspace (`~/ros2_ws`), chạy:

```bash
colcon test
```

> [!NOTE]
> Bạn **không cần phải source workspace trước khi chạy test**. `colcon test` sẽ tự động thiết lập biến môi trường và nạp các dependencies cần thiết cho từng gói độc lập.

---

### 2. Chạy Test cho một hoặc nhiều Package cụ thể
Dùng cờ `--packages-select` để tiết kiệm thời gian khi phát triển:

```bash
colcon test --packages-select my_robot_pkg
```

---

### 3. Kiểm tra Báo cáo Kết quả (Test Results)

Sau khi `colcon test` hoàn tất, xem tóm tắt kết quả:

```bash
colcon test-result --all
```

Nếu có ca kiểm thử bị thất bại (`Failed`), sử dụng cờ **`--verbose`** để in chi tiết thông báo lỗi và dòng mã bị assert fail:

```bash
colcon test-result --all --verbose
```

---

## 🚀 Truyền tham số Nâng cao

### 1. Truyền cờ cho CTest (Package C++)
```bash
colcon test --packages-select cpp_package --ctest-args tests
```

### 2. Truyền cờ cho Pytest (Package Python)
Chỉ chạy một hàm test cụ thể và in log ra console theo thời gian thực:

```bash
colcon test --packages-select py_package \
  --pytest-args -k test_math_function \
  --event-handlers console_cohesion+
```

---

## 📌 Tóm tắt (Summary)
- Chu trình chuẩn: `colcon test --packages-select <pkg>` $\rightarrow$ `colcon test-result --all --verbose`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[01 - Why Automatic Tests in ROS 2|Tại sao cần Kiểm thử Tự động trong ROS 2]]
- 💻 Viết Test C++: [[03 - Writing Unit Tests with C++ and GTest|Viết Unit Test C++ với GTest]]
- 🐍 Viết Test Python: [[04 - Writing Unit Tests with Python and Pytest|Viết Unit Test Python với Pytest]]

---
tags:
  - ros2
  - testing
  - pytest
  - python
  - unit-tests
  - intermediate
created: 2026-08-25
aliases:
  - Viết Unit Test Python với Pytest
  - Writing Basic Tests with Python
---

# 🐍 Viết Unit Test Python với Pytest (pytest in ament_python)

> [!INFO] **Mục tiêu bài học**
> Học cách tổ chức thư mục kiểm thử trong package Python (`ament_python`), cấu hình `extras_require` trong `setup.py`, viết các hàm kiểm tra tự động với **`pytest`** và câu lệnh `assert`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 10 phút
> - **Bài trước:** [[02 - Running Tests from Command Line|Chạy Kiểm thử từ Dòng lệnh với colcon]]
> - **Bài song song (C++):** [[03 - Writing Unit Tests with C++ and GTest|Viết Unit Test C++ với GTest]]
> - **Bài tiếp theo:** [[05 - Writing Integration Tests with launch_testing|Viết Integration Test với launch_testing]]

---

## 📖 Bối cảnh (Background)

Trong các package ROS 2 viết bằng Python, framework kiểm thử tiêu chuẩn và mạnh mẽ nhất là **`pytest`**. `pytest` cho phép viết các bài test cực kỳ ngắn gọn và tự nhiên bằng cú pháp `assert` có sẵn của ngôn ngữ Python.

---

## 🛠️ Cấu trúc Thư mục và File cấu hình

### 1. Cấu trúc thư mục chuẩn
Toàn bộ các file kiểm thử phải được đặt trong thư mục **`tests/`** hoặc `test/` ở cấp cao nhất của package và tuân theo tiền tố **`test_*.py`**:

```text
my_python_package/
├── my_python_package/
│   ├── __init__.py
│   └── robot_controller.py
├── package.xml
├── setup.cfg
├── setup.py
└── tests/
    ├── test_copyright.py
    └── test_robot_controller.py
```

---

### 2. Cấu hình `setup.py`
Khai báo `pytest` trong mục `extras_require`:

```python
from setuptools import find_packages, setup

package_name = 'my_python_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    # ...
    extras_require={
        'test': ['pytest'],
    },
)
```

---

## ✍️ Viết mã kiểm thử (`tests/test_robot_controller.py`)

Tất cả các hàm kiểm thử bắt buộc phải có tiền tố **`test_`**:

```python
import pytest
from my_python_package.robot_controller import calculate_wheel_speeds


def test_basic_arithmetic():
    assert 2 + 2 == 4


def test_wheel_speeds_forward():
    # Giả sử robot đi thẳng với vận tốc 1.0 m/s
    v_left, v_right = calculate_wheel_speeds(linear_v=1.0, angular_v=0.0)
    
    assert v_left == pytest.approx(1.0, rel=1e-3)
    assert v_right == pytest.approx(1.0, rel=1e-3)


def test_wheel_speeds_turning():
    # Giả sử robot quay tại chỗ
    v_left, v_right = calculate_wheel_speeds(linear_v=0.0, angular_v=1.0)
    
    # Bánh trái và bánh phải phải quay ngược chiều nhau
    assert v_left == -v_right
```

---

## 🚀 Chạy kiểm thử

```bash
cd ~/ros2_ws
colcon test --packages-select my_python_package
colcon test-result --all --verbose
```

Chạy và xem trực tiếp kết quả chi tiết của pytest:
```bash
colcon test --packages-select my_python_package --event-handlers console_cohesion+
```

---

## 📌 Tóm tắt (Summary)
- Tạo thư mục `tests/` với các file `test_*.py`.
- Dùng từ khóa `assert` tiêu chuẩn kết hợp với `pytest.approx` để so sánh số thực (floating point).

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[03 - Writing Unit Tests with C++ and GTest|Viết Unit Test C++ với GTest]]
- ➡️ Bài tiếp theo: [[05 - Writing Integration Tests with launch_testing|Viết Integration Test với launch_testing]]

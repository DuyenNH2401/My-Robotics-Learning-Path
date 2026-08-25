---
tags:
  - ros2
  - package
  - ament_cmake
  - ament_python
  - package_xml
  - beginner
created: 2026-08-25
aliases:
  - Tạo một Package trong ROS 2
  - Creating a package
---

# 📦 Tạo một Package trong ROS 2 (Creating a Package)

> [!INFO] **Mục tiêu bài học**
> Học cách tạo một **Package** mới hỗ trợ C++ (`ament_cmake`) hoặc Python (`ament_python`), tìm hiểu cấu trúc tệp tin tối thiểu, tùy chỉnh `package.xml` và chạy node thực thi đầu tiên.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[02 - Creating a Workspace|Tạo Workspace và Thiết lập Overlay]]
> - **Bài tiếp theo:** [[04 - Writing PubSub (C++)|Viết Publisher và Subscriber đơn giản (C++)]]

---

## 📖 Bối cảnh (Background)

### 1. Package trong ROS 2 là gì?
**Package** là đơn vị tổ chức mã nguồn cơ bản nhất trong ROS 2. Nếu bạn muốn cài đặt, quản lý dependencies hoặc chia sẻ mã nguồn với cộng đồng, bạn cần đóng gói code vào trong một package.

ROS 2 sử dụng **ament** làm hệ thống xây dựng (*build system*) và **colcon** làm công cụ biên dịch (*build tool*).

### 2. Cấu trúc chuẩn của một Package

```text
📁 Package C++ (ament_cmake)            📁 Package Python (ament_python)
my_cpp_pkg/                             my_py_pkg/
├── CMakeLists.txt                      ├── package.xml
├── package.xml                         ├── setup.py
├── include/my_cpp_pkg/                 ├── setup.cfg
└── src/                                ├── resource/my_py_pkg
    └── my_node.cpp                     └── my_py_pkg/
                                            ├── __init__.py
                                            └── my_node.py
```

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package với lệnh `ros2 pkg create`
Di chuyển vào thư mục `src` của workspace:

```bash
cd ~/ros2_ws/src
```

#### Tạo Package C++ (`ament_cmake`):
```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 --node-name my_node my_package
```

#### Tạo Package Python (`ament_python`):
```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name my_node my_package_py
```

> [!NOTE] **Ý nghĩa các cờ tùy chọn:**
> - `--build-type`: Chọn `ament_cmake` (cho C++) hoặc `ament_python` (cho Python).
> - `--license`: Khai báo giấy phép mã nguồn (ví dụ: `Apache-2.0`, `MIT`, `GPL-3.0`).
> - `--node-name`: Tự động sinh ra một file mã nguồn mẫu chứa node in ra *"Hello World"*.

---

### 2. Biên dịch Package với `colcon`
Quay về thư mục gốc của workspace và chỉ định build riêng package vừa tạo:

```bash
cd ~/ros2_ws
colcon build --packages-select my_package
```

---

### 3. Nạp môi trường và Chạy thử Node
Mở terminal mới, nạp setup script và chạy node:

```bash
cd ~/ros2_ws
source install/local_setup.bash

ros2 run my_package my_node
```
Kết quả trên terminal:
```text
hello world my_package package
```

---

### 4. Tùy chỉnh thông tin trong `package.xml`
File `package.xml` chứa toàn bộ siêu dữ liệu (metadata) của package. Mở file `package.xml` và cập nhật các trường quan trọng:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_package</name>
  <version>0.0.0</version>
  <description>Package thực hành tự tạo đầu tiên trong ROS 2</description>
  <maintainer email="your_email@domain.com">Tên Của Bạn</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- Khai báo các thư viện phụ thuộc ở đây -->
  <depend>rclcpp</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

> [!TIP] **Các thẻ Dependencies thường dùng:**
> - `<depend>`: Thư viện cần thiết cho cả lúc build và lúc chạy (thường dùng nhất).
> - `<buildtool_depend>`: Công cụ hỗ trợ build (như `ament_cmake`, `rosidl_default_generators`).
> - `<exec_depend>`: Thư viện chỉ cần lúc runtime (thường dùng cho package Python hoặc thư viện dynamic).
> - `<test_depend>`: Thư viện phục vụ chạy unit test.

---

## 📌 Tóm tắt (Summary)
- Sử dụng `ros2 pkg create` để sinh nhanh cấu trúc thư mục chuẩn.
- Đảm bảo khai báo đầy đủ thông tin maintainer, license và dependencies trong `package.xml` để `rosdep` và `colcon` hoạt động chính xác.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[02 - Creating a Workspace|Tạo Workspace và Thiết lập Overlay]]
- ➡️ Bài tiếp theo: [[04 - Writing PubSub (C++)|Viết Publisher và Subscriber đơn giản (C++)]] hoặc [[05 - Writing PubSub (Python)|Viết Publisher và Subscriber (Python)]]

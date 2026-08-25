---
tags:
  - ros2
  - interfaces
  - custom-msg
  - custom-srv
  - rosidl
  - beginner
created: 2026-08-25
aliases:
  - Tạo Message và Service tùy chỉnh
  - Creating custom msg and srv files
---

# 📝 Tạo Message và Service tùy chỉnh (Creating custom msg and srv files)

> [!INFO] **Mục tiêu bài học**
> Học cách tự định nghĩa các cấu trúc dữ liệu tùy chỉnh (**Custom Messages `.msg`** và **Custom Services `.srv`**), đóng gói chúng vào package riêng bằng `rosidl`, và sử dụng lại trong cả mã nguồn C++ và Python.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[06 - Writing Service Client (C++)|Viết Service/Client (C++)]] / [[07 - Writing Service Client (Python)|Viết Service/Client (Python)]]
> - **Bài tiếp theo:** [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]]

---

## 📖 Bối cảnh (Background)

Mặc dù ROS 2 cung cấp sẵn nhiều gói giao diện chuẩn (như `std_msgs`, `geometry_msgs`, `sensor_msgs`), trong các dự án robot thực tế bạn thường xuyên phải tự tạo các kiểu dữ liệu chuyên biệt.

> [!IMPORTANT] **Quy tắc vàng về Package chứa Interface:**
> - Package chứa file `.msg` và `.srv` **bắt buộc phải là `ament_cmake`** (không dùng `ament_python`).
> - Tuy nhiên, các interface sau khi được biên dịch có thể sử dụng bình thường trong **cả node C++ và node Python**.
> - Khuyến nghị nên tách riêng các định nghĩa interface thành một package độc lập (ví dụ `my_robot_interfaces`) để các package khác dễ dàng tái sử dụng.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package `tutorial_interfaces`
Tạo package giao diện trong thư mục `src`:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 tutorial_interfaces
cd tutorial_interfaces
mkdir msg srv
```

---

### 2. Định nghĩa các file `.msg` và `.srv`

#### 2.1 File `msg/Num.msg`:
Truyền một số nguyên 64-bit:
```text
int64 num
```

#### 2.2 File `msg/Sphere.msg`:
Sử dụng lồng ghép kiểu message từ package khác (`geometry_msgs/Point`):
```text
geometry_msgs/Point center
float64 radius
```

#### 2.3 File `srv/AddThreeInts.srv`:
Yêu cầu cộng 3 số nguyên và trả về tổng:
```text
int64 a
int64 b
int64 c
---
int64 sum
```

---

### 3. Cấu hình `CMakeLists.txt`
Sử dụng macro `rosidl_generate_interfaces` để sinh mã nguồn C++ và Python tự động:

```cmake
cmake_minimum_required(VERSION 3.20)
project(tutorial_interfaces)

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Num.msg"
  "msg/Sphere.msg"
  "srv/AddThreeInts.srv"
  DEPENDENCIES geometry_msgs
)

ament_package()
```

---

### 4. Cấu hình `package.xml`
Bổ sung các thẻ sinh mã và nhóm giao diện:

```xml
<depend>geometry_msgs</depend>

<!-- Thư viện sinh mã lúc build -->
<buildtool_depend>rosidl_default_generators</buildtool_depend>

<!-- Thư viện runtime để node có thể import/include -->
<exec_depend>rosidl_default_runtime</exec_depend>

<!-- Khai báo package thuộc nhóm interface -->
<member_of_group>rosidl_interface_packages</member_of_group>
```

---

### 5. Biên dịch Package Interface

```bash
cd ~/ros2_ws
colcon build --packages-select tutorial_interfaces
```

Sau khi build xong, mở terminal mới, source workspace và kiểm tra interface đã xuất hiện chưa:

```bash
source install/setup.bash

# Kiểm tra Message
ros2 interface show tutorial_interfaces/msg/Num
ros2 interface show tutorial_interfaces/msg/Sphere

# Kiểm tra Service
ros2 interface show tutorial_interfaces/srv/AddThreeInts
```

---

## 💻 Sử dụng Custom Interface trong Node C++

### Trong mã nguồn C++:
```cpp
// Include header sinh tự động: <tên_pkg>/<loại>/<tên_file_snake_case>.hpp
#include "tutorial_interfaces/msg/num.hpp"
#include "tutorial_interfaces/srv/add_three_ints.hpp"

// Khởi tạo Publisher
auto pub = node->create_publisher<tutorial_interfaces::msg::Num>("custom_topic", 10);
auto msg = tutorial_interfaces::msg::Num();
msg.num = 42;
pub->publish(msg);
```

### Trong `CMakeLists.txt` của Node dùng interface:
```cmake
find_package(tutorial_interfaces REQUIRED)
target_link_libraries(my_node PUBLIC tutorial_interfaces::tutorial_interfaces)
```

### Trong `package.xml` của Node dùng interface:
```xml
<depend>tutorial_interfaces</depend>
```

---

## 🐍 Sử dụng Custom Interface trong Node Python

### Trong mã nguồn Python:
```python
# Import trực tiếp như một module Python tiêu chuẩn
from tutorial_interfaces.msg import Num
from tutorial_interfaces.srv import AddThreeInts

# Tạo message
msg = Num()
msg.num = 42
publisher.publish(msg)
```

---

## 📌 Tóm tắt (Summary)
- `rosidl` là công cụ cốt lõi giúp chuyển đổi các định nghĩa `.msg`, `.srv` thành struct/class trong C++ và Python.
- Nhớ khai báo `<member_of_group>rosidl_interface_packages</member_of_group>` trong `package.xml` và `rosidl_generate_interfaces()` trong `CMakeLists.txt`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[06 - Writing Service Client (C++)|Viết Service/Client (C++)]]
- ➡️ Bài tiếp theo: [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]]

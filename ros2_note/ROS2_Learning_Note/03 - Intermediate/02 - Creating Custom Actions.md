---
tags:
  - ros2
  - actions
  - custom-action
  - interfaces
  - rosidl
  - intermediate
created: 2026-08-25
aliases:
  - Tạo Action tùy chỉnh
  - Creating an action
---

# 🎯 Tạo Action tùy chỉnh (Creating an Action)

> [!INFO] **Mục tiêu bài học**
> Học cách tự định nghĩa giao diện [[07 - Understanding Actions|Action]] tùy chỉnh (`.action`) gồm 3 phần (**Goal**, **Result**, **Feedback**), cấu hình biên dịch tự động bằng `rosidl` trong package `ament_cmake`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 5 phút
> - **Bài trước:** [[01 - Managing Dependencies with rosdep|Quản lý Dependencies với rosdep]]
> - **Bài tiếp theo:** [[03 - Writing Action Server and Client (C++)|Viết Action Server và Client (C++)]] hoặc [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]

---

## 📖 Bối cảnh (Background)

Tương tự như cách định nghĩa [[08 - Creating Custom Interfaces (msg and srv)|Custom Message và Service]], file `.action` là bản thiết kế giao thức truyền thông cho các tác vụ tốn thời gian.

Một file `.action` luôn bao gồm **3 phần được ngăn cách bởi 2 dấu `---`**:
1. **Goal Request (Yêu cầu mục tiêu):** Dữ liệu Client gửi đến Server để bắt đầu tác vụ.
2. **Result (Kết quả cuối cùng):** Dữ liệu Server trả về khi tác vụ hoàn thành (`SUCCEEDED`, `CANCELED`, hoặc `ABORTED`).
3. **Feedback (Phản hồi định kỳ):** Dữ liệu Server phát liên tục cho Client biết tiến độ thực thi.

```text
# 1. Goal (Yêu cầu)
int32 order
---
# 2. Result (Kết quả)
int32[] sequence
---
# 3. Feedback (Tiến độ)
int32[] sequence
```

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package giao diện `custom_action_interfaces`
Tạo package dạng `ament_cmake` trong thư mục `src` của workspace:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces
cd custom_action_interfaces
mkdir action
```

> [!NOTE]
> Theo quy chuẩn phát triển ROS 2, các file interface (`.msg`, `.srv`, `.action`) nên được đặt trong một package giao diện riêng biệt để các node C++ và Python khác có thể cùng dùng chung.

---

### 2. Tạo file định nghĩa `Fibonacci.action`
Tạo file `action/Fibonacci.action` với nội dung tính dãy số Fibonacci:

```text
int32 order
---
int32[] sequence
---
int32[] sequence
```

- **Goal:** `order` (Bậc của dãy Fibonacci cần tính toán, ví dụ `order = 5`).
- **Result:** `sequence` (Mảng chứa toàn bộ dãy số hoàn chỉnh `[0, 1, 1, 2, 3, 5]`).
- **Feedback:** `sequence` (Mảng các số đã tính được đến thời điểm hiện tại gửi cập nhật sau mỗi bước).

---

### 3. Cấu hình `CMakeLists.txt` và `package.xml`

#### Cập nhật `CMakeLists.txt`:
Thêm macro `rosidl_generate_interfaces` trước dòng `ament_package()`:

```cmake
cmake_minimum_required(VERSION 3.20)
project(custom_action_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Đăng ký file action để sinh mã nguồn C++ và Python
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/Fibonacci.action"
)

ament_package()
```

#### Cập nhật `package.xml`:
```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

---

### 4. Biên dịch và Kiểm tra

Quay về thư mục gốc workspace và build package:
```bash
cd ~/ros2_ws
colcon build --packages-select custom_action_interfaces
```

Mở terminal mới, nạp setup script và kiểm tra action definition:
```bash
source install/local_setup.bash
ros2 interface show custom_action_interfaces/action/Fibonacci
```

Kết quả in ra đúng 3 phần của file `Fibonacci.action` chứng tỏ quá trình tạo và sinh code cho Action đã thành công!

---

## 📌 Tóm tắt (Summary)
- Action được định nghĩa trong file `.action` với 3 trường: **Goal**, **Result**, **Feedback**.
- Package chứa action phải sử dụng `rosidl_default_generators` và khai báo `<member_of_group>rosidl_interface_packages</member_of_group>`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[01 - Managing Dependencies with rosdep|Quản lý Dependencies với rosdep]]
- 💻 Viết Action Server/Client bằng C++: [[03 - Writing Action Server and Client (C++)|Viết Action Server và Client (C++)]]
- 🐍 Viết Action Server/Client bằng Python: [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]

---
tags:
  - ros2
  - colcon
  - build-tool
  - workspace
  - beginner
created: 2026-08-25
aliases:
  - Sử dụng colcon để build packages
  - Using colcon to build packages
---

# 🔨 Sử dụng colcon để build packages (Using colcon to build packages)

> [!INFO] **Mục tiêu bài học**
> Làm quen với công cụ biên dịch tiêu chuẩn **`colcon`** trong ROS 2: tạo workspace, tải mã nguồn mẫu, biên dịch với `--symlink-install`, chạy test và nạp môi trường thực thi.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 20 phút
> - **Mục lục tổng quan:** [[ROS 2 Learning Path]]
> - **Bài tiếp theo:** [[02 - Creating a Workspace|Tạo Workspace và Thiết lập Overlay]]

---

## 📖 Bối cảnh (Background)

**`colcon`** là công cụ build hợp nhất thế hệ mới của ROS 2, kế thừa và cải tiến từ các công cụ xây dựng trước đây của ROS 1 như `catkin_make`, `catkin_make_isolated`, `catkin_tools` và `ament_tools`.

### Cấu trúc thư mục của một colcon Workspace
`colcon` thực hiện biên dịch bên ngoài thư mục mã nguồn (*out-of-source builds*). Khi biên dịch, nó tự động sinh ra các thư mục ngang hàng với `src`:

```text
ros2_ws/
├── src/      # Nơi chứa mã nguồn các ROS packages (git clone, code tự viết)
├── build/    # Nơi lưu trữ các file tạm trung gian trong quá trình build (CMake cache, object files...)
├── install/  # Nơi các package được cài đặt đến (executables, libraries, setup scripts)
└── log/      # Nơi lưu nhật ký chi tiết các lần gọi lệnh colcon
```

> [!NOTE] **So sánh với catkin (ROS 1):**
> Trong `colcon` không còn thư mục `devel`. Toàn bộ sản phẩm chạy được sẽ nằm trực tiếp trong thư mục `install/`.

---

## 🛠️ Cài đặt & Chuẩn bị (Prerequisites)

Cài đặt tiện ích mở rộng đầy đủ cho `colcon`:
```bash
sudo apt update
sudo apt install python3-colcon-common-extensions
```

---

## 🚀 Các bước thực hành (Tasks)

### 1. Tạo Workspace
Tạo thư mục workspace `ros2_ws` và thư mục con `src`:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

---

### 2. Tải mã nguồn mẫu vào `src`
Clone repository chứa các ví dụ chuẩn của ROS 2 vào thư mục `src`:

```bash
git clone https://github.com/ros2/examples src/examples -b <distro>
```
*(Thay `<distro>` bằng bản phân phối của bạn, ví dụ `humble`, `jazzy`, `iron`...)*

---

### 3. Source môi trường Underlay
Trước khi build, bạn phải source môi trường ROS 2 gốc để cung cấp các dependencies nền tảng:

```bash
source /opt/ros/<distro>/setup.bash
```

---

### 4. Biên dịch Workspace với `colcon build`
Chạy lệnh biên dịch tại thư mục gốc của workspace (`~/ros2_ws`):

```bash
colcon build --symlink-install
```

> [!TIP] **Ý nghĩa của cờ `--symlink-install`:**
> Tùy chọn này tạo các liên kết mềm (symlink) từ `src/` tới `install/` cho các file không cần biên dịch (như script Python, launch file, file cấu hình YAML). Khi bạn chỉnh sửa mã nguồn Python, thay đổi sẽ có hiệu lực ngay mà **không cần chạy lại lệnh build**!

> [!WARNING] **Tránh tràn RAM trên thiết bị nhúng (Raspberry Pi, Jetson):**
> `colcon build` mặc định biên dịch đa luồng song song (parallel) có thể làm đơ máy. Hãy dùng cờ tuần tự:
> ```bash
> colcon build --symlink-install --executor sequential
> ```

---

### 5. Chạy kiểm thử tự động (Run Tests)
```bash
colcon test
```

---

### 6. Nạp môi trường thực thi (Source the environment)
Sau khi build xong, để sử dụng các executable và library vừa tạo:

```bash
source install/setup.bash
```

---

### 7. Chạy thử nghiệm Demo
Mở 2 terminal đã source `install/setup.bash` để kiểm tra kết quả:

```bash
# Terminal 1: Chạy Subscriber
ros2 run examples_rclcpp_minimal_subscriber subscriber_member_function

# Terminal 2: Chạy Publisher
ros2 run examples_rclcpp_minimal_publisher publisher_member_function
```

---

## 💡 Mẹo & Tiện ích nâng cao (Tips & Tricks)

### 1. Bỏ qua không build package với `COLCON_IGNORE`
Tạo một file rỗng tên `COLCON_IGNORE` bên trong thư mục package bất kỳ để `colcon` bỏ qua không index và không build package đó.

### 2. Chỉ build 1 package cụ thể
```bash
colcon build --packages-select <tên_package>
```

### 3. Tắt biên dịch Unit Test để tăng tốc
```bash
colcon build --cmake-args -DBUILD_TESTING=0
```

### 4. Cấu hình `colcon_cd`
Tiện ích `colcon_cd` cho phép nhảy nhanh đến thư mục của package bất kỳ từ bất cứ đâu:
```bash
echo "source /etc/profile.d/colcon_cd.sh" >> ~/.bashrc
echo "export _colcon_cd_root=/opt/ros/<distro>/" >> ~/.bashrc
```
Sử dụng: `colcon_cd <tên_package>` sẽ tự động `cd` đến thư mục package đó.

---

## 📌 Tóm tắt (Summary)
- `colcon` là công cụ build tiêu chuẩn cho các workspace ROS 2 chứa cả package C++ (`ament_cmake`) và Python (`ament_python`).
- Luôn nhớ: Thư mục `src/` chứa code, chạy `colcon build --symlink-install` tại root workspace, và `source install/setup.bash` trước khi chạy node.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Trở về: [[ROS 2 Learning Path|Lộ trình học ROS 2]]
- ➡️ Bài tiếp theo: [[02 - Creating a Workspace|Tạo Workspace và Thiết lập Overlay]]

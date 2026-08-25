---
tags:
  - ros2
  - rosbag
  - recording
  - playback
  - cli
  - beginner
created: 2026-08-25
aliases:
  - Ghi và Phát lại dữ liệu với ros2 bag
  - Recording and playing back data
---

# 📼 Ghi và Phát lại dữ liệu với ros2 bag (Recording and Playing Back Data)

> [!INFO] **Mục tiêu bài học**
> Sử dụng công cụ **`ros2 bag`** để ghi lại (record) và phát lại (replay) dữ liệu từ [[04 - Understanding Topics|Topics]], [[05 - Understanding Services|Services]], và [[07 - Understanding Actions|Actions]] phục vụ việc kiểm thử, mô phỏng và gỡ lỗi mà không cần chạy lại robot thật.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[09 - Launching Nodes|Khởi chạy Nodes với Launch Files]]
> - **Tổng quan lộ trình:** [[ROS 2 Learning Path]]

---

## 📖 Bối cảnh (Background)

**`ros2 bag`** là công cụ thu thập và lưu trữ toàn bộ dữ liệu trao đổi trong mạng ROS 2 vào cơ sở dữ liệu định dạng **MCAP** (hoặc SQLite3):

- **Tại sao cần dùng rosbag?**
  - **Tái hiện thí nghiệm:** Phát lại chính xác dữ liệu cảm biến (LiDAR, Camera, IMU) đã thu ngoài thực địa để thuật toán xử lý lặp đi lặp lại trong phòng lab.
  - **Gỡ lỗi (Debugging):** Phân tích các sự cố xảy ra ngẫu nhiên bằng cách tua chậm hoặc dừng lại từng khung dữ liệu.
  - **Chia sẻ bộ dữ liệu (Datasets):** Gửi dữ liệu đã ghi cho các thành viên trong nhóm nghiên cứu để cùng phát triển thuật toán.

---

## 🛠️ 1. Quản lý dữ liệu Topic (Managing Topic Data)

### 1.1 Chuẩn bị môi trường
Khởi động Turtlesim và teleop:
```bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key
```

Tạo một thư mục riêng để lưu các file bag:
```bash
mkdir bag_files && cd bag_files
```

---

### 1.2 Ghi dữ liệu một Topic
Ghi lại lệnh điều khiển rùa trên topic `/turtle1/cmd_vel`:

```bash
ros2 bag record --topics /turtle1/cmd_vel
```
- Quay sang cửa sổ teleop và nhấn các phím mũi tên để di chuyển rùa.
- Nhấn `Ctrl + C` tại terminal record để kết thúc quá trình ghi. Thư mục chứa dữ liệu có tên dạng `rosbag2_YYYY_MM_DD-HH_MM_SS` sẽ được tạo ra.

---

### 1.3 Ghi nhiều Topic và đặt tên thư mục tùy chỉnh
Dùng tùy chọn `-o <folder_name>`:

```bash
ros2 bag record -o subset --topics /turtle1/cmd_vel /turtle1/pose
```
*(Ghi đồng thời cả lệnh vận tốc và tọa độ vị trí của rùa vào thư mục `subset`)*

> [!TIP] **Các tùy chọn nâng cao:**
> - `-a` (hoặc `--all`): Ghi lại **toàn bộ** topic hiện có trên hệ thống.
> - `-d <số_giây>`: Tự động chia nhỏ bản ghi thành các file sau mỗi khoảng thời gian (ví dụ `-d 60` sau mỗi 1 phút chia 1 file).
> - `-b <dung_lượng_byte>`: Tự động cắt file khi dung lượng vượt quá ngưỡng quy định.

---

### 1.4 Kiểm tra thông tin bản ghi với `ros2 bag info`
Xem chi tiết file bag mà không cần phát:

```bash
ros2 bag info subset
```

Kết quả in ra thông số chi tiết:
```text
Files:             subset_0.mcap
Bag size:          228.5 KiB
Storage id:        mcap
ROS Distro:        humble / jazzy
Duration:          48.47s
Messages:          3013
Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 9
                   Topic: /turtle1/pose    | Type: turtlesim_msgs/msg/Pose | Count: 3004
```

---

### 1.5 Phát lại dữ liệu Topic với `ros2 bag play`
Tắt cửa sổ teleop, giữ cửa sổ `turtlesim_node` mở và chạy lệnh:

```bash
ros2 bag play subset
```
Chú rùa trong Turtlesim sẽ tự động chuyển động lại y hệt như những gì bạn đã điều khiển trong lúc ghi!

> [!NOTE] **Phím tắt điều khiển khi phát lại (Interactive Playback):**
> - `SPACE`: Tạm dừng (Pause) / Tiếp tục (Resume).
> - `CURSOR_RIGHT` (Phím mũi tên phải): Phát từng thông điệp tiếp theo (Step by step).
> - `CURSOR_UP` / `DOWN`: Tăng / Giảm 10% tốc độ phát lại.

---

## 🛠️ 2. Ghi và Phát lại dữ liệu Service (Managing Service Data)

Để ghi được dữ liệu của Service, tính năng **Service Introspection** phải được kích hoạt trên Node:

```bash
# Ghi một service cụ thể
ros2 bag record --service /add_two_ints

# Ghi toàn bộ các service
ros2 bag record --all-services
```

### Phát lại yêu cầu Service (Replay Service Requests):
Khi phát lại, dùng cờ `--publish-service-requests` để rosbag đóng vai trò như Service Client gửi lại các request đến Service Server:

```bash
ros2 bag play --publish-service-requests <bag_folder_name>
```

---

## 🛠️ 3. Ghi và Phát lại dữ liệu Action (Managing Action Data)

Tương tự Service, Action cần được kích hoạt **Action Introspection**:

```bash
# Ghi một action cụ thể (bao gồm Goal, Feedback, Result và Status)
ros2 bag record --action /fibonacci

# Ghi toàn bộ actions
ros2 bag record --all-actions
```

### Phát lại Action (Replay Actions):
Dùng cờ `--send-actions-as-client` để phát lại các mục tiêu Goal tới Action Server:

```bash
ros2 bag play --send-actions-as-client <bag_folder_name>
```

---

## 📌 Tóm tắt (Summary)
- `ros2 bag` là bộ công cụ toàn diện giúp lưu trữ và phát lại vòng đời dữ liệu của Topic, Service và Action.
- Hỗ trợ định dạng lưu trữ hiện đại **MCAP** cho hiệu năng cao và khả năng đọc tuần tự tối ưu.

---

## 🎉 Hoàn thành Lộ trình Beginner CLI Tools!
Chúc mừng bạn đã hoàn thành trọn bộ 10 bài học về bộ công cụ dòng lệnh cơ bản của ROS 2. 

- ⬅️ Trở về: [[ROS 2 Learning Path|Lộ trình học ROS 2]]
- 🚀 **Chặng tiếp theo:** Chuyển sang lộ trình **Beginner: Client Libraries** để bắt đầu tự viết code C++ (`rclcpp`) và Python (`rclpy`) xây dựng các Node hoàn chỉnh!

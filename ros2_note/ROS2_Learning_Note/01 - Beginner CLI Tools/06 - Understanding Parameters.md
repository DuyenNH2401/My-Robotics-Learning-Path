---
tags:
  - ros2
  - parameters
  - configuration
  - yaml
  - cli
  - beginner
created: 2026-08-25
aliases:
  - Tìm hiểu về Parameters trong ROS 2
  - Understanding parameters
---

# ⚙️ Tìm hiểu về Parameters trong ROS 2 (Understanding Parameters)

> [!INFO] **Mục tiêu bài học**
> Học cách đọc (get), thay đổi (set), lưu trữ (dump) và nạp lại (load) các thông số cấu hình (**Parameters**) của các Node trong ROS 2.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 5 phút
> - **Bài trước:** [[05 - Understanding Services|Tìm hiểu về Services trong ROS 2]]
> - **Bài tiếp theo:** [[07 - Understanding Actions|Tìm hiểu về Actions trong ROS 2]]

---

## 📖 Bối cảnh (Background)

**Parameter (Tham số cấu hình)** là giá trị thiết lập dành riêng cho một [[03 - Understanding Nodes|Node]]. Bạn có thể xem parameter như là "bảng cài đặt" (settings) của node đó.

- **Kiểu dữ liệu hỗ trợ:** `integer`, `float`, `boolean`, `string`, `list/array`.
- **Phạm vi quản lý:** Mỗi node tự quản lý các parameter của riêng mình.
- **Tính năng hữu ích:** Cho phép thay đổi hành vi hoạt động của robot (ví dụ: tốc độ tối đa, ngưỡng khoảng cách an toàn, màu sắc giao diện, chọn cổng serial) tại thời điểm khởi động hoặc ngay trong lúc đang chạy (runtime) mà **không cần biên dịch lại mã nguồn**.

---

## 🛠️ Các lệnh CLI với Parameters (Tasks)

### 1. Khởi động môi trường
Mở hai terminal chạy các node quen thuộc:
```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2
ros2 run turtlesim turtle_teleop_key
```

---

### 2. Liệt kê các Parameter với `ros2 param list`
Xem toàn bộ parameter của các node đang chạy:

```bash
ros2 param list
```

Kết quả trả về:
```text
/teleop_turtle:
  scale_angular
  scale_linear
  use_sim_time
  ...
/turtlesim:
  background_b
  background_g
  background_r
  use_sim_time
  ...
```

> [!NOTE]
> Parameter `use_sim_time` có mặt ở hầu hết mọi node ROS 2. Khi đặt là `true`, node sẽ lấy mốc thời gian từ topic `/clock` của trình mô phỏng (Gazebo, Isaac Sim) thay vì đồng hồ hệ thống thực tế.

---

### 3. Đọc giá trị Parameter với `ros2 param get`
Cú pháp:
```bash
ros2 param get <node_name> <parameter_name>
```

*Ví dụ đọc giá trị màu nền xanh lá của Turtlesim:*
```bash
ros2 param get /turtlesim background_g
# Trả về: Integer value is: 86
```

Đọc một parameter áp dụng trên toàn bộ các node (bỏ qua tên node):
```bash
ros2 param get use_sim_time
```

---

### 4. Thay đổi giá trị Parameter khi Node đang chạy với `ros2 param set`
Cú pháp:
```bash
ros2 param set <node_name> <parameter_name> <value>
```

*Ví dụ đổi màu nền cửa sổ Turtlesim sang màu tím:*
```bash
ros2 param set /turtlesim background_r 150
```
Màn hình Turtlesim sẽ đổi màu ngay lập tức!

> [!WARNING]
> Thay đổi bằng lệnh `ros2 param set` chỉ có hiệu lực tạm thời trong phiên làm việc hiện tại. Khi tắt node và bật lại, node sẽ quay về giá trị mặc định trừ khi bạn lưu ra file hoặc truyền file cấu hình lúc khởi động.

---

### 5. Xuất cấu hình Parameter ra file YAML với `ros2 param dump`
Lưu toàn bộ cài đặt hiện tại của node ra file:

```bash
ros2 param dump /turtlesim > turtlesim.yaml
```

Nội dung file `turtlesim.yaml` được tạo ra:
```yaml
/turtlesim:
  ros__parameters:
    background_b: 255
    background_g: 86
    background_r: 150
    use_sim_time: false
```

---

### 6. Nạp cấu hình từ file YAML với `ros2 param load`
Nạp các giá trị đã lưu vào một node đang chạy:

```bash
ros2 param load /turtlesim turtlesim.yaml
```

---

### 7. Khởi chạy Node kèm file cấu hình Parameter
Để khởi động một node và tự động áp dụng các thiết lập từ file YAML:

```bash
ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml
```

> [!TIP]
> Khi nạp file parameter lúc khởi động node (`--params-file`), tất cả các giá trị (kể cả những tham số dạng *read-only* chỉ nạp một lần) đều sẽ được cập nhật chính xác.

---

## 📌 Tóm tắt (Summary)
- **Parameters** là giải pháp chuẩn trong ROS 2 để cấu hình node động.
- Dùng `ros2 param get / set` để xem và thay đổi nhanh lúc runtime.
- Dùng file định dạng **YAML** kết hợp với `dump / load` hoặc `--params-file` để quản lý cấu hình chuyên nghiệp cho các hệ thống lớn.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[05 - Understanding Services|Tìm hiểu về Services trong ROS 2]]
- ➡️ Bài tiếp theo: [[07 - Understanding Actions|Tìm hiểu về Actions trong ROS 2]]

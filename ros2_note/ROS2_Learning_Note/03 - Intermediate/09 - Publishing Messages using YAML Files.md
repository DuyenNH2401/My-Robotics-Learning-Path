---
tags:
  - ros2
  - topic
  - yaml
  - cli
  - messages
  - intermediate
created: 2026-08-25
aliases:
  - Publish Message qua File YAML
  - Publishing messages using YAML files
---

# 📄 Publish Message qua File YAML (Publishing messages using YAML files)

> [!INFO] **Mục tiêu bài học**
> Học cách trích xuất dữ liệu thông điệp phức tạp từ [[04 - Understanding Topics|Topic]] ra file YAML bằng `ros2 topic echo`, chỉnh sửa và phát lại tuần tự nhiều thông điệp bằng cờ `--yaml-file` trong `ros2 topic pub`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 5 phút
> - **Bài trước:** [[08 - Using Node Interfaces Template Class (C++)|Sử dụng Node Interfaces Template Class (C++)]]
> - **Bài tiếp theo:** [[10 - Monitoring Parameter Changes (C++)|Theo dõi thay đổi Parameter (C++)]]

---

## 📖 Bối cảnh (Background)

Khi kiểm thử các thông điệp có cấu trúc dữ liệu lồng nhau phức tạp (ví dụ: `sensor_msgs/msg/LaserScan`, `nav_msgs/msg/Path`, hoặc `geometry_msgs/msg/PoseWithCovarianceStamped`), việc gõ toàn bộ chuỗi JSON/YAML trực tiếp trên dòng lệnh là rất mất thời gian và dễ sai sót cú pháp.

Giải pháp tiện lợi là **lưu cấu trúc ra file `.yaml`**, chỉnh sửa giá trị mong muốn và nạp lại khi phát tin.

---

## 🛠️ Các bước thực hành (Tasks)

### 1. Trích xuất Message mẫu ra file YAML
Sử dụng toán tử điều hướng đầu ra `>` của Linux để lưu 1 thông điệp duy nhất (`--once`):

```bash
ros2 topic echo --once /turtle1/cmd_vel > cmd_vel.yaml
```

File `cmd_vel.yaml` được tạo ra có định dạng:
```yaml
linear:
  x: 1.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

---

### 2. Xuất bản dữ liệu từ File YAML với `--yaml-file`
Cú pháp:
```bash
ros2 topic pub <topic_name> <msg_type> --yaml-file <path_to_yaml>
```

*Ví dụ:*
```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist --yaml-file cmd_vel.yaml
```

---

### 3. Xuất bản chuỗi nhiều thông điệp liên tiếp
Bạn có thể định nghĩa một kịch bản di chuyển hoàn chỉnh bằng cách thêm nhiều khối dữ liệu ngăn cách bởi dấu `---` trong cùng một file `cmd_vel.yaml`:

```yaml
linear:
  x: 1.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 1.5
---
linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

Khi chạy lại lệnh `ros2 topic pub ... --yaml-file cmd_vel.yaml`, hệ thống sẽ lần lượt phát cả 3 thông điệp trên theo thứ tự tuần tự.

---

## 📌 Tóm tắt (Summary)
- Sử dụng `ros2 topic echo --once > file.yaml` để lấy mẫu cấu trúc tin nhắn chuẩn.
- Sử dụng `ros2 topic pub --yaml-file file.yaml` để kiểm thử các kịch bản dữ liệu phức tạp dễ dàng.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[08 - Using Node Interfaces Template Class (C++)|Sử dụng Node Interfaces Template Class (C++)]]
- ➡️ Bài tiếp theo: [[10 - Monitoring Parameter Changes (C++)|Theo dõi thay đổi Parameter (C++)]]

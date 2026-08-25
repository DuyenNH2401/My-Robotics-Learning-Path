---
tags:
  - ros2
  - ros2doctor
  - troubleshooting
  - diagnostic
  - cli
  - beginner
created: 2026-08-25
aliases:
  - Kiểm tra hệ thống với ros2doctor
  - Using ros2doctor to identify issues
---

# 🩺 Kiểm tra và Chẩn đoán hệ thống với ros2doctor (Using ros2doctor to identify issues)

> [!INFO] **Mục tiêu bài học**
> Sử dụng công cụ **`ros2doctor`** (`ros2 doctor`) để kiểm tra toàn diện cấu hình môi trường, mạng, middleware và phát hiện các vấn đề tiềm ẩn trong hệ thống ROS 2 đang chạy.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 10 phút
> - **Bài trước:** [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]] / [[10 - Using Parameters in a Class (Python)|Sử dụng Parameters trong Class (Python)]]
> - **Bài tiếp theo:** [[12 - Creating and Using Plugins (C++)|Tạo và Sử dụng Plugins (C++)]]

---

## 📖 Bối cảnh (Background)

Khi hệ thống ROS 2 hoạt động không như mong đợi (ví dụ: các node không nhìn thấy nhau, mất gói tin, xung đột IP, biến môi trường chưa thiết lập), **`ros2doctor`** đóng vai trò như một "bác sĩ" tự động rà soát toàn bộ các thành phần:
- Nền tảng hệ điều hành (Platform) và phiên bản ROS.
- Cấu hình mạng (Network Interfaces, Multicast, Domain ID).
- Middleware DDS (RMW).
- Tình trạng kết nối giữa các Publisher và Subscriber trên hệ thống đang chạy.

---

## 🛠️ Các lệnh Chẩn đoán (Tasks)

### 1. Kiểm tra tổng quát môi trường cài đặt
Mở terminal đã source ROS 2 và chạy lệnh:

```bash
ros2 doctor
```

- Nếu hệ thống hoàn hảo: `All <n> checks passed`.
- Nếu có vấn đề không lý tưởng, hệ thống sẽ đưa ra các `UserWarning`:
  - Ví dụ cảnh báo bản phân phối thử nghiệm (prerelease):
    ```text
    UserWarning: Distribution <distro> is not fully supported or tested.
    ```
- Nếu có lỗi nghiêm trọng làm hỏng hệ thống:
  ```text
  1/3 checks failed
  Failed modules: network
  ```

---

### 2. Kiểm tra Đồ thị truyền thông trên hệ thống đang chạy
Chạy thử `turtlesim_node` và kiểm tra `ros2 doctor`:

```bash
ros2 run turtlesim turtlesim_node
```

Tại một terminal khác, chạy:
```bash
ros2 doctor
```
Bạn sẽ thấy cảnh báo:
```text
UserWarning: Publisher without subscriber detected on /turtle1/color_sensor.
UserWarning: Publisher without subscriber detected on /turtle1/pose.
```
> [!NOTE]
> Cảnh báo này cho biết node `/turtlesim` đang phát dữ liệu lên 2 topic trên nhưng chưa có bất kỳ subscriber nào lắng nghe, điều này có thể gây lãng phí tài nguyên tính toán.

Khi bạn mở thêm terminal chạy `ros2 topic echo /turtle1/pose`, cảnh báo trên sẽ tự động biến mất vì topic đã có subscriber hợp lệ!

---

### 3. Xuất Báo cáo chi tiết toàn diện với `--report`
Khi cần nhờ cộng đồng trợ giúp hoặc phân tích lỗi sâu:

```bash
ros2 doctor --report
```

Lệnh này sẽ xuất ra một bản báo cáo đầy đủ chia thành các danh mục:
- **`ROS ENVIRONMENT`**: Biến `ROS_DISTRO`, `ROS_VERSION`, `ROS_DOMAIN_ID`...
- **`NETWORK CONFIGURATION`**: Địa chỉ IP, card mạng, subnet mask, loopback...
- **`RMW MIDDLEWARE`**: Nhà cung cấp DDS đang kích hoạt (Fast DDS, Cyclone DDS, Zenoh...).
- **`PACKAGE VERSIONS`**: Phiên bản chi tiết của các gói phần mềm cài đặt.
- **`TOPIC LIST & SERVICE LIST`**: Danh sách tất cả topic/service đang mở.

---

## 📌 Tóm tắt (Summary)
- `ros2 doctor` là công cụ đầu tiên bạn nên chạy khi gặp các lỗi khó hiểu liên quan đến mạng hoặc kết nối giữa các node.
- Dùng `ros2 doctor --report` để đính kèm thông tin cấu hình khi tạo issue báo lỗi trên GitHub hoặc diễn đàn ROS Discourse.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]]
- ➡️ Bài tiếp theo: [[12 - Creating and Using Plugins (C++)|Tạo và Sử dụng Plugins (C++)]]

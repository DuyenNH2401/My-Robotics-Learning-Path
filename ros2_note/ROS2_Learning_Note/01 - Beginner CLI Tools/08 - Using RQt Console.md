---
tags:
  - ros2
  - rqt
  - rqt_console
  - logging
  - cli
  - beginner
created: 2026-08-25
aliases:
  - Quản lý Log với RQt Console
  - Using rqt_console to view logs
---

# 📋 Quản lý và Kiểm tra Logs với RQt Console (Using rqt_console to view logs)

> [!INFO] **Mục tiêu bài học**
> Làm quen với công cụ giao diện đồ họa **rqt_console** để theo dõi, lọc, và phân tích các thông điệp ghi log (log messages) trong hệ thống ROS 2.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 5 phút
> - **Bài trước:** [[07 - Understanding Actions|Tìm hiểu về Actions trong ROS 2]]
> - **Bài tiếp theo:** [[09 - Launching Nodes|Khởi chạy Nodes với Launch Files]]

---

## 📖 Bối cảnh (Background)

- **Log Messages (Nhật ký hệ thống):** Các [[03 - Understanding Nodes|Node]] trong ROS 2 phát ra các thông điệp log để thông báo về trạng thái hoạt động, sự kiện hoặc cảnh báo lỗi.
- Thông thường log sẽ in trực tiếp ra terminal chạy node. Tuy nhiên, khi hệ thống chạy hàng chục node cùng lúc, việc theo dõi trên từng terminal rất hỗn loạn.
- **`rqt_console`:** Là công cụ GUI tập trung toàn bộ log từ tất cả các node trong mạng ROS 2 (thông qua topic chuẩn `/rosout`), cho phép:
  - Xem log có tổ chức theo thời gian thực.
  - Lọc log theo mức độ nghiêm trọng (Severity levels) hoặc theo tên node.
  - Tìm kiếm và làm nổi bật (highlight) chuỗi ký tự.
  - Lưu và nạp lại file log để điều tra lỗi sau này.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Khởi động `rqt_console` và Turtlesim
Mở hai terminal riêng biệt:

```bash
# Terminal 1: Mở giao diện theo dõi log
ros2 run rqt_console rqt_console

# Terminal 2: Chạy node turtlesim
ros2 run turtlesim turtlesim_node
```

> [!NOTE] **Cấu trúc giao diện RQt Console:**
> - **Khu vực trên:** Hiển thị danh sách các thông điệp log đến từ tất cả các node.
> - **Khu vực giữa:** Bộ lọc loại trừ (Exclusion filters) theo mức nghiêm trọng hoặc tên node.
> - **Khu vực dưới:** Bộ lọc tìm kiếm và đánh dấu (Highlighting filters).

---

### 2. Tạo thông điệp cảnh báo (Warn Log)
Cho rùa chạy liên tục vào tường để Turtlesim kích hoạt cảnh báo va chạm:

```bash
ros2 topic pub -r 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Trên cửa sổ `rqt_console`, bạn sẽ thấy liên tục xuất hiện các dòng log màu vàng ở mức độ **Warn** thông báo rùa chạm vào giới hạn màn hình.

Nhấn `Ctrl + C` ở terminal phát lệnh để dừng lại.

---

## 📊 5 Mức độ nghiêm trọng của Logger (Logger Levels)

ROS 2 phân chia log theo thứ tự độ nghiêm trọng từ cao xuống thấp như sau:

| Mức Log | Tên gọi | Ý nghĩa |
| :---: | :--- | :--- |
| 🔴 **1** | **Fatal** | Hệ thống gặp lỗi chí mạng và buộc phải dừng hoạt động ngay lập tức để bảo vệ phần cứng. |
| 🟠 **2** | **Error** | Gặp lỗi nghiêm trọng khiến một chức năng cụ thể không thể hoạt động bình thường, nhưng node chưa bị crash hoàn toàn. |
| 🟡 **3** | **Warn** | Hoạt động bất thường hoặc kết quả không lý tưởng (ví dụ va chạm mép tường), chưa gây hỏng hóc ngay nhưng cần lưu ý. |
| 🟢 **4** | **Info** | Thông tin cập nhật sự kiện, trạng thái hoạt động bình thường của hệ thống *(Mức hiển thị mặc định)*. |
| 🔵 **5** | **Debug** | Thông tin chi tiết từng bước phục vụ quá trình debug của lập trình viên. |

> [!IMPORTANT]
> **Quy tắc hiển thị mặc định:** Hệ thống chỉ hiển thị log từ mức **Info** trở lên (Info, Warn, Error, Fatal). Các log ở mức **Debug** sẽ bị ẩn để tránh rác màn hình.

---

### 3. Thiết lập mức Log lúc khởi chạy Node
Bạn có thể thay đổi mức log tối thiểu của node bằng cờ `--log-level`:

```bash
ros2 run turtlesim turtlesim_node --ros-args --log-level WARN
```
Với thiết lập này, node `/turtlesim` sẽ chỉ phát ra các log ở mức `WARN`, `ERROR`, và `FATAL`. Toàn bộ log `INFO` thông thường lúc khởi động sẽ bị bỏ qua.

---

## 📌 Tóm tắt (Summary)
- `rqt_console` là công cụ không thể thiếu khi cần gỡ lỗi (debug) hệ thống robot phức tạp gồm nhiều node.
- Hiểu và sử dụng đúng 5 mức **Logger Levels** giúp bạn phân loại và xử lý sự cố nhanh chóng.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[07 - Understanding Actions|Tìm hiểu về Actions trong ROS 2]]
- ➡️ Bài tiếp theo: [[09 - Launching Nodes|Khởi chạy Nodes với Launch Files]]

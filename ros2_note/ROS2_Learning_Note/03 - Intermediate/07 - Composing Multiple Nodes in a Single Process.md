---
tags:
  - ros2
  - composition
  - components
  - component_container
  - multi-threading
  - intermediate
created: 2026-08-25
aliases:
  - Kết hợp nhiều Node trong một Tiến trình
  - Composing multiple nodes in a single process
---

# 🏢 Kết hợp nhiều Node trong một Tiến trình (Composition)

> [!INFO] **Mục tiêu bài học**
> Thực hành các phương pháp kết hợp nhiều [[06 - Writing a Composable Node (C++)|Composable Node]] vào trong một tiến trình duy nhất (**Component Container**) lúc runtime qua CLI, lúc compile-time hoặc tự động hóa qua Launch file.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]
> - **Bài tiếp theo:** [[08 - Using Node Interfaces Template Class (C++)|Sử dụng Node Interfaces Template Class (C++)]]

---

## 📖 Bối cảnh (Background)

ROS 2 hỗ trợ 4 cơ chế Composition:
1. **Run-time Composition (Khuyên dùng):** Khởi động tiến trình container rỗng (`ComponentManager`), sau đó nạp (*load*) hoặc gỡ bỏ (*unload*) các component linh hoạt qua lệnh CLI hoặc Service lúc runtime.
2. **Launch-time Composition:** Khởi chạy container và tự động nạp sẵn danh sách các component thông qua `ComposableNodeContainer` trong Launch file.
3. **Compile-time Composition:** Viết mã C++ gộp cứng nhiều component vào một file `main.cpp` thực thi duy nhất.
4. **dlopen Composition:** Nạp trực tiếp file `.so` qua `dlopen`.

---

## 🛠️ Thực hành Run-time Composition qua CLI (Tasks)

### 1. Khám phá các Component có sẵn
Kiểm tra danh sách các component đã được đăng ký trong hệ thống:

```bash
ros2 component types
```
Kết quả mẫu:
```text
composition
  composition::Talker
  composition::Listener
  composition::Server
  composition::Client
```

---

### 2. Khởi chạy Component Container
Mở terminal 1 và khởi động container quản lý:

```bash
ros2 run rclcpp_components component_container
```

Tại terminal 2, kiểm tra danh sách container đang chạy:
```bash
ros2 component list
# Trả về: /ComponentManager
```

---

### 3. Nạp (Load) Components vào Container
Nạp component `Talker`:
```bash
ros2 component load /ComponentManager composition composition::Talker
# Trả về: Loaded component 1 into '/ComponentManager' container node as '/talker'
```

Nạp tiếp component `Listener`:
```bash
ros2 component load /ComponentManager composition composition::Listener
# Trả về: Loaded component 2 into '/ComponentManager' container node as '/listener'
```

Kiểm tra lại trạng thái container:
```bash
ros2 component list
```
Kết quả:
```text
/ComponentManager
   1  /talker
   2  /listener
```
Lúc này trên terminal 1, hai node `Talker` và `Listener` đang trao đổi dữ liệu trực tiếp trong cùng một vùng nhớ tiến trình!

---

### 4. Gỡ bỏ (Unload) Components
Để dừng và giải phóng component khỏi RAM, sử dụng ID tương ứng:

```bash
ros2 component unload /ComponentManager 1 2
```

---

## ⚙️ Các tùy chọn Nâng cao (Advanced Topics)

### 1. Chọn loại Executor cho Container

| Loại Executor | Lệnh khởi chạy | Mô tả |
| :--- | :--- | :--- |
| **SingleThreaded** | `ros2 run rclcpp_components component_container` | Mặc định, chạy đơn luồng. |
| **MultiThreaded** | `ros2 run rclcpp_components component_container --executor-type multi-threaded -p thread_num:=4` | Sử dụng 4 luồng xử lý song song. |
| **EventsCBG** | `ros2 run rclcpp_components component_container --executor-type events-cbg` | Tối ưu hóa hiệu năng theo nhóm Callback Group. |
| **Isolated** | `ros2 run rclcpp_components component_container --executor-type multi-threaded --isolated` | Mỗi component sở hữu một MultiThreadedExecutor riêng. |

---

### 2. Đổi tên và Namespace cho Component khi nạp
```bash
# Nạp với tên node và namespace tùy chỉnh
ros2 component load /ComponentManager composition composition::Talker \
  --node-name my_talker \
  --node-namespace /robot1
```

---

### 3. Truyền Parameters và Extra Arguments lúc nạp
```bash
ros2 component load /ComponentManager composition composition::Talker \
  -p publish_rate:=10.0 \
  -e use_intra_process_comms:=true \
  -e forward_global_arguments:=false
```

> [!TIP] **Bảng Extra Arguments thường dùng:**
> - `use_intra_process_comms`: Bật giao tiếp Zero-Copy trong bộ nhớ (mặc định: `false`).
> - `enable_rosout`: Bật xuất bản log lên `/rosout` (mặc định: `true`).
> - `use_clock_thread`: Tạo luồng clock riêng biệt cho component (mặc định: `true`).

---

## 📌 Tóm tắt (Summary)
- **Composition** là kiến trúc tiêu chuẩn cho các robot hiệu năng cao trong ROS 2.
- `ros2 component` cung cấp bộ lệnh đầy đủ: `types`, `list`, `load`, `unload` để quản lý vòng đời node linh hoạt trong container.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]
- ➡️ Bài tiếp theo: [[08 - Using Node Interfaces Template Class (C++)|Sử dụng Node Interfaces Template Class (C++)]]

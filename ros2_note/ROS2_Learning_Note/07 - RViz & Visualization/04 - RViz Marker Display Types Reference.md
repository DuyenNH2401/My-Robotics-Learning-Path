---
tags:
  - ros2
  - rviz2
  - markers
  - reference
  - 3d-graphics
  - intermediate
created: 2026-08-25
aliases:
  - Bảng Tra cứu Toàn bộ 12 Loại Marker trong RViz
  - Marker: Display types
---

# 📚 Bảng Tra cứu Toàn bộ 12 Loại Marker trong RViz2 (Marker Reference)

> [!INFO] **Mục tiêu bài học**
> Tài liệu tra cứu toàn diện về cấu trúc bản tin **`visualization_msgs/msg/Marker`**, giải thích chi tiết **12 loại Marker** hỗ trợ trong RViz2, quy tắc hiển thị kích thước (*Scale*), màu sắc theo từng đỉnh (*Per-vertex colors*), nạp file lưới 3D (*Mesh Resources*) và các kỹ thuật tối ưu hóa hiệu năng render hàng loạt (*Batch Rendering*).
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[03 - Sending Points and Lines Markers to RViz (C++)|Vẽ Điểm và Đường thẳng với Marker (C++)]]
> - **Bài tiếp theo:** [[05 - Building a Custom RViz Display Plugin (C++)|Tự Xây dựng Custom RViz Display Plugin (C++)]]

---

## 📋 Bảng Chi tiết 12 Loại Marker Types trong ROS 2

| Hằng số (Enum Value) | Tên loại Marker | Mô tả hình học | Quy ước trường `scale` | Quy ước trường `points` |
| :--- | :--- | :--- | :--- | :--- |
| **`ARROW = 0`** | Mũi tên 3D | Chỉ hướng vectơ hoặc lực | `x`: Độ dài, `y`: Bán kính thân, `z`: Bán kính đầu | Dùng 2 điểm xác định vị trí Gốc và Ngọn |
| **`CUBE = 1`** | Khối lập phương / hộp | Hộp định vị vật thể | `(x, y, z)`: Chiều dài 3 cạnh (mét) | Không dùng |
| **`SPHERE = 2`** | Khối cầu / Ellipsoid | Điểm mốc dạng hình cầu | `(x, y, z)`: Đường kính 3 trục | Không dùng |
| **`CYLINDER = 3`** | Khối trụ tròn / Ellipse | Cột mốc hình trụ đứng | `x, y`: Đường kính đáy, `z`: Chiều cao | Không dùng |
| **`LINE_STRIP = 4`** | Đường gấp khúc | Nối liên tiếp $0 \to 1 \to 2 \to 3$ | `scale.x`: Độ dày nét vẽ | Chứa danh sách các đỉnh cần nối |
| **`LINE_LIST = 5`** | Tập hợp đoạn thẳng rời | Nối từng cặp $0 \to 1, 2 \to 3$ | `scale.x`: Độ dày nét vẽ | Số điểm phải là số chẵn |
| **`CUBE_LIST = 6`** | Danh sách hàng ngàn hộp | Render hàng loạt khối hộp cực nhanh | `(x, y, z)`: Kích thước chung cho mọi hộp | Mỗi điểm trong mảng là tọa độ 1 hộp |
| **`SPHERE_LIST = 7`** | Danh sách hàng ngàn khối cầu | Render hàng loạt khối cầu cực nhanh | `(x, y, z)`: Kích thước chung cho mọi cầu | Mỗi điểm trong mảng là tọa độ 1 cầu |
| **`POINTS = 8`** | Tập hợp điểm rời | Điểm đám mây | `scale.x`: Rộng, `scale.y`: Cao | Mỗi điểm vẽ 1 ô vuông/chấm tròn |
| **`TEXT_VIEW_FACING = 9`** | Chữ viết 3D luôn nhìn vào Camera | Nhãn văn bản thông tin trên đầu robot | `scale.z`: Chiều cao chữ in hoa 'A' | Nội dung chuỗi lưu trong trường `text` |
| **`MESH_RESOURCE = 10`** | File 3D Mesh ngoài (`.dae`, `.stl`) | Hiển thị mô hình xe hơi, người, tòa nhà | `(x, y, z)`: Tỉ lệ co giãn (Scale Factor) | Đường dẫn file lưu trong `mesh_resource` |
| **`TRIANGLE_LIST = 11`** | Mặt lưới tam giác tùy biến | Tự dựng bề mặt 3D phức tạp | `(x, y, z)`: Tỉ lệ co giãn | Cứ 3 điểm liên tiếp tạo thành 1 tam giác |

---

## 🏷️ Giải mã Các Trường Thuộc tính Quan trọng

### 1. `action` (Hành vi của Marker)
- `visualization_msgs::msg::Marker::ADD` (Giá trị `0`): Tạo mới hoặc Cập nhật marker hiện có.
- `visualization_msgs::msg::Marker::DELETE` (Giá trị `2`): Xóa marker có `ns` và `id` tương ứng.
- `visualization_msgs::msg::Marker::DELETEALL` (Giá trị `3`): Xóa sạch toàn bộ marker đang hiển thị trên màn hình.

---

### 2. `frame_locked` (Khóa Tọa độ theo Thời gian Thực)
- Mặc định (`false`): Marker được đặt tại vị trí biến đổi tọa độ ở thời điểm nhận tin và sẽ đứng yên tại đó.
- Đặt `true`: RViz2 sẽ **tự động tính toán lại ma trận TF ở mỗi khung hình**, giúp marker luôn "dính chặt" vào frame chuyển động (ví dụ: nhãn tên gắn trên đầu robot chạy theo robot).

---

### 3. `mesh_resource` & `mesh_use_embedded_materials`
Cho phép nạp các mô hình đồ họa 3D chất lượng cao định dạng COLLADA (`.dae`) hoặc Stereolithography (`.stl`):

```cpp
marker.type = visualization_msgs::msg::Marker::MESH_RESOURCE;
marker.mesh_resource = "package://my_robot_pkg/meshes/car_model.dae";
marker.mesh_use_embedded_materials = true; // Sử dụng vân màu và texture gốc của file 3D
```

---

## ⚡ Bí quyết Tối ưu Hóa Hiệu năng Đồ họa (Performance Tips)

> [!TIP] **Quy tắc Vàng về Hiệu năng (Batching):**
> - **Tránh:** Gửi 10,000 thông điệp `CUBE` riêng lẻ trong một `MarkerArray` $\to$ Gây quá tải CPU và giật lag RViz do phải thực hiện 10,000 lệnh vẽ riêng biệt (*Draw Calls*).
> - **Nên dùng:** Gửi duy nhất **1 thông điệp `CUBE_LIST`** hoặc `SPHERE_LIST` chứa 10,000 điểm tọa độ $\to$ Card đồ họa (GPU) sẽ gom nhóm và vẽ toàn bộ chỉ trong 1 chu kỳ render duy nhất!

---

## 📌 Tóm tắt (Summary)
- `visualization_msgs/msg/Marker` cung cấp bộ 12 công cụ hiển thị 3D hoàn chỉnh.
- Sử dụng `TEXT_VIEW_FACING` để làm chú thích và tận dụng `*_LIST` khi cần render số lượng lớn vật thể.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[03 - Sending Points and Lines Markers to RViz (C++)|Vẽ Điểm và Đường thẳng với Marker (C++)]]
- ➡️ Bài tiếp theo: [[05 - Building a Custom RViz Display Plugin (C++)|Tự Xây dựng Custom RViz Display Plugin (C++)]]

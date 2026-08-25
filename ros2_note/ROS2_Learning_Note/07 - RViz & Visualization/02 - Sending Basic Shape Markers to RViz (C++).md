---
tags:
  - ros2
  - rviz2
  - markers
  - visualization_msgs
  - cpp
  - 3d-shapes
  - intermediate
created: 2026-08-25
aliases:
  - Gửi Marker Hình học Cơ bản lên RViz2 bằng C++
  - Marker: Sending Basic Shapes (C++)
---

# 🔺 Gửi Marker Hình học Cơ bản lên RViz2 bằng C++ (Basic Shape Markers)

> [!INFO] **Mục tiêu bài học**
> Học cách xuất bản các hình khối 3D tùy biến (**`CUBE`**, **`SPHERE`**, **`CYLINDER`**, **`ARROW`**) lên RViz2 bằng thông điệp **`visualization_msgs/msg/Marker`** trong C++, cấu hình màu sắc, độ trong suốt (*Alpha*), kích thước và thời gian tồn tại (*Lifetime*).
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[01 - RViz User Guide and Core Concepts|Hướng dẫn Sử dụng RViz2 Toàn diện]]
> - **Bài tiếp theo:** [[03 - Sending Points and Lines Markers to RViz (C++)|Vẽ Điểm và Đường thẳng với Marker (C++)]]

---

## 📖 Bối cảnh (Background)

Khác với các Display cảm biến thông thường (chỉ hiển thị được dữ liệu theo định dạng cố định của Lidar/Camera), **Marker Display** cho phép lập trình viên tự do vẽ bất kỳ hình khối 3D nào trong không gian mô phỏng (ví dụ: đánh dấu vị trí vật cản cần tránh, vẽ hộp bao quanh người đi bộ, hiển thị mục tiêu định vị).

---

## 🛠️ Triển khai mã nguồn C++ (`basic_shapes.cpp`)

```cpp
#include <chrono>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "visualization_msgs/msg/marker.hpp"

using namespace std::chrono_literals;

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("basic_shapes");
  
  // 1. Publisher xuất bản lên topic 'visualization_marker'
  auto marker_pub = node->create_publisher<visualization_msgs::msg::Marker>(
    "visualization_marker", 1
  );
  rclcpp::Rate loop_rate(1); // Tần số 1 Hz (1 giây đổi hình 1 lần)

  // Bắt đầu với hình hộp CUBE
  uint32_t shape = visualization_msgs::msg::Marker::CUBE;

  while (rclcpp::ok()) {
    visualization_msgs::msg::Marker marker;

    // 2. Thiết lập Header: Frame quy chiếu và Timestamp
    marker.header.frame_id = "my_frame";
    marker.header.stamp = node->get_clock()->now();

    // 3. Namespace và ID tạo định danh độc nhất cho Marker (ns + id)
    marker.ns = "basic_shapes";
    marker.id = 0;

    // 4. Loại hình khối
    marker.type = shape;

    // 5. Hành động: ADD (Tạo mới hoặc Cập nhật)
    marker.action = visualization_msgs::msg::Marker::ADD;

    // 6. Vị trí và Hướng xoay (6-DOF Pose)
    marker.pose.position.x = 0.0;
    marker.pose.position.y = 0.0;
    marker.pose.position.z = 0.0;
    marker.pose.orientation.x = 0.0;
    marker.pose.orientation.y = 0.0;
    marker.pose.orientation.z = 0.0;
    marker.pose.orientation.w = 1.0;

    // 7. Kích thước (Scale 3D): 1.0 mét mỗi cạnh
    marker.scale.x = 1.0;
    marker.scale.y = 1.0;
    marker.scale.z = 1.0;

    // 8. Màu sắc RGBA (Màu xanh lá cây đậm)
    marker.color.r = 0.0f;
    marker.color.g = 1.0f;
    marker.color.b = 0.0f;
    marker.color.a = 1.0f; // BẮT BUỘC: a = 1.0 (đục), nếu a = 0 sẽ bị tàng hình!

    // 9. Thời gian sống (Lifetime): 0 nghĩa là tồn tại mãi mãi cho đến khi bị xóa
    marker.lifetime = rclcpp::Duration::from_nanoseconds(0);

    // Xuất bản Marker
    marker_pub->publish(marker);

    // 10. Chuyển đổi tuần tự giữa 4 loại hình khối
    switch (shape) {
      case visualization_msgs::msg::Marker::CUBE:
        shape = visualization_msgs::msg::Marker::SPHERE;
        break;
      case visualization_msgs::msg::Marker::SPHERE:
        shape = visualization_msgs::msg::Marker::ARROW;
        break;
      case visualization_msgs::msg::Marker::ARROW:
        shape = visualization_msgs::msg::Marker::CYLINDER;
        break;
      case visualization_msgs::msg::Marker::CYLINDER:
        shape = visualization_msgs::msg::Marker::CUBE;
        break;
    }

    loop_rate.sleep();
  }

  rclcpp::shutdown();
  return 0;
}
```

---

## 🚀 Xem Marker trên RViz2

```bash
# Terminal 1: Chạy node phát Marker
ros2 run visualization_marker_tutorials basic_shapes

# Terminal 2: Mở RViz2
ros2 run rviz2 rviz2
```

### Cấu hình trong RViz2:
1. Đặt **Fixed Frame** thành: `my_frame` (khớp với `header.frame_id` trong code).
2. Nhấn nút **Add** ở góc dưới bên trái $\rightarrow$ Chọn **Marker** (lắng nghe topic mặc định `/visualization_marker`).
3. Bạn sẽ thấy tại gốc tọa độ, vật thể tự động chuyển đổi luân phiên mỗi giây một lần giữa: **Khối Hộp $\to$ Khối Cầu $\to$ Mũi Tên $\to$ Khối Trụ**!

---

## 📌 Tóm tắt (Summary)
- Gửi dữ liệu đồ họa qua tin nhắn `visualization_msgs/msg/Marker`.
- Luôn kiểm tra `color.a > 0.0` và cấu hình đúng `header.frame_id` trong RViz2.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[01 - RViz User Guide and Core Concepts|Hướng dẫn Sử dụng RViz2 Toàn diện]]
- ➡️ Bài tiếp theo: [[03 - Sending Points and Lines Markers to RViz (C++)|Vẽ Điểm và Đường thẳng với Marker (C++)]]

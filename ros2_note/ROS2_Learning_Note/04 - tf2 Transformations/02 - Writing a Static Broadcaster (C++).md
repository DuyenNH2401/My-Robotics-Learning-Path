---
tags:
  - ros2
  - tf2
  - transformations
  - static-broadcaster
  - cpp
  - rclcpp
  - intermediate
created: 2026-08-25
aliases:
  - Viết Static Broadcaster bằng C++
  - Writing a static broadcaster (C++)
---

# 📍 Viết Static Broadcaster bằng C++ (tf2_ros)

> [!INFO] **Mục tiêu bài học**
> Xây dựng một node C++ sử dụng lớp `tf2_ros::StaticTransformBroadcaster` và `tf2::Quaternion` để phát biến đổi tọa độ tĩnh (**Static Transform**) lên cây `tf2`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài song song (Python):** [[01 - Introduction to tf2 and Static Broadcaster (Python)|Viết Static Broadcaster bằng Python]]
> - **Bài tiếp theo:** [[04 - Writing a Dynamic Broadcaster (C++)|Viết Dynamic Broadcaster bằng C++]]

---

## 📖 Bối cảnh (Background)

Trong C++, thư viện `tf2` cung cấp lớp hỗ trợ toán học `tf2::Quaternion` để tính toán góc quay thuận tiện với phương thức `setRPY(roll, pitch, yaw)`, và `tf2_ros::StaticTransformBroadcaster` để gửi thông điệp `geometry_msgs::msg::TransformStamped` vào cây biến đổi tọa độ.

---

## 🛠️ Triển khai mã nguồn C++ (Tasks)

### 1. Tạo Package `learning_tf2_cpp`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies geometry_msgs rclcpp tf2 tf2_ros turtlesim learning_tf2_cpp
```

---

### 2. Viết Node C++ (`src/static_turtle_tf2_broadcaster.cpp`)

```cpp
#include <memory>
#include <cstring>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
#include "tf2_ros/static_transform_broadcaster.h"

class StaticFramePublisher : public rclcpp::Node
{
public:
  explicit StaticFramePublisher(char * transformation[])
  : Node("static_turtle_tf2_broadcaster")
  {
    // 1. Khởi tạo StaticTransformBroadcaster
    tf_static_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    // 2. Xuất bản Static Transform một lần duy nhất
    this->make_transforms(transformation);
  }

private:
  void make_transforms(char * transformation[])
  {
    geometry_msgs::msg::TransformStamped t;

    // Header metadata
    t.header.stamp = this->get_clock()->now();
    t.header.frame_id = "world";          // Frame gốc (Parent)
    t.child_frame_id = transformation[1];  // Frame con (Child)

    // Tịnh tiến (Translation 3D)
    t.transform.translation.x = atof(transformation[2]);
    t.transform.translation.y = atof(transformation[3]);
    t.transform.translation.z = atof(transformation[4]);

    // Góc quay (Rotation qua Quaternion)
    tf2::Quaternion q;
    q.setRPY(
      atof(transformation[5]),
      atof(transformation[6]),
      atof(transformation[7])
    );
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    // Phát Transform
    tf_static_broadcaster_->sendTransform(t);
  }

  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_static_broadcaster_;
};

int main(int argc, char * argv[])
{
  auto logger = rclcpp::get_logger("logger");

  if (argc != 8) {
    RCLCPP_INFO(
      logger, "Số lượng tham số không hợp lệ!\nCách dùng: "
      "$ ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster "
      "child_frame_name x y z roll pitch yaw");
    return 1;
  }

  if (strcmp(argv[1], "world") == 0) {
    RCLCPP_INFO(logger, "Tên frame con không thể trùng với 'world'");
    return 1;
  }

  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<StaticFramePublisher>(argv));
  rclcpp::shutdown();
  return 0;
}
```

---

### 3. Cấu hình `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.20)
project(learning_tf2_cpp)

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(turtlesim REQUIRED)

add_executable(static_turtle_tf2_broadcaster src/static_turtle_tf2_broadcaster.cpp)
target_link_libraries(static_turtle_tf2_broadcaster PUBLIC
   geometry_msgs::geometry_msgs
   rclcpp::rclcpp
   tf2::tf2
   tf2_ros::tf2_ros
)

install(TARGETS
   static_turtle_tf2_broadcaster
   DESTINATION lib/${PROJECT_NAME})

ament_package()
```

---

### 4. Biên dịch và Kiểm tra

```bash
cd ~/ros2_ws
colcon build --packages-select learning_tf2_cpp
source install/setup.bash

# Khởi chạy node phát frame 'mystaticturtle'
ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster mystaticturtle 0 0 1 0 0 0
```

Kiểm tra kết quả với `ros2 topic echo /tf_static`:
```yaml
transforms:
- header:
    stamp:
      sec: ...
    frame_id: world
  child_frame_id: mystaticturtle
  transform:
    translation:
      x: 0.0
      y: 0.0
      z: 1.0
    rotation:
      x: 0.0
      y: 0.0
      z: 0.0
      w: 1.0
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng `tf2::Quaternion::setRPY` giúp chuyển đổi dễ dàng từ góc trực quan Roll-Pitch-Yaw sang Quaternion $(x, y, z, w)$.
- `StaticTransformBroadcaster` gửi thông tin tĩnh vào `/tf_static` để tái sử dụng xuyên suốt toàn hệ thống.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[01 - Introduction to tf2 and Static Broadcaster (Python)|Viết Static Broadcaster bằng Python]]
- ➡️ Bài tiếp theo: [[04 - Writing a Dynamic Broadcaster (C++)|Viết Dynamic Broadcaster bằng C++]]

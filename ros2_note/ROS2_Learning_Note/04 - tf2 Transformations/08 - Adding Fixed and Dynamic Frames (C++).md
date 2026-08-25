---
tags:
  - ros2
  - tf2
  - coordinate-frames
  - tf-tree
  - cpp
  - rclcpp
  - intermediate
created: 2026-08-25
aliases:
  - Thêm Khung tọa độ Tĩnh và Động bằng C++
  - Adding a frame (C++)
---

# 🌳 Thêm Khung tọa độ Tĩnh và Động bằng C++ (Adding Frames to tf2)

> [!INFO] **Mục tiêu bài học**
> Xây dựng các node C++ mở rộng cây `tf2 Tree`: tạo khung tọa độ cố định tương đối (**Fixed Frame**) và khung tọa độ chuyển động tuần hoàn (**Dynamic Frame**) cho củ cà rốt `carrot1`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[06 - Writing a Listener (C++)|Viết tf2 Listener bằng C++]]
> - **Bài song song (Python):** [[07 - Adding Fixed and Dynamic Frames (Python)|Thêm Khung tọa độ Tĩnh và Động (Python)]]
> - **Bài tiếp theo:** [[09 - Using Time and Timeouts in tf2 (C++)|Sử dụng Thời gian và Timeout trong tf2 (C++)]]

---

## 🛠️ Phần 1: Viết Fixed Frame Broadcaster C++

Tạo file `src/fixed_frame_tf2_broadcaster.cpp`:

```cpp
#include <chrono>
#include <memory>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"

using namespace std::chrono_literals;

class FixedFrameBroadcaster : public rclcpp::Node
{
public:
  FixedFrameBroadcaster()
  : Node("fixed_frame_tf2_broadcaster")
  {
    tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

    auto broadcast_timer_callback = [this]() {
      geometry_msgs::msg::TransformStamped t;

      t.header.stamp = this->get_clock()->now();
      t.header.frame_id = "turtle1";
      t.child_frame_id = "carrot1";

      // Cố định offset y = 2 mét so với turtle1
      t.transform.translation.x = 0.0;
      t.transform.translation.y = 2.0;
      t.transform.translation.z = 0.0;

      t.transform.rotation.x = 0.0;
      t.transform.rotation.y = 0.0;
      t.transform.rotation.z = 0.0;
      t.transform.rotation.w = 1.0;

      tf_broadcaster_->sendTransform(t);
    };

    timer_ = this->create_wall_timer(100ms, broadcast_timer_callback);
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FixedFrameBroadcaster>());
  rclcpp::shutdown();
  return 0;
}
```

---

## 🛠️ Phần 2: Viết Dynamic Frame Broadcaster C++

Tạo file `src/dynamic_frame_tf2_broadcaster.cpp`:

```cpp
#include <chrono>
#include <cmath>
#include <memory>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"

using namespace std::chrono_literals;

const double PI = 3.141592653589793238463;

class DynamicFrameBroadcaster : public rclcpp::Node
{
public:
  DynamicFrameBroadcaster()
  : Node("dynamic_frame_tf2_broadcaster")
  {
    tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

    auto broadcast_timer_callback = [this]() {
      rclcpp::Time now = this->get_clock()->now();
      double x = now.seconds() * PI;

      geometry_msgs::msg::TransformStamped t;
      t.header.stamp = now;
      t.header.frame_id = "turtle1";
      t.child_frame_id = "carrot1";

      // Vị trí biến thiên liên tục theo quỹ đạo tròn
      t.transform.translation.x = 10.0 * sin(x);
      t.transform.translation.y = 10.0 * cos(x);
      t.transform.translation.z = 0.0;

      t.transform.rotation.x = 0.0;
      t.transform.rotation.y = 0.0;
      t.transform.rotation.z = 0.0;
      t.transform.rotation.w = 1.0;

      tf_broadcaster_->sendTransform(t);
    };

    timer_ = this->create_wall_timer(100ms, broadcast_timer_callback);
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<DynamicFrameBroadcaster>());
  rclcpp::shutdown();
  return 0;
}
```

---

### Cập nhật `CMakeLists.txt`:
```cmake
add_executable(fixed_frame_tf2_broadcaster src/fixed_frame_tf2_broadcaster.cpp)
target_link_libraries(fixed_frame_tf2_broadcaster PUBLIC
  geometry_msgs::geometry_msgs rclcpp::rclcpp tf2_ros::tf2_ros)

add_executable(dynamic_frame_tf2_broadcaster src/dynamic_frame_tf2_broadcaster.cpp)
target_link_libraries(dynamic_frame_tf2_broadcaster PUBLIC
  geometry_msgs::geometry_msgs rclcpp::rclcpp tf2_ros::tf2_ros)

install(TARGETS
  fixed_frame_tf2_broadcaster
  dynamic_frame_tf2_broadcaster
  DESTINATION lib/${PROJECT_NAME})
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng `TransformBroadcaster` định kỳ phát thông điệp với `child_frame_id` mong muốn để mở rộng cây tf2.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[06 - Writing a Listener (C++)|Viết tf2 Listener bằng C++]]
- ➡️ Bài tiếp theo: [[09 - Using Time and Timeouts in tf2 (C++)|Sử dụng Thời gian và Timeout trong tf2 (C++)]]

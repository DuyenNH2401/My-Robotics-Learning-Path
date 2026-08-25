---
tags:
  - ros2
  - tf2
  - dynamic-broadcaster
  - cpp
  - rclcpp
  - intermediate
created: 2026-08-25
aliases:
  - Viết Dynamic Broadcaster bằng C++
  - Writing a broadcaster (C++)
---

# 🚗 Viết Dynamic Broadcaster bằng C++ (tf2_ros::TransformBroadcaster)

> [!INFO] **Mục tiêu bài học**
> Xây dựng node C++ sử dụng `tf2_ros::TransformBroadcaster` để liên tục xuất bản trạng thái chuyển động của robot lên cây `tf2` theo thời gian thực.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[02 - Writing a Static Broadcaster (C++)|Viết Static Broadcaster bằng C++]]
> - **Bài song song (Python):** [[03 - Writing a Dynamic Broadcaster (Python)|Viết Dynamic Broadcaster bằng Python]]
> - **Bài tiếp theo:** [[06 - Writing a Listener (C++)|Viết tf2 Listener bằng C++]]

---

## 📖 Bối cảnh (Background)

Trong C++, lớp `tf2_ros::TransformBroadcaster` quản lý việc gửi các thông điệp `geometry_msgs::msg::TransformStamped` lên topic `/tf`. Khi nhận dữ liệu cảm biến hoặc từ bộ ước lượng odometry, node sẽ cập nhật dấu thời gian hiện tại (`this->get_clock()->now()`) và phát thông tin vị trí không gian 3D.

---

## 🛠️ Triển khai mã nguồn C++ (Tasks)

### 1. Viết Node C++ (`src/turtle_tf2_broadcaster.cpp`)

```cpp
#include <functional>
#include <memory>
#include <sstream>
#include <string>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "turtlesim_msgs/msg/pose.hpp"

class FramePublisher : public rclcpp::Node
{
public:
  FramePublisher()
  : Node("turtle_tf2_frame_publisher")
  {
    // 1. Khai báo parameter nhận tên chú rùa
    turtlename_ = this->declare_parameter<std::string>("turtlename", "turtle");

    // 2. Khởi tạo TransformBroadcaster
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    // 3. Đăng ký nhận dữ liệu từ topic /<turtlename>/pose
    std::ostringstream stream;
    stream << "/" << turtlename_.c_str() << "/pose";
    std::string topic_name = stream.str();

    auto handle_turtle_pose = [this](const std::shared_ptr<const turtlesim_msgs::msg::Pose> msg) {
      geometry_msgs::msg::TransformStamped t;

      // Metadata
      t.header.stamp = this->get_clock()->now();
      t.header.frame_id = "world";
      t.child_frame_id = turtlename_.c_str();

      // Vị trí (Translation 2D)
      t.transform.translation.x = msg->x;
      t.transform.translation.y = msg->y;
      t.transform.translation.z = 0.0;

      // Góc quay (Rotation Z)
      tf2::Quaternion q;
      q.setRPY(0.0, 0.0, msg->theta);
      t.transform.rotation.x = q.x();
      t.transform.rotation.y = q.y();
      t.transform.rotation.z = q.z();
      t.transform.rotation.w = q.w();

      // Gửi Transform động
      tf_broadcaster_->sendTransform(t);
    };

    subscription_ = this->create_subscription<turtlesim_msgs::msg::Pose>(
      topic_name, 10, handle_turtle_pose);
  }

private:
  rclcpp::Subscription<turtlesim_msgs::msg::Pose>::SharedPtr subscription_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  std::string turtlename_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FramePublisher>());
  rclcpp::shutdown();
  return 0;
}
```

---

### 2. Cấu hình `CMakeLists.txt`

```cmake
find_package(turtlesim_msgs REQUIRED)

add_executable(turtle_tf2_broadcaster src/turtle_tf2_broadcaster.cpp)
target_link_libraries(
    turtle_tf2_broadcaster PUBLIC
    geometry_msgs::geometry_msgs
    rclcpp::rclcpp
    tf2::tf2
    tf2_ros::tf2_ros
    turtlesim_msgs::turtlesim_msgs
)

install(TARGETS
    turtle_tf2_broadcaster
    DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})
```

---

### 3. Viết Launch File (`launch/turtle_tf2_demo_launch.py`)

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),
        Node(
            package='learning_tf2_cpp',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[
                {'turtlename': 'turtle1'}
            ]
        ),
    ])
```

---

### 4. Biên dịch và Chạy thử nghiệm

```bash
cd ~/ros2_ws
colcon build --packages-select learning_tf2_cpp
source install/setup.bash

# Khởi chạy hệ thống
ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.py
```

Kiểm tra bằng lệnh echo trong terminal riêng:
```bash
ros2 run tf2_ros tf2_echo world turtle1
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng `tf2_ros::TransformBroadcaster` truyền vào `*this` để phát bản tin `TransformStamped` liên tục mỗi khi nhận được dữ liệu odometry/pose mới.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[02 - Writing a Static Broadcaster (C++)|Viết Static Broadcaster bằng C++]]
- 🐍 Phiên bản Python: [[03 - Writing a Dynamic Broadcaster (Python)|Viết Dynamic Broadcaster bằng Python]]
- ➡️ Bài tiếp theo: [[06 - Writing a Listener (C++)|Viết tf2 Listener bằng C++]]

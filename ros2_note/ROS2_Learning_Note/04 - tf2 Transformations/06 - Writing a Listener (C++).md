---
tags:
  - ros2
  - tf2
  - listener
  - lookup-transform
  - cpp
  - rclcpp
  - intermediate
created: 2026-08-25
aliases:
  - Viết tf2 Listener bằng C++
  - Writing a listener (C++)
---

# 👂 Viết tf2 Listener bằng C++ (tf2_ros::TransformListener)

> [!INFO] **Mục tiêu bài học**
> Xây dựng một node C++ sử dụng `tf2_ros::Buffer` và `tf2_ros::TransformListener` để truy vấn biến đổi không gian (`lookupTransform`), xử lý ngoại lệ `tf2::TransformException` và điều khiển bám đuôi giữa các robot.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[04 - Writing a Dynamic Broadcaster (C++)|Viết Dynamic Broadcaster bằng C++]]
> - **Bài song song (Python):** [[05 - Writing a Listener (Python)|Viết tf2 Listener bằng Python]]
> - **Bài tiếp theo:** [[08 - Adding Fixed and Dynamic Frames (C++)|Thêm Khung tọa độ Tĩnh và Động (C++)]]

---

## 📖 Bối cảnh (Background)

Trong C++, đối tượng `tf2_ros::Buffer` nhận xung nhịp đồng hồ `this->get_clock()` để quản lý bộ đệm thời gian. Khi khởi tạo `tf2_ros::TransformListener`, bạn nên truyền kèm con trỏ `this` của node (hoặc `NodeInterfaces`) để đảm bảo listener kế thừa chính xác cấu hình namespace và remapping topic của node.

---

## 🛠️ Triển khai mã nguồn C++ (Tasks)

### 1. Viết Node C++ (`src/turtle_tf2_listener.cpp`)

```cpp
#include <chrono>
#include <cmath>
#include <functional>
#include <memory>
#include <string>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/exceptions.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "turtlesim_msgs/srv/spawn.hpp"

using namespace std::chrono_literals;

class FrameListener : public rclcpp::Node
{
public:
  FrameListener()
  : Node("turtle_tf2_frame_listener"),
    turtle_spawning_service_ready_(false),
    turtle_spawned_(false)
  {
    // 1. Khai báo parameter frame mục tiêu
    target_frame_ = this->declare_parameter<std::string>("target_frame", "turtle1");

    // 2. Khởi tạo Buffer và TransformListener
    tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
    // Truyền 'this' để listener gắn liền với lifecycle và namespace của node này
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_, this);

    // 3. Client gọi Service spawn turtle2
    spawner_ = this->create_client<turtlesim_msgs::srv::Spawn>("spawn");

    // 4. Publisher điều khiển vận tốc cho turtle2
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("turtle2/cmd_vel", 1);

    // 5. Timer chu kỳ 100ms tính toán điều khiển
    timer_ = this->create_wall_timer(
      100ms, [this]() { return this->on_timer(); });
  }

private:
  void on_timer()
  {
    std::string fromFrameRel = target_frame_.c_str(); // "turtle1"
    std::string toFrameRel = "turtle2";               // "turtle2"

    if (turtle_spawning_service_ready_) {
      if (turtle_spawned_) {
        geometry_msgs::msg::TransformStamped t;

        // Tra cứu ma trận biến đổi tọa độ mới nhất (TimePointZero)
        try {
          t = tf_buffer_->lookupTransform(
            toFrameRel,
            fromFrameRel,
            tf2::TimePointZero
          );
        } catch (const tf2::TransformException & ex) {
          RCLCPP_INFO(
            this->get_logger(), "Chưa thể transform %s sang %s: %s",
            toFrameRel.c_str(), fromFrameRel.c_str(), ex.what());
          return;
        }

        // Tính toán vận tốc bám đuổi
        geometry_msgs::msg::Twist msg;

        static const double scaleRotationRate = 1.0;
        msg.angular.z = scaleRotationRate * atan2(
          t.transform.translation.y,
          t.transform.translation.x);

        static const double scaleForwardSpeed = 0.5;
        msg.linear.x = scaleForwardSpeed * sqrt(
          pow(t.transform.translation.x, 2) +
          pow(t.transform.translation.y, 2));

        publisher_->publish(msg);
      } else {
        RCLCPP_INFO(this->get_logger(), "Đã spawn turtle2 thành công!");
        turtle_spawned_ = true;
      }
    } else {
      if (spawner_->service_is_ready()) {
        auto request = std::make_shared<turtlesim_msgs::srv::Spawn::Request>();
        request->x = 4.0;
        request->y = 2.0;
        request->theta = 0.0;
        request->name = "turtle2";

        using ServiceResponseFuture = rclcpp::Client<turtlesim_msgs::srv::Spawn>::SharedFuture;
        auto response_received_callback = [this](ServiceResponseFuture future) {
          auto result = future.get();
          if (result->name == "turtle2") {
            turtle_spawning_service_ready_ = true;
          }
        };
        spawner_->async_send_request(request, response_received_callback);
      }
    }
  }

  bool turtle_spawning_service_ready_;
  bool turtle_spawned_;
  rclcpp::Client<turtlesim_msgs::srv::Spawn>::SharedPtr spawner_{nullptr};
  rclcpp::TimerBase::SharedPtr timer_{nullptr};
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_{nullptr};
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
  std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
  std::string target_frame_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<FrameListener>());
  rclcpp::shutdown();
  return 0;
}
```

---

### 2. Cấu hình `CMakeLists.txt`

```cmake
add_executable(turtle_tf2_listener src/turtle_tf2_listener.cpp)
target_link_libraries(
    turtle_tf2_listener PUBLIC
    geometry_msgs::geometry_msgs
    rclcpp::rclcpp
    tf2::tf2
    tf2_ros::tf2_ros
    turtlesim_msgs::turtlesim_msgs
)

install(TARGETS
    turtle_tf2_listener
    DESTINATION lib/${PROJECT_NAME})
```

---

### 3. Cập nhật Launch File (`launch/turtle_tf2_demo_launch.py`)

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(
            package='learning_tf2_cpp',
            executable='turtle_tf2_broadcaster',
            name='broadcaster1',
            parameters=[{'turtlename': 'turtle1'}]
        ),
        DeclareLaunchArgument('target_frame', default_value='turtle1'),
        Node(
            package='learning_tf2_cpp',
            executable='turtle_tf2_broadcaster',
            name='broadcaster2',
            parameters=[{'turtlename': 'turtle2'}]
        ),
        Node(
            package='learning_tf2_cpp',
            executable='turtle_tf2_listener',
            name='listener',
            parameters=[{'target_frame': LaunchConfiguration('target_frame')}]
        ),
    ])
```

---

### 4. Biên dịch và Chạy thử nghiệm

```bash
cd ~/ros2_ws
colcon build --packages-select learning_tf2_cpp
source install/setup.bash

# Chạy hệ thống
ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.py
```

---

## 📌 Tóm tắt (Summary)
- `tf2_ros::Buffer::lookupTransform(target, source, tf2::TimePointZero)` là hàm cốt lõi để lấy biến đổi tọa độ mới nhất trong C++.
- Luôn bọc lệnh trong khối `try - catch (const tf2::TransformException & ex)` để tránh crash node khi dữ liệu frame chưa kịp đến.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[04 - Writing a Dynamic Broadcaster (C++)|Viết Dynamic Broadcaster bằng C++]]
- 🐍 Phiên bản Python: [[05 - Writing a Listener (Python)|Viết tf2 Listener bằng Python]]
- ➡️ Bài tiếp theo: [[08 - Adding Fixed and Dynamic Frames (C++)|Thêm Khung tọa độ Tĩnh và Động (C++)]]

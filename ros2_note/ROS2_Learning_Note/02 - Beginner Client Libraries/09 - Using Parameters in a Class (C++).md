---
tags:
  - ros2
  - cpp
  - rclcpp
  - parameters
  - launch
  - beginner
created: 2026-08-25
aliases:
  - Sử dụng Parameters trong Class (C++)
  - Using parameters in a class (C++)
---

# ⚙️ Sử dụng Parameters trong Class C++ (rclcpp)

> [!INFO] **Mục tiêu bài học**
> Học cách khai báo (declare), truy xuất (get), thiết lập (set) các [[06 - Understanding Parameters|Parameters]] ngay trong class C++ (`rclcpp::Node`) và cấu hình chúng thông qua Launch File hoặc dòng lệnh CLI.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[08 - Creating Custom Interfaces (msg and srv)|Tạo Message và Service tùy chỉnh]]
> - **Bài song song (Python):** [[10 - Using Parameters in a Class (Python)|Sử dụng Parameters trong Class (Python)]]
> - **Bài tiếp theo:** [[11 - Using ROS2 Doctor|Kiểm tra hệ thống với ros2doctor]]

---

## 📖 Bối cảnh (Background)

Trong ROS 2, mọi parameter trước khi được đọc hoặc ghi đều **bắt buộc phải được khai báo (declared)** trong node. Điều này giúp kiểm soát kiểu dữ liệu và mô tả thông số rõ ràng.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package `cpp_parameters`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_parameters --dependencies rclcpp
```

---

### 2. Viết Node C++ quản lý Parameter (`src/cpp_parameters_node.cpp`)

```cpp
#include <chrono>
#include <functional>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class MinimalParam : public rclcpp::Node
{
public:
  MinimalParam()
  : Node("minimal_param_node")
  {
    // 1. Khai báo parameter với tên "my_parameter" và giá trị mặc định là "world"
    this->declare_parameter("my_parameter", "world");

    // 2. Timer đọc và in giá trị parameter mỗi 1 giây
    auto timer_callback = [this]() {
      std::string my_param = this->get_parameter("my_parameter").as_string();

      RCLCPP_INFO(this->get_logger(), "Hello %s!", my_param.c_str());

      // Tùy chọn: Đặt lại giá trị nếu cần
      std::vector<rclcpp::Parameter> all_new_parameters{
        rclcpp::Parameter("my_parameter", "world")
      };
      this->set_parameters(all_new_parameters);
    };
    
    timer_ = this->create_wall_timer(1000ms, timer_callback);
  }

private:
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalParam>());
  rclcpp::shutdown();
  return 0;
}
```

> [!TIP] **Thêm mô tả cho Parameter với `ParameterDescriptor`:**
> ```cpp
> auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
> param_desc.description = "Thong so mo ta ten dinh kem";
> this->declare_parameter("my_parameter", "world", param_desc);
> ```
> Khi đó, lệnh `ros2 param describe /minimal_param_node my_parameter` sẽ in ra thông tin mô tả này.

---

### 3. Cấu hình `CMakeLists.txt`
```cmake
cmake_minimum_required(VERSION 3.20)
project(cpp_parameters)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(minimal_param_node src/cpp_parameters_node.cpp)
target_link_libraries(minimal_param_node rclcpp::rclcpp)

# Cài đặt executable và thư mục launch (nếu có)
install(TARGETS
  minimal_param_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
```

---

### 4. Thiết lập Parameter qua Launch File
Tạo file `launch/cpp_parameters_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cpp_parameters',
            executable='minimal_param_node',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'my_parameter': 'earth'}  # Nạp giá trị mới "earth"
            ]
        )
    ])
```

---

### 5. 4 Cách thay đổi Parameter linh hoạt

1. **Thay đổi từ Terminal lúc đang chạy:**
   ```bash
   ros2 param set /minimal_param_node my_parameter universe
   ```

2. **Truyền trực tiếp qua Launch File:**
   ```bash
   ros2 launch cpp_parameters cpp_parameters_launch.py
   ```

3. **Nạp file YAML từ Launch File:**
   ```python
   parameters=['path/to/params.yaml']
   ```

4. **Truyền file YAML qua lệnh `ros2 run`:**
   ```bash
   ros2 run cpp_parameters minimal_param_node --ros-args --params-file params.yaml
   ```

---

## 📌 Tóm tắt (Summary)
- Trong `rclcpp`, sử dụng `this->declare_parameter()`, `this->get_parameter()`, và `this->set_parameters()`.
- Kết hợp launch file giúp dễ dàng chuyển đổi cấu hình giữa các môi trường mô phỏng và thực tế.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[08 - Creating Custom Interfaces (msg and srv)|Tạo Message và Service tùy chỉnh]]
- 🐍 Phiên bản Python: [[10 - Using Parameters in a Class (Python)|Sử dụng Parameters trong Class (Python)]]
- ➡️ Bài tiếp theo: [[11 - Using ROS2 Doctor|Kiểm tra hệ thống với ros2doctor]]

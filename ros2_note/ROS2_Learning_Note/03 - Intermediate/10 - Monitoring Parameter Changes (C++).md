---
tags:
  - ros2
  - cpp
  - rclcpp
  - parameters
  - parameter-event-handler
  - intermediate
created: 2026-08-25
aliases:
  - Theo dõi thay đổi Parameter trong C++
  - Monitoring for parameter changes (C++)
---

# 📡 Theo dõi thay đổi Parameter trong C++ (rclcpp::ParameterEventHandler)

> [!INFO] **Mục tiêu bài học**
> Sử dụng lớp tiện ích **`rclcpp::ParameterEventHandler`** trong C++ để lắng nghe và phản hồi tức thời khi một [[06 - Understanding Parameters|Parameter]] bị thay đổi (của chính node đó hoặc từ một node khác trên mạng).
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]
> - **Bài song song (Python):** [[11 - Monitoring Parameter Changes (Python)|Theo dõi thay đổi Parameter (Python)]]
> - **Bài tiếp theo:** [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]

---

## 📖 Bối cảnh (Background)

Trong các ứng dụng điều khiển robot (như bám quỹ đạo, điều khiển động cơ, thuật toán tránh vật cản), thuật toán cần cập nhật ngay các hệ số $K_p, K_i, K_d$ hoặc ngưỡng an toàn ngay khi người vận hành thay đổi thông số qua giao diện hoặc terminal mà không cần khởi động lại node.

Lớp **`rclcpp::ParameterEventHandler`** cung cấp giải pháp đăng ký callback theo dõi sự kiện thay đổi parameter cực kỳ đơn giản và hiệu quả.

---

## 🛠️ Triển khai mã nguồn C++ (Tasks)

### 1. Tạo Package `cpp_parameter_event_handler`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_parameter_event_handler --dependencies rclcpp
```

---

### 2. Viết Node C++ (`src/parameter_event_handler.cpp`)

```cpp
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"

class SampleNodeWithParameters : public rclcpp::Node
{
public:
  SampleNodeWithParameters()
  : Node("node_with_parameters")
  {
    // 1. Khai báo parameter của node
    this->declare_parameter("an_int_param", 0);

    // 2. Khởi tạo ParameterEventHandler
    param_subscriber_ = std::make_shared<rclcpp::ParameterEventHandler>(this);

    // 3. Callback theo dõi parameter của chính node này
    auto cb = [this](const rclcpp::Parameter & p) {
      RCLCPP_INFO(
        this->get_logger(), "Callback cuc bo: Parameter '%s' vua doi gia tri thanh: %ld",
        p.get_name().c_str(),
        p.as_int()
      );
    };
    
    // Đăng ký callback và BẮT BUỘC lưu lại handle
    cb_handle_ = param_subscriber_->add_parameter_callback("an_int_param", cb);

    // 4. Theo dõi parameter từ một Node từ xa (Remote Node: 'parameter_blackboard')
    auto cb_remote = [this](const rclcpp::Parameter & p) {
      RCLCPP_INFO(
        this->get_logger(), "Callback tu xa: Node ngoai '%s' vua doi param '%s' thanh: %.2f",
        "parameter_blackboard",
        p.get_name().c_str(),
        p.as_double()
      );
    };
    cb_remote_handle_ = param_subscriber_->add_parameter_callback(
      "a_double_param", cb_remote, "parameter_blackboard"
    );

    // 5. Theo dõi TẤT CẢ sự kiện Parameter trên toàn hệ thống
    auto event_cb = [this](const rcl_interfaces::msg::ParameterEvent & event) {
      RCLCPP_INFO(this->get_logger(), "Phat hien su kien param tu Node: '%s'", event.node.c_str());
    };
    event_cb_handle_ = param_subscriber_->add_parameter_event_callback(event_cb);
  }

private:
  std::shared_ptr<rclcpp::ParameterEventHandler> param_subscriber_;
  
  // Bắt buộc phải lưu trữ các handle này làm biến thành viên (member variables)
  // Nếu handle bị hủy (destruct), callback sẽ lập tức ngừng hoạt động!
  std::shared_ptr<rclcpp::ParameterCallbackHandle> cb_handle_;
  std::shared_ptr<rclcpp::ParameterCallbackHandle> cb_remote_handle_;
  std::shared_ptr<rclcpp::ParameterEventCallbackHandle> event_cb_handle_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SampleNodeWithParameters>());
  rclcpp::shutdown();
  return 0;
}
```

> [!IMPORTANT] **Lưu ý sống còn về Callback Handle:**
> Phương thức `add_parameter_callback` trả về một con trỏ handle `rclcpp::ParameterCallbackHandle`. Bạn **bắt buộc phải lưu biến này trong class**. Nếu không lưu, handle sẽ bị hủy ngay khi kết thúc constructor và callback sẽ không bao giờ được kích hoạt!

---

### 3. Cấu hình `CMakeLists.txt`
```cmake
add_executable(parameter_event_handler src/parameter_event_handler.cpp)
target_link_libraries(parameter_event_handler PUBLIC rclcpp::rclcpp)

install(TARGETS parameter_event_handler DESTINATION lib/${PROJECT_NAME})
```

---

### 4. Biên dịch và Kiểm tra thực tế

```bash
cd ~/ros2_ws
colcon build --packages-select cpp_parameter_event_handler
source install/setup.bash

# Terminal 1: Chạy Node
ros2 run cpp_parameter_event_handler parameter_event_handler
```

Mở terminal 2 và thay đổi parameter:
```bash
ros2 param set node_with_parameters an_int_param 43
```
Terminal 1 sẽ lập tức in ra dòng log:
`[node_with_parameters]: Callback cuc bo: Parameter 'an_int_param' vua doi gia tri thanh: 43`.

---

## 📌 Tóm tắt (Summary)
- `rclcpp::ParameterEventHandler` là giải pháp chính quy và an toàn để lắng nghe các sự kiện thay đổi tham số trong ROS 2.
- Hỗ trợ giám sát tham số nội bộ, tham số từ xa của node khác, hoặc toàn bộ sự kiện thông qua `ParameterEvent`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]
- 🐍 Phiên bản Python: [[11 - Monitoring Parameter Changes (Python)|Theo dõi thay đổi Parameter (Python)]]
- ➡️ Bài tiếp theo: [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]

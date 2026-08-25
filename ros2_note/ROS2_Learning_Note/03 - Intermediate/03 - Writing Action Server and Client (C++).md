---
tags:
  - ros2
  - cpp
  - rclcpp
  - rclcpp_action
  - action-server
  - action-client
  - intermediate
created: 2026-08-25
aliases:
  - Viết Action Server và Client bằng C++
  - Writing an action server and client (C++)
---

# 🎯 Viết Action Server và Client bằng C++ (rclcpp_action)

> [!INFO] **Mục tiêu bài học**
> Xây dựng hoàn chỉnh cặp **Action Server** và **Action Client** bằng C++ sử dụng thư viện `rclcpp_action`, xử lý Goal, gửi Feedback định kỳ, bắt sự kiện Cancel và nhận Result tính dãy Fibonacci.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[02 - Creating Custom Actions|Tạo Action tùy chỉnh]]
> - **Bài song song (Python):** [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]
> - **Bài tiếp theo:** [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]

---

## 📖 Bối cảnh (Background)

Lập trình Action trong C++ yêu cầu sử dụng thư viện **`rclcpp_action`**:
- **Action Server:** Cần quản lý 3 callbacks chính:
  1. `handle_goal`: Quyết định chấp nhận hay từ chối Goal.
  2. `handle_cancel`: Quyết định cho phép hủy tác vụ hay không.
  3. `handle_accepted`: Bắt đầu thực thi tác vụ trên một **luồng riêng biệt (separate thread)** để không làm nghẽn luồng executor chính.
- **Action Client:** Cần xử lý 3 callbacks tương ứng từ Server:
  1. `goal_response_callback`: Nhận phản hồi Goal có được chấp nhận không.
  2. `feedback_callback`: Nhận tiến độ trả về liên tục.
  3. `result_callback`: Nhận kết quả cuối cùng sau khi hoàn tất.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package `custom_action_cpp`
```bash
cd ~/ros2_ws/src
ros2 pkg create --dependencies custom_action_interfaces rclcpp rclcpp_action rclcpp_components --license Apache-2.0 custom_action_cpp
```

---

### 2. Viết Action Server (`src/fibonacci_action_server.cpp`)

```cpp
#include <functional>
#include <memory>
#include <thread>

#include "custom_action_interfaces/action/fibonacci.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"

namespace custom_action_cpp
{
class FibonacciActionServer : public rclcpp::Node
{
public:
  using Fibonacci = custom_action_interfaces::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;

  explicit FibonacciActionServer(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : Node("fibonacci_action_server", options)
  {
    using namespace std::placeholders;

    // 1. Callback xử lý khi nhận Goal mới
    auto handle_goal = [this](
      const rclcpp_action::GoalUUID & uuid,
      std::shared_ptr<const Fibonacci::Goal> goal)
    {
      RCLCPP_INFO(this->get_logger(), "Nhan yeu cau Goal voi order = %d", goal->order);
      (void)uuid;
      return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    };

    // 2. Callback xử lý khi Client yêu cầu hủy (Cancel)
    auto handle_cancel = [this](
      const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
      RCLCPP_INFO(this->get_logger(), "Nhan yeu cau huy (Cancel) Goal");
      (void)goal_handle;
      return rclcpp_action::CancelResponse::ACCEPT;
    };

    // 3. Callback khi Goal da duoc chap nhan -> Chay thread rieng de xu ly
    auto handle_accepted = [this](
      const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
      auto execute_in_thread = [this, goal_handle](){ return this->execute(goal_handle); };
      std::thread{execute_in_thread}.detach();
    };

    // Khoi tao Action Server
    this->action_server_ = rclcpp_action::create_server<Fibonacci>(
      this,
      "fibonacci",
      handle_goal,
      handle_cancel,
      handle_accepted);
  }

private:
  rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;

  // Ham thuc thi tinh toan dai han tren thread rieng
  void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "Bat dau thuc thi Goal...");
    rclcpp::Rate loop_rate(1); // 1 Hz (1 giay moi chu ky)
    const auto goal = goal_handle->get_goal();
    auto feedback = std::make_shared<Fibonacci::Feedback>();
    auto & sequence = feedback->sequence;
    sequence.push_back(0);
    sequence.push_back(1);
    auto result = std::make_shared<Fibonacci::Result>();

    for (int i = 1; (i < goal->order) && rclcpp::ok(); ++i) {
      // Kiem tra neu Client yeu cau huy
      if (goal_handle->is_canceling()) {
        result->sequence = sequence;
        goal_handle->canceled(result);
        RCLCPP_INFO(this->get_logger(), "Goal da bi huy bo.");
        return;
      }
      // Tinh so tiep theo trong day Fibonacci
      sequence.push_back(sequence[i] + sequence[i - 1]);
      
      // Publish Feedback
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(this->get_logger(), "Da phat Feedback buoc: %d", i);

      loop_rate.sleep();
    }

    // Hoan thanh Goal thanh cong
    if (rclcpp::ok()) {
      result->sequence = sequence;
      goal_handle->succeed(result);
      RCLCPP_INFO(this->get_logger(), "Goal thanh cong hoan toan (SUCCEEDED).");
    }
  }
};
} // namespace custom_action_cpp

RCLCPP_COMPONENTS_REGISTER_NODE(custom_action_cpp::FibonacciActionServer)
```

---

### 3. Viết Action Client (`src/fibonacci_action_client.cpp`)

```cpp
#include <functional>
#include <future>
#include <memory>
#include <string>
#include <sstream>

#include "custom_action_interfaces/action/fibonacci.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "rclcpp_components/register_node_macro.hpp"

namespace custom_action_cpp
{
class FibonacciActionClient : public rclcpp::Node
{
public:
  using Fibonacci = custom_action_interfaces::action::Fibonacci;
  using GoalHandleFibonacci = rclcpp_action::ClientGoalHandle<Fibonacci>;

  explicit FibonacciActionClient(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : Node("fibonacci_action_client", options)
  {
    this->client_ptr_ = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");

    // Dung Timer goi ham send_goal sau khi node khoi dong
    this->timer_ = this->create_wall_timer(
      std::chrono::milliseconds(500),
      [this](){ return this->send_goal(); });
  }

  void send_goal()
  {
    this->timer_->cancel(); // Huy timer de chi gui goal dung 1 lan

    if (!this->client_ptr_->wait_for_action_server(std::chrono::seconds(10))) {
      RCLCPP_ERROR(this->get_logger(), "Khong tim thay Action Server sau thoi gian cho.");
      rclcpp::shutdown();
      return;
    }

    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = 10;

    RCLCPP_INFO(this->get_logger(), "Dang gui Goal order = 10...");

    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();

    // 1. Callback nhan phan hoi chap nhan Goal
    send_goal_options.goal_response_callback = [this](const GoalHandleFibonacci::SharedPtr & goal_handle) {
      if (!goal_handle) {
        RCLCPP_ERROR(this->get_logger(), "Goal bi Server tu choi :(");
      } else {
        RCLCPP_INFO(this->get_logger(), "Goal duoc Server chap nhan, dang doi ket qua...");
      }
    };

    // 2. Callback nhan Feedback dinh ky
    send_goal_options.feedback_callback = [this](
      GoalHandleFibonacci::SharedPtr,
      const std::shared_ptr<const Fibonacci::Feedback> feedback)
    {
      std::stringstream ss;
      ss << "Nhan Feedback day so: ";
      for (auto number : feedback->sequence) {
        ss << number << " ";
      }
      RCLCPP_INFO(this->get_logger(), "%s", ss.str().c_str());
    };

    // 3. Callback nhan Result cuoi cung
    send_goal_options.result_callback = [this](const GoalHandleFibonacci::WrappedResult & result) {
      switch (result.code) {
        case rclcpp_action::ResultCode::SUCCEEDED:
          break;
        case rclcpp_action::ResultCode::ABORTED:
          RCLCPP_ERROR(this->get_logger(), "Goal bi huy boi Server (ABORTED)");
          return;
        case rclcpp_action::ResultCode::CANCELED:
          RCLCPP_ERROR(this->get_logger(), "Goal bi huy boi Client (CANCELED)");
          return;
        default:
          RCLCPP_ERROR(this->get_logger(), "Ma ket qua khong xac dinh");
          return;
      }
      std::stringstream ss;
      ss << "Nhan KET QUA cuoi cung: ";
      for (auto number : result.result->sequence) {
        ss << number << " ";
      }
      RCLCPP_INFO(this->get_logger(), "%s", ss.str().c_str());
      rclcpp::shutdown();
    };

    // Gui Goal bat dong bo
    this->client_ptr_->async_send_goal(goal_msg, send_goal_options);
  }

private:
  rclcpp_action::Client<Fibonacci>::SharedPtr client_ptr_;
  rclcpp::TimerBase::SharedPtr timer_;
};
} // namespace custom_action_cpp

RCLCPP_COMPONENTS_REGISTER_NODE(custom_action_cpp::FibonacciActionClient)
```

---

### 4. Cấu hình `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.20)
project(custom_action_cpp)

find_package(ament_cmake REQUIRED)
find_package(custom_action_interfaces REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)

# 1. Action Server Target
add_library(action_server SHARED src/fibonacci_action_server.cpp)
target_link_libraries(action_server PUBLIC
  custom_action_interfaces::custom_action_interfaces
  rclcpp::rclcpp
  rclcpp_action::rclcpp_action
  rclcpp_components::component)
rclcpp_components_register_node(action_server PLUGIN "custom_action_cpp::FibonacciActionServer" EXECUTABLE fibonacci_action_server)

# 2. Action Client Target
add_library(action_client SHARED src/fibonacci_action_client.cpp)
target_link_libraries(action_client PUBLIC
  custom_action_interfaces::custom_action_interfaces
  rclcpp::rclcpp
  rclcpp_action::rclcpp_action
  rclcpp_components::component)
rclcpp_components_register_node(action_client PLUGIN "custom_action_cpp::FibonacciActionClient" EXECUTABLE fibonacci_action_client)

install(TARGETS
  action_server
  action_client
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)

ament_package()
```

---

### 5. Biên dịch và Chạy thử nghiệm

```bash
cd ~/ros2_ws
colcon build --packages-select custom_action_cpp
```

Mở 2 terminal để chạy:

```bash
# Terminal 1: Chạy Action Server
source install/setup.bash
ros2 run custom_action_cpp fibonacci_action_server

# Terminal 2: Chạy Action Client
source install/setup.bash
ros2 run custom_action_cpp fibonacci_action_client
```

Client sẽ in ra từng số trong feedback và cuối cùng in toàn bộ dãy số Fibonacci khi đạt trạng thái `SUCCEEDED`!

---

## 📌 Tóm tắt (Summary)
- Sử dụng `rclcpp_action::create_server` và `std::thread` trong Server để xử lý tác vụ dài hạn mà không nghẽn executor.
- Client sử dụng `SendGoalOptions` để đăng ký đồng thời 3 callbacks: `goal_response`, `feedback`, và `result`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[02 - Creating Custom Actions|Tạo Action tùy chỉnh]]
- 🐍 Phiên bản Python: [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]
- ➡️ Bài tiếp theo: [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]

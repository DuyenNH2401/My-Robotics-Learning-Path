---
tags:
  - ros2
  - python
  - rclpy
  - rclpy-action
  - action-server
  - action-client
  - intermediate
created: 2026-08-25
aliases:
  - Viết Action Server và Client bằng Python
  - Writing an action server and client (Python)
---

# 🐍 Viết Action Server và Client bằng Python (rclpy.action)

> [!INFO] **Mục tiêu bài học**
> Xây dựng hoàn chỉnh **Action Server** và **Action Client** bằng Python sử dụng module `rclpy.action`, xuất bản Feedback trong vòng lặp và nhận Result tính toán dãy Fibonacci.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[02 - Creating Custom Actions|Tạo Action tùy chỉnh]]
> - **Bài song song (C++):** [[03 - Writing Action Server and Client (C++)|Viết Action Server và Client (C++)]]
> - **Bài tiếp theo:** [[05 - Writing Async Node with asyncio (Python)|Viết Async Node với asyncio (Python)]]

---

## 📖 Bối cảnh (Background)

Trong Python, module `rclpy.action` cung cấp 2 lớp chính:
- **`ActionServer`**: Tiếp nhận Goal, gọi phương thức `execute_callback`, phát feedback bằng `goal_handle.publish_feedback()` và hoàn thành bằng `goal_handle.succeed()`.
- **`ActionClient`**: Kết nối tới Server, gửi Goal bất đồng bộ qua `send_goal_async()`, nhận feedback qua `feedback_callback` và lấy kết quả qua `get_result_async()`.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Viết Action Server (`fibonacci_action_server.py`)

```python
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        # 1. Khởi tạo ActionServer
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Bat dau thuc thi Goal...')

        # Khởi tạo Feedback và Result
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        # Vòng lặp tính toán dãy số và gửi Feedback
        for i in range(1, goal_handle.request.order):
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            )
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            
            # Gửi Feedback về Client
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1) # Giả lập tác vụ tốn 1 giây mỗi bước

        # Đánh dấu Goal thành công (SUCCEEDED)
        goal_handle.succeed()

        # Trả về Result cuối cùng
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result


def main(args=None):
    try:
        with rclpy.init(args=args):
            fibonacci_action_server = FibonacciActionServer()
            rclpy.spin(fibonacci_action_server)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

---

### 2. Viết Action Client (`fibonacci_action_client.py`)

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')
        # 1. Khởi tạo ActionClient
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info('Dang cho Action Server san sang...')
        self._action_client.wait_for_server()

        self.get_logger().info(f'Dang gui Goal order = {order}...')
        # Gửi Goal bất đồng bộ và đăng ký feedback_callback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    # 2. Callback xử lý khi Server chấp nhận hoặc từ chối Goal
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal bi Server tu choi :(')
            return

        self.get_logger().info('Goal da duoc Server chap nhan, dang cho ket qua...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    # 3. Callback nhận Feedback liên tục trong quá trình thực thi
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Nhan Feedback tu Server: {feedback.sequence}')

    # 4. Callback nhận Result sau khi Server hoàn thành
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Ket qua (Result) cuoi cung: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    try:
        with rclpy.init(args=args):
            action_client = FibonacciActionClient()
            action_client.send_goal(10)
            rclpy.spin(action_client)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

---

### 3. Chạy thử nghiệm

Mở 2 terminal đã source workspace:

```bash
# Terminal 1: Chạy Action Server
python3 fibonacci_action_server.py

# Terminal 2: Chạy Action Client
python3 fibonacci_action_client.py
```

Bạn cũng có thể gửi Goal trực tiếp từ dòng lệnh CLI với cờ `--feedback`:
```bash
ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
```

---

## 📌 Tóm tắt (Summary)
- Tạo Action Server trong Python với `ActionServer(self, ActionType, name, execute_callback)`.
- Client sử dụng `send_goal_async(goal_msg, feedback_callback=...)` kết hợp với `add_done_callback()` để xử lý luồng kết quả không đồng bộ hoàn chỉnh.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[02 - Creating Custom Actions|Tạo Action tùy chỉnh]]
- 💻 Phiên bản C++: [[03 - Writing Action Server and Client (C++)|Viết Action Server và Client (C++)]]
- ➡️ Bài tiếp theo: [[05 - Writing Async Node with asyncio (Python)|Viết Async Node với asyncio (Python)]]

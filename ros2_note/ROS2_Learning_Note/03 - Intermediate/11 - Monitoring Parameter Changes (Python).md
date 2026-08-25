---
tags:
  - ros2
  - python
  - rclpy
  - parameters
  - parameter-event-handler
  - intermediate
created: 2026-08-25
aliases:
  - Theo dõi thay đổi Parameter trong Python
  - Monitoring for parameter changes (Python)
---

# 🐍 Theo dõi thay đổi Parameter trong Python (rclpy.parameter_event_handler)

> [!INFO] **Mục tiêu bài học**
> Sử dụng lớp **`ParameterEventHandler`** trong Python (`rclpy`) để đăng ký callback tự động xử lý khi các [[06 - Understanding Parameters|Parameters]] được cập nhật.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]
> - **Bài song song (C++):** [[10 - Monitoring Parameter Changes (C++)|Theo dõi thay đổi Parameter (C++)]]
> - **Bài tiếp theo:** [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]

---

## 📖 Bối cảnh (Background)

Trong Python, module `rclpy.parameter_event_handler` cung cấp cơ chế đăng ký callback bất đồng bộ để nhận thông báo khi có sự thay đổi tham số cấu hình.

---

## 🛠️ Triển khai mã nguồn Python (Tasks)

### 1. Tạo Package `python_parameter_event_handler`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 python_parameter_event_handler --dependencies rclpy
```

---

### 2. Viết Node Python (`python_parameter_event_handler/parameter_event_handler.py`)

```python
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import rclpy.parameter
from rclpy.parameter_event_handler import ParameterEventHandler


class SampleNodeWithParameters(Node):
    def __init__(self):
        super().__init__('node_with_parameters')

        # 1. Khai báo parameter cục bộ
        self.declare_parameter('an_int_param', 0)
        self.declare_parameter('another_double_param', 0.0)

        # 2. Khởi tạo ParameterEventHandler
        self.handler = ParameterEventHandler(self)

        # 3. Đăng ký theo dõi parameter cục bộ (Bắt buộc lưu handle vào self)
        self.callback_handle = self.handler.add_parameter_callback(
            parameter_name="an_int_param",
            node_name="node_with_parameters",
            callback=self.param_callback,
        )

        # 4. Đăng ký theo dõi parameter từ xa (Remote node: 'parameter_blackboard')
        self.callback_handle_remote = self.handler.add_parameter_callback(
            parameter_name="a_double_param",
            node_name="parameter_blackboard",
            callback=self.param_callback,
        )

        # 5. Đăng ký lắng nghe TOÀN BỘ sự kiện ParameterEvent
        self.event_callback_handle = self.handler.add_parameter_event_callback(
            callback=self.event_callback,
        )

    # Callback cho 1 parameter cụ thể
    def param_callback(self, p: rclpy.parameter.Parameter) -> None:
        val = rclpy.parameter.parameter_value_to_python(p.value)
        self.get_logger().info(f"Nhan cap nhat param '{p.name}': gia tri moi = {val}")

    # Callback cho su kien tong quat ParameterEvent
    def event_callback(self, parameter_event) -> None:
        self.get_logger().info(f"Su kien ParameterEvent tu Node: {parameter_event.node}")
        for p in parameter_event.changed_parameters:
            val = rclpy.parameter.parameter_value_to_python(p.value)
            self.get_logger().info(f" - Param '{p.name}' -> {val}")


def main():
    try:
        with rclpy.init():
            node = SampleNodeWithParameters()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

---

### 3. Cấu hình `setup.py`
Thêm entry point:
```python
entry_points={
    'console_scripts': [
        'node_with_parameters = python_parameter_event_handler.parameter_event_handler:main',
    ],
},
```

---

### 4. Biên dịch và Chạy thử

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select python_parameter_event_handler
source install/setup.bash

# Terminal 1: Chạy node
ros2 run python_parameter_event_handler node_with_parameters
```

Mở terminal 2 để set parameter:
```bash
ros2 param set node_with_parameters an_int_param 43
```
Terminal 1 sẽ lập tức phản hồi thông báo nhận giá trị 43 thành công!

---

## 📌 Tóm tắt (Summary)
- `ParameterEventHandler` trong Python giúp code ngắn gọn và dễ quản lý.
- Luôn gán kết quả trả về của `add_parameter_callback` vào biến thành viên (`self.callback_handle`) để tránh bị Python Garbage Collector thu hồi.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]
- 💻 Phiên bản C++: [[10 - Monitoring Parameter Changes (C++)|Theo dõi thay đổi Parameter (C++)]]
- ➡️ Bài tiếp theo: [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]

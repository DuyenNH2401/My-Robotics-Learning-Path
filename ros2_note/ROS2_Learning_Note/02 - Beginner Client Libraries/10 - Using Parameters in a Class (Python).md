---
tags:
  - ros2
  - python
  - rclpy
  - parameters
  - launch
  - beginner
created: 2026-08-25
aliases:
  - Sử dụng Parameters trong Class (Python)
  - Using parameters in a class (Python)
---

# 🐍 Sử dụng Parameters trong Class Python (rclpy)

> [!INFO] **Mục tiêu bài học**
> Học cách khai báo (declare), đọc (get) và cập nhật (set) [[06 - Understanding Parameters|Parameters]] bên trong class Node Python (`rclpy.node.Node`), và tích hợp nạp tham số qua Launch file.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 20 phút
> - **Bài trước:** [[08 - Creating Custom Interfaces (msg and srv)|Tạo Message và Service tùy chỉnh]]
> - **Bài song song (C++):** [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]]
> - **Bài tiếp theo:** [[11 - Using ROS2 Doctor|Kiểm tra hệ thống với ros2doctor]]

---

## 📖 Bối cảnh (Background)

Trong Python (`rclpy`), việc khai báo parameter được thực hiện trực quan thông qua các phương thức của đối tượng `Node`.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package `python_parameters`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 python_parameters --dependencies rclpy
```

---

### 2. Viết Node Python (`python_parameters/python_parameters_node.py`)

```python
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import rclpy.parameter


class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')

        # 1. Khai báo parameter kèm giá trị mặc định
        self.declare_parameter('my_parameter', 'world')

        # 2. Tạo Timer lặp định kỳ 1s
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        # Đọc giá trị chuỗi của parameter
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value

        self.get_logger().info(f'Hello {my_param}!')

        # Cập nhật lại parameter (tùy chọn)
        my_new_param = rclpy.parameter.Parameter(
            'my_parameter',
            rclpy.Parameter.Type.STRING,
            'world'
        )
        self.set_parameters([my_new_param])


def main():
    try:
        with rclpy.init():
            node = MinimalParam()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

> [!TIP] **Thêm mô tả cho Parameter trong Python:**
> ```python
> from rcl_interfaces.msg import ParameterDescriptor
> 
> my_descriptor = ParameterDescriptor(description='Mô tả về tham số này!')
> self.declare_parameter('my_parameter', 'world', my_descriptor)
> ```

---

### 3. Cấu hình Launch file trong Package Python

Tạo thư mục `launch` và file `launch/python_parameters_launch.py`:
```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='python_parameters',
            executable='minimal_param_node',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'my_parameter': 'earth'}
            ]
        )
    ])
```

#### Cập nhật `setup.py` để copy thư mục `launch`:
```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'python_parameters'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Bổ sung dòng này để cài đặt các file launch vào share/<package_name>/launch
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='YourName',
    maintainer_email='you@email.com',
    description='Python parameter tutorial',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'minimal_param_node = python_parameters.python_parameters_node:main',
        ],
    },
)
```

---

### 4. Biên dịch và Chạy thử nghiệm

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select python_parameters
source install/setup.bash

# Khởi chạy bằng Launch file
ros2 launch python_parameters python_parameters_launch.py
```
Dòng log đầu tiên sẽ in ra: `[custom_minimal_param_node]: Hello earth!`.

---

## 📌 Tóm tắt (Summary)
- Khai báo tham số trong Python với `self.declare_parameter(name, default_value)`.
- Đọc giá trị bằng `self.get_parameter(name).get_parameter_value()`.
- Cài đặt thư mục launch thông qua tham số `data_files` trong `setup.py`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[08 - Creating Custom Interfaces (msg and srv)|Tạo Message và Service tùy chỉnh]]
- 💻 Phiên bản C++: [[09 - Using Parameters in a Class (C++)|Sử dụng Parameters trong Class (C++)]]
- ➡️ Bài tiếp theo: [[11 - Using ROS2 Doctor|Kiểm tra hệ thống với ros2doctor]]

---
tags:
  - ros2
  - urdf
  - robot_state_publisher
  - joint_state
  - python
  - rclpy
  - rviz2
  - intermediate
created: 2026-08-25
aliases:
  - Sử dụng URDF với robot_state_publisher bằng Python
  - Using URDF with robot_state_publisher (Python)
---

# 🐍 Sử dụng URDF với robot_state_publisher bằng Python (State Publisher)

> [!INFO] **Mục tiêu bài học**
> Xây dựng một node Python (`rclpy`) để mô phỏng chuyển động robot: xuất bản dữ liệu góc khớp **`JointState`** và biến đổi vị trí tổng thể robot trong không gian (`odom -> axis`) kết hợp với **`robot_state_publisher`** để hiển thị chuyển động động học trong **RViz2**.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[04 - Using Xacro to Clean Up URDF Code|Sử dụng Xacro Tối ưu hóa Mã nguồn URDF]]
> - **Bài song song (C++):** [[05 - Using URDF with robot_state_publisher (C++)|Sử dụng URDF với robot_state_publisher (C++)]]
> - **Bài tiếp theo:** [[07 - Exporting URDF from CAD and Tools|Xuất file URDF từ phần mềm CAD]]

---

## 🛠️ Triển khai mã nguồn Python (Tasks)

### 1. Tạo Package `urdf_tutorial_r2d2`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 urdf_tutorial_r2d2 --dependencies rclpy
```

---

### 2. Viết Node Python (`urdf_tutorial_r2d2/state_publisher.py`)

```python
from math import cos, pi, sin
from geometry_msgs.msg import Quaternion, TransformStamped
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster


def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2)*cos(pitch/2)*cos(yaw/2) - cos(roll/2)*sin(pitch/2)*sin(yaw/2)
    qy = cos(roll/2)*sin(pitch/2)*cos(yaw/2) + sin(roll/2)*cos(pitch/2)*sin(yaw/2)
    qz = cos(roll/2)*cos(pitch/2)*sin(yaw/2) - sin(roll/2)*sin(pitch/2)*cos(yaw/2)
    qw = cos(roll/2)*cos(pitch/2)*cos(yaw/2) + sin(roll/2)*sin(pitch/2)*sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)


class StatePublisher(Node):

    def __init__(self):
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        
        # 1. Publisher xuất bản trạng thái góc khớp
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        
        # 2. Broadcaster phát biến đổi tọa độ odom -> axis
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        
        # 3. Timer chu kỳ 30 Hz
        self.timer = self.create_timer(1.0 / 30.0, self.update)

        self.degree = pi / 180.0
        self.tilt = 0.0
        self.tinc = self.degree
        self.swivel = 0.0
        self.angle = 0.0
        self.height = 0.0
        self.hinc = 0.005

        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = 'odom'
        self.odom_trans.child_frame_id = 'axis'
        self.joint_state = JointState()

    def update(self):
        now = self.get_clock().now()

        # A. Cập nhật JointState cho 3 khớp: swivel, tilt, periscope
        self.joint_state.header.stamp = now.to_msg()
        self.joint_state.name = ['swivel', 'tilt', 'periscope']
        self.joint_state.position = [self.swivel, self.tilt, self.height]

        # B. Cập nhật Transform robot chuyển động vòng tròn (bán kính = 2m)
        self.odom_trans.header.stamp = now.to_msg()
        self.odom_trans.transform.translation.x = cos(self.angle) * 2.0
        self.odom_trans.transform.translation.y = sin(self.angle) * 2.0
        self.odom_trans.transform.translation.z = 0.7
        self.odom_trans.transform.rotation = euler_to_quaternion(0.0, 0.0, self.angle + pi / 2.0)

        # Phát tin
        self.joint_pub.publish(self.joint_state)
        self.broadcaster.sendTransform(self.odom_trans)

        # C. Cập nhật góc động học
        self.tilt += self.tinc
        if self.tilt < -0.5 or self.tilt > 0.0:
            self.tinc *= -1.0
        self.height += self.hinc
        if self.height > 0.2 or self.height < 0.0:
            self.hinc *= -1.0
        self.swivel += self.degree
        self.angle += self.degree / 4.0


def main():
    try:
        with rclpy.init():
            node = StatePublisher()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

---

### 3. Cấu hình `setup.py`
```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'urdf_tutorial_r2d2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name), glob('urdf/*')),
    ],
    entry_points={
        'console_scripts': [
            'state_publisher = urdf_tutorial_r2d2.state_publisher:main',
        ],
    },
)
```

---

### 4. Viết Launch File (`launch/demo_launch.py`)

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import FileContent, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    urdf = FileContent(
        PathJoinSubstitution([FindPackageShare('urdf_tutorial_r2d2'), 'r2d2.urdf.xml'])
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': urdf}],
        ),
        Node(
            package='urdf_tutorial_r2d2',
            executable='state_publisher',
        ),
    ])
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng Python xuất bản `JointState` và `TransformBroadcaster` giúp nhanh chóng tạo các bộ giả lập kinematics cho robot.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[04 - Using Xacro to Clean Up URDF Code|Sử dụng Xacro Tối ưu hóa Mã nguồn URDF]]
- ➡️ Bài tiếp theo: [[07 - Exporting URDF from CAD and Tools|Xuất file URDF từ phần mềm CAD]]

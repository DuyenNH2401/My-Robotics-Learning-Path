---
aliases: [Launching nodes]
tags: [ros2, launch, cli, node]
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
translation-status: complete
---

# Khởi chạy nhiều node

## Nguồn

- Lyrical: [Launching nodes](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)
- Jazzy: [Launching nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)
- Humble: [Launching nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)

## Mục tiêu

Dùng command line để khởi chạy nhiều [[Node|node]] cùng lúc.

## Điều kiện tiên quyết

- Đã cài ROS 2 và source ROS 2 trong terminal mới.
- Command giả định bản cài binary (package `deb` trên Linux). Nếu build from source, đường dẫn setup file có thể khác và không dùng được `sudo apt install ros-<distro>-<package>`.

## Nội dung

Khi hệ thống có nhiều node, mở terminal và nhập lại cấu hình cho từng node trở nên phiền. [[Launch file]] khởi động và cấu hình đồng thời nhiều executable chứa ROS 2 node; một `ros2 launch` khởi động toàn hệ thống, gồm mọi node và cấu hình.

### Chạy launch file

```console
$ ros2 launch turtlesim multisim.launch.py
```

Command này chạy launch file Python sau:

```python
from launch import LaunchDescription
import launch_ros.actions


def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            namespace='turtlesim1', package='turtlesim',
            executable='turtlesim_node', output='screen'),
        launch_ros.actions.Node(
            namespace='turtlesim2', package='turtlesim',
            executable='turtlesim_node', output='screen'),
    ])
```

Launch file cũng có thể viết bằng XML hoặc YAML. Bài này chỉ dùng file có sẵn: hai node `turtlesim` sẽ chạy.

![Hai cửa sổ turtlesim được launch trong namespace turtlesim1 và turtlesim2](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/turtlesim-multisim.png)

*Nguồn ảnh: [turtlesim_multisim.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/images/turtlesim_multisim.png).*

### Tùy chọn: điều khiển hai turtlesim node

Mở hai terminal nữa. Terminal thứ hai:

```console
$ ros2 topic pub  /turtlesim1/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

Terminal thứ ba:

```console
$ ros2 topic pub  /turtlesim2/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -1.8}}"
```

Hai turtle quay theo hướng ngược nhau.

![Hai turtlesim quay theo hai hướng ngược nhau sau khi publish hai cmd_vel namespace riêng](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/turtlesim-multisim-spin.png)

*Nguồn ảnh: [turtlesim_multisim_spin.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/images/turtlesim_multisim_spin.png).*

Bạn vừa chạy hai turtlesim node bằng một command. Khi biết viết launch file, bạn có thể chạy nhiều node và cấu hình của chúng theo cùng cách với `ros2 launch`.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Nội dung, package/file name, code launch, command và hành vi giống Lyrical.

> [!warning] ROS 2 Humble
> Nội dung, package/file name, code launch, command và hành vi giống Lyrical.

## Kiến thức liên quan

- [[Launch file]]
- [[Node]]
- [[Topic]]
- [[turtlesim]]

## Bước tiếp theo

- [[Ghi và phát lại dữ liệu]]

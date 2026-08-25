---
aliases:
  - Understanding nodes
tags:
  - ros2
  - node
  - cli
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html
translation-status: complete
---

# Tìm hiểu về node

## Nguồn

- Lyrical: [Understanding nodes](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- Jazzy: [Understanding nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
- Humble: [Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)

## Mục tiêu

Khởi chạy, liệt kê, remap tên và introspect [[Node|node]] bằng `ros2` CLI.

## Điều kiện tiên quyết

- Hoàn thành [[Sử dụng turtlesim, ros2 và rqt]].
- Source ROS 2 trong mỗi terminal mới.

## Nội dung

[[ROS graph]] là mạng các thành phần ROS 2 cùng xử lý dữ liệu và các kết nối giữa chúng. Một node có một mục đích mô-đun; nó trao đổi dữ liệu qua [[Topic|topic]], service, action hoặc parameter. Một executable C++ hoặc Python có thể chứa một hay nhiều node.

### Khởi chạy executable

`ros2 run` khởi chạy một executable từ package:

```console
$ ros2 run <package_name> <executable_name>
```

Khởi chạy executable `turtlesim_node` trong package `turtlesim`:

```console
$ ros2 run turtlesim turtlesim_node
```

`turtlesim_node` là **tên executable**, chưa phải tên node. Tên node chỉ xuất hiện khi process đang chạy.

### Liệt kê node đang chạy

Trong terminal khác, chạy:

```console
$ ros2 node list
/turtlesim
```

Khởi chạy executable teleoperation ở terminal thứ ba:

```console
$ ros2 run turtlesim turtle_teleop_key
```

Chạy lại danh sách; hai node mặc định là:

```console
$ ros2 node list
/turtlesim
/teleop_turtle
```

### Remap tên node

Remapping gán lại thuộc tính mặc định, như node name, topic name hoặc service name. Khởi chạy thêm `turtlesim_node` và remap tên node của nó:

```console
$ ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
```

Lúc này `ros2 node list` cho thấy ba node. `my_turtle` là tên node đã remap, còn executable vẫn là `turtlesim_node`:

```console
$ ros2 node list
/my_turtle
/turtlesim
/teleop_turtle
```

### Xem các kết nối của node

Dùng tên node, không dùng tên executable, với `ros2 node info`:

```console
$ ros2 node info <node_name>
```

Ví dụ với node vừa remap:

```console
$ ros2 node info /my_turtle
/my_turtle
  Subscribers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /turtle1/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /turtle1/color_sensor: turtlesim_msgs/msg/Color
    /turtle1/pose: turtlesim_msgs/msg/Pose
  Service Servers:
    /clear: std_srvs/srv/Empty
    /kill: turtlesim_msgs/srv/Kill
    /my_turtle/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /my_turtle/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /my_turtle/get_parameters: rcl_interfaces/srv/GetParameters
    /my_turtle/list_parameters: rcl_interfaces/srv/ListParameters
    /my_turtle/set_parameters: rcl_interfaces/srv/SetParameters
    /my_turtle/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
    /reset: std_srvs/srv/Empty
    /spawn: turtlesim_msgs/srv/Spawn
    /turtle1/set_pen: turtlesim_msgs/srv/SetPen
    /turtle1/teleport_absolute: turtlesim_msgs/srv/TeleportAbsolute
    /turtle1/teleport_relative: turtlesim_msgs/srv/TeleportRelative
  Service Clients:

  Action Servers:
    /turtle1/rotate_absolute: turtlesim_msgs/action/RotateAbsolute
  Action Clients:
```

Output liệt kê subscriber, publisher, service và action có kết nối với node này. Thử `ros2 node info /teleop_turtle` để đối chiếu các kết nối của node điều khiển.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Thao tác và command giống Lyrical. Trong output mẫu, interface của turtlesim dùng package `turtlesim`, ví dụ `turtlesim/msg/Pose`, thay vì `turtlesim_msgs/msg/Pose`.

> [!warning] ROS 2 Humble
> Thao tác và command giống Lyrical. Interface turtlesim trong output mẫu cũng dùng package `turtlesim`, không phải `turtlesim_msgs`.

## Kiến thức liên quan

- [[Node]]
- [[ROS graph]]
- [[Topic]]
- [[Publisher]]
- [[Subscriber]]
- [[turtlesim]]
- [[ros2 CLI]]

## Bước tiếp theo

- [[Tìm hiểu về topic]]

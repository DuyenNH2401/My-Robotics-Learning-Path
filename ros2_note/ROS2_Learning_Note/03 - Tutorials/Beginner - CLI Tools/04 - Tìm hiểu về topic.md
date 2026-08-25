---
aliases:
  - Understanding topics
  - Tìm hiểu về topic
tags:
  - ros2
  - topic
  - cli
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html
translation-status: complete
---

# Tìm hiểu về topic

## Nguồn

- Lyrical: [Understanding topics](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- Jazzy: [Understanding topics](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- Humble: [Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

## Mục tiêu

Dùng `rqt_graph` và `ros2` CLI để quan sát [[Topic|topic]], message và các [[Publisher|publisher]]/[[Subscriber|subscriber]].

## Điều kiện tiên quyết

- Hoàn thành [[Tìm hiểu về node]].
- Source ROS 2 trong mỗi terminal mới và cài `rqt_graph` theo [[Sử dụng turtlesim, ros2 và rqt]].

## Nội dung

Topic là bus message trong [[ROS graph]]. Node có thể publish tới nhiều topic và subscribe nhiều topic cùng lúc; một topic có thể có one-to-many, many-to-one hoặc many-to-many publisher/subscriber. Đây là luồng dữ liệu liên tục, khác với service request/response và action cho tác vụ dài có feedback/cancel.

### Khởi động ví dụ và mở đồ thị

Trong hai terminal riêng, chạy:

```console
$ ros2 run turtlesim turtlesim_node
```

```console
$ ros2 run turtlesim turtle_teleop_key
```

Mở công cụ đồ thị:

```console
$ ros2 run rqt_graph rqt_graph
```

`/teleop_turtle` publish keystroke tới `/turtle1/cmd_vel`; `/turtlesim` subscribe topic đó. Trong `rqt`, cũng có thể mở **Plugins** > **Introspection** > **Node Graph**.

### Liệt kê và xác định type

Liệt kê các topic đang hoạt động:

```console
$ ros2 topic list
/parameter_events
/rosout
/turtle1/cmd_vel
/turtle1/color_sensor
/turtle1/pose
```

Thêm `-t` để xem type:

```console
$ ros2 topic list -t
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim_msgs/msg/Color]
/turtle1/pose [turtlesim_msgs/msg/Pose]
```

Có thể hỏi trực tiếp type của một topic:

```console
$ ros2 topic type /turtle1/cmd_vel
geometry_msgs/msg/Twist
```

Các node chỉ giao tiếp khi type message phù hợp.

### Xem message đang chảy

`echo` tạo một node tạm thời để subscribe và in message:

```console
$ ros2 topic echo <topic_name>
```

```console
$ ros2 topic echo /turtle1/cmd_vel
```

Nhấn phím mũi tên trong terminal `turtle_teleop_key`; output là message `Twist`:

```console
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

### Xem endpoint và cấu trúc message

Xem type cùng số publisher/subscription:

```console
$ ros2 topic info /turtle1/cmd_vel
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 2
```

Thêm `--verbose` (hoặc `-v`) để có node name, namespace, type, QoS profile và thông tin endpoint:

```console
$ ros2 topic info /turtle1/cmd_vel --verbose
```

Xem cấu trúc của `geometry_msgs/msg/Twist` trước khi publish:

```console
$ ros2 interface show geometry_msgs/msg/Twist
# This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
            float64 x
            float64 y
            float64 z
    Vector3  angular
            float64 x
            float64 y
            float64 z
```

Message có hai vector `linear` và `angular`, mỗi vector có `x`, `y`, `z`.

### Publish từ command line

Cú pháp chung là:

```console
$ ros2 topic pub <topic_name> <msg_type> '<args>'
```

`<args>` là YAML theo cấu trúc message. Command sau publish liên tục (mặc định 1 Hz) để turtle tiếp tục di chuyển:

```console
$ ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

Chỉ publish một message rồi thoát; `-w 2` chờ hai subscription khớp (`turtlesim` và `topic echo`):

```console
$ ros2 topic pub --once -w 2 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
Waiting for at least 2 matching subscription(s)...
publisher: beginning loop
publishing #1: geometry_msgs.msg.Twist(linear=geometry_msgs.msg.Vector3(x=2.0, y=0.0, z=0.0), angular=geometry_msgs.msg.Vector3(x=0.0, y=0.0, z=1.8))
```

### Đo tần suất

Đo tốc độ nhận message của subscription do CLI tạo:

```console
$ ros2 topic hz /turtle1/pose
average rate: 59.354
  min: 0.005s max: 0.027s std dev: 0.00284s window: 58
```

Kết quả là tốc độ nhận và có thể khác tốc độ publisher vì tài nguyên platform hoặc QoS. Kết thúc các node bằng `Ctrl+C` ở từng terminal.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Command và thao tác giống Lyrical. `ros2 topic list -t` hiển thị `turtlesim/msg/Color` và `turtlesim/msg/Pose`, thay cho `turtlesim_msgs/...`.

> [!warning] ROS 2 Humble
> Cùng thay đổi tên interface `turtlesim/...` như Jazzy. Phần `ros2 topic pub` của Humble không còn các ví dụ autocomplete và message rỗng có trong Lyrical/Jazzy; cú pháp YAML, publish liên tục và `--once` vẫn giống nhau.

## Kiến thức liên quan

- [[Topic]]
- [[Publisher]]
- [[Subscriber]]
- [[Node]]
- [[ROS graph]]
- [[ros2 CLI]]
- [[rqt]]

## Bước tiếp theo

- [[Tìm hiểu về service]]

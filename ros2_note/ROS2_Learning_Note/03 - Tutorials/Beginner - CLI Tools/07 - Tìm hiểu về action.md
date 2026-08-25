---
aliases:
  - Understanding actions
  - Tìm hiểu về action
tags:
  - ros2
  - action
  - cli
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
translation-status: complete
---

# Tìm hiểu về action

## Nguồn

- Lyrical: [Understanding actions](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- Jazzy: [Understanding actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- Humble: [Understanding actions](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

## Mục tiêu

Introspect [[Action|action]] trong ROS 2 và gửi action goal.

## Điều kiện tiên quyết

- Hoàn thành [[Tìm hiểu về node]] và [[Tìm hiểu về topic]].
- Source ROS 2 trong mỗi terminal mới và chạy `turtlesim`.

## Nội dung

Action dành cho tác vụ lâu, gồm goal, feedback và result. [[Action client]] gửi goal tới [[Action server]]; server xác nhận, gửi feedback, rồi trả result. Action được xây trên topic/service và, không như [[Service]], goal có thể cancel.

### Khởi động và cancel bằng teleop

```console
$ ros2 run turtlesim turtlesim_node
```

```console
$ ros2 run turtlesim turtle_teleop_key
Use arrow keys to move the turtle.
Use G|B|V|C|D|E|R|T keys to rotate to absolute orientations. 'F' to cancel a rotation.
```

Các phím quanh `F` (bố cục US QWERTY) gửi goal xoay turtle tới hướng tuyệt đối tương ứng. `F` cancel goal đang chạy:

```console
[INFO] [turtlesim]: Rotation goal canceled
```

Nếu đang xoay mà gửi goal mới, action server turtlesim abort goal cũ:

```console
[WARN] [turtlesim]: Rotation goal received before a previous goal finished. Aborting previous goal
```

Đây là lựa chọn riêng của server; action server khác có thể reject goal mới hoặc đợi goal cũ xong.

### Xác định action client và action server

```console
$ ros2 node info /turtlesim
```

Trong output, `/turtle1/rotate_absolute: turtlesim_msgs/action/RotateAbsolute` nằm dưới `Action Servers`; vì vậy `/turtlesim` là action server. Chạy:

```console
$ ros2 node info /teleop_turtle
```

Trong output, action đó nằm dưới `Action Clients`; `/teleop_turtle` là action client gửi goal.

### Liệt kê, xem type và endpoint

```console
$ ros2 action list
/turtle1/rotate_absolute
```

```console
$ ros2 action list -t
/turtle1/rotate_absolute [turtlesim_msgs/action/RotateAbsolute]
```

```console
$ ros2 action type /turtle1/rotate_absolute
turtlesim_msgs/action/RotateAbsolute
```

```console
$ ros2 action info /turtle1/rotate_absolute
Action: /turtle1/rotate_absolute
Action clients: 1
    /teleop_turtle
Action servers: 1
    /turtlesim
```

### Xem interface và gửi goal

```console
$ ros2 interface show turtlesim_msgs/action/RotateAbsolute
# The desired heading in radians
float32 theta
---
# The angular displacement in radians to the starting position
float32 delta
---
# The remaining rotation in radians
float32 remaining
```

Ba phần lần lượt là cấu trúc goal request, result và feedback. Cú pháp gửi goal:

```console
$ ros2 action send_goal <action_name> <action_type> <values>
```

`<values>` dùng YAML.

```console
$ ros2 action send_goal /turtle1/rotate_absolute turtlesim_msgs/action/RotateAbsolute "{theta: 1.57}"
Waiting for an action server to become available...
Sending goal:
   theta: 1.57

Goal accepted with ID: f8db8f44410849eaa93d3feb747dd444

Result:
  delta: -1.568000316619873

Goal finished with status: SUCCEEDED
```

Mỗi goal có ID duy nhất. Thêm `--feedback` để nhận feedback cho đến khi hoàn tất:

```console
$ ros2 action send_goal /turtle1/rotate_absolute turtlesim_msgs/action/RotateAbsolute "{theta: -1.57}" --feedback
Sending goal:
   theta: -1.57

Goal accepted with ID: e6092c831f994afda92f0086f220da27

Feedback:
  remaining: -3.1268222332000732

Feedback:
  remaining: -3.1108222007751465

…

Result:
  delta: 3.1200008392333984

Goal finished with status: SUCCEEDED
```

### Quan sát action bằng introspection

Lyrical có `ros2 action echo`; action introspection mặc định tắt. Khởi động hai demo với parameter cấu hình introspection rồi echo action:

```console
$ ros2 run action_tutorials_cpp fibonacci_action_server --ros-args -p action_server_configure_introspection:=contents
```

```console
$ ros2 run action_tutorials_py fibonacci_action_client --ros-args -p action_client_configure_introspection:=contents
```

```console
$ ros2 action echo /fibonacci example_interfaces/action/Fibonacci --flow-style
```

Output cho thấy `GOAL_SERVICE`, `RESULT_SERVICE`, `FEEDBACK_TOPIC` và `STATUS_TOPIC`. Tính năng này có từ Kilted Kaiju trở lên.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Các interface turtlesim dùng `turtlesim/msg/...`, `turtlesim/srv/...` và `turtlesim/action/...`, không dùng `turtlesim_msgs/...`. Tutorial Jazzy không có phần `ros2 action echo` Lyrical; các phần `list`, `type`, `info`, `interface show`, `send_goal`, feedback và cancel tương đương.

> [!warning] ROS 2 Humble
> Cũng dùng namespace interface `turtlesim/...`. Tutorial Humble không có `ros2 action type` và `ros2 action echo`; dùng `ros2 action list -t` để lấy type. Luồng goal, feedback, cancel và các command còn lại không đổi.

## Kiến thức liên quan

- [[Action]]
- [[Action client]]
- [[Action server]]
- [[Service]]
- [[Topic]]
- [[ros2 CLI]]

## Bước tiếp theo

- [[Xem log bằng rqt_console]]

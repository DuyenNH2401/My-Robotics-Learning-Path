---
aliases:
  - Understanding services
tags:
  - ros2
  - service
  - cli
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
translation-status: complete
---

# Tìm hiểu về service

## Nguồn

- Lyrical: [Understanding services](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- Jazzy: [Understanding services](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
- Humble: [Understanding services](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)

## Mục tiêu

Tìm, introspect và gọi [[Service|service]] bằng command-line tools.

## Điều kiện tiên quyết

- Hoàn thành [[Tìm hiểu về node]] và [[Tìm hiểu về topic]].
- Source ROS 2 trong mỗi terminal mới và cài `turtlesim` theo [[Sử dụng turtlesim, ros2 và rqt]].

## Nội dung

Service là giao tiếp call-and-response trong [[ROS graph]]. [[Service client]] chỉ nhận dữ liệu khi gọi service, trái với [[Topic|topic]] cho dữ liệu stream liên tục.

### Khởi động turtlesim

Trong hai terminal riêng, chạy:

```console
$ ros2 run turtlesim turtlesim_node
```

```console
$ ros2 run turtlesim turtle_teleop_key
```

### Liệt kê và xem type service

```console
$ ros2 service list
/clear
/kill
/reset
/spawn
/teleop_turtle/describe_parameters
/teleop_turtle/get_parameter_types
/teleop_turtle/get_parameters
/teleop_turtle/list_parameters
/teleop_turtle/set_parameters
/teleop_turtle/set_parameters_atomically
/turtle1/set_pen
/turtle1/teleport_absolute
/turtle1/teleport_relative
/turtlesim/describe_parameters
/turtlesim/get_parameter_types
/turtlesim/get_parameters
/turtlesim/list_parameters
/turtlesim/set_parameters
/turtlesim/set_parameters_atomically
```

Gần như mọi node ROS 2 có sáu infrastructure service liên quan parameter; tập trung vào service riêng của turtlesim là `/clear`, `/kill`, `/reset`, `/spawn`, `/turtle1/set_pen`, `/turtle1/teleport_absolute` và `/turtle1/teleport_relative`.

Service type gồm message request và response. Xem type của một service hoặc của toàn bộ danh sách:

```console
$ ros2 service type <service_name>
```

```console
$ ros2 service type /clear
std_srvs/srv/Empty
```

`Empty` nghĩa là cả request lẫn response không mang dữ liệu.

```console
$ ros2 service list -t
/clear [std_srvs/srv/Empty]
/kill [turtlesim_msgs/srv/Kill]
/reset [std_srvs/srv/Empty]
/spawn [turtlesim_msgs/srv/Spawn]
...
/turtle1/set_pen [turtlesim_msgs/srv/SetPen]
/turtle1/teleport_absolute [turtlesim_msgs/srv/TeleportAbsolute]
/turtle1/teleport_relative [turtlesim_msgs/srv/TeleportRelative]
...
```

### Xem endpoint và tìm theo type

`info` trả về type cùng số service client/server:

```console
$ ros2 service info <service_name>
```

```console
$ ros2 service info /clear
Type: std_srvs/srv/Empty
Clients count: 0
Services count: 1
```

`--verbose` (hay `-v`) bổ sung node name, namespace, endpoint và chi tiết RMW. Với RMW dựa trên DDS, một service server có hai endpoint (request và response); `rmw_zenoh_cpp` dùng một endpoint chung.

```console
$ ros2 service info --verbose <service_name>
```

Tìm tất cả service có một type:

```console
$ ros2 service find <type_name>
```

```console
$ ros2 service find std_srvs/srv/Empty
/clear
/reset
```

### Xem interface và gọi service

```console
$ ros2 interface show std_srvs/srv/Empty
---
```

Dấu `---` ngăn request (phía trên) và response (phía dưới). Interface `/spawn` có dữ liệu ở cả hai phía:

```console
$ ros2 interface show turtlesim_msgs/srv/Spawn
float32 x
float32 y
float32 theta
string name # Optional.  A unique name will be created and returned if this is empty
---
string name
```

`x`, `y`, `theta` xác định pose 2D; `name` là optional. Cú pháp gọi là:

```console
$ ros2 service call <service_name> <service_type> <arguments>
```

`<arguments>` là optional và, khi có, phải theo YAML. Gọi service rỗng:

```console
$ ros2 service call /clear std_srvs/srv/Empty
```

Gọi `/spawn` để tạo turtle mới:

```console
$ ros2 service call /spawn turtlesim_msgs/srv/Spawn "{x: 2, y: 2, theta: 0.2, name: ''}"
requester: making request: turtlesim_msgs.srv.Spawn_Request(x=2.0, y=2.0, theta=0.2, name='')

response:
turtlesim_msgs.srv.Spawn_Response(name='turtle2')
```

### Quan sát service bằng introspection

Lyrical có `ros2 service echo`; service introspection bị tắt mặc định. Khởi động demo, bật introspection trên service client và service server, rồi echo:

```console
$ ros2 launch demo_nodes_cpp introspect_services_launch.py
```

```console
$ ros2 param set /introspection_service service_configure_introspection contents
$ ros2 param set /introspection_client client_configure_introspection contents
```

```console
$ ros2 service echo --flow-style /add_two_ints
```

Output hiển thị tuần tự `REQUEST_SENT`, `REQUEST_RECEIVED`, `RESPONSE_SENT`, `RESPONSE_RECEIVED`, cùng request và response.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Các service interface của turtlesim dùng `turtlesim/srv/...`, thay cho `turtlesim_msgs/srv/...`. Tutorial Jazzy không có phần `ros2 service info --verbose` của Lyrical, nhưng vẫn có đầy đủ phần `ros2 service echo`.

> [!warning] ROS 2 Humble
> Cũng dùng `turtlesim/srv/...`; ngoài các phần introspection trên, Humble không có cả mục `ros2 service info` trong tutorial. Các command `list`, `type`, `find`, `interface show` và `call` vẫn cùng cú pháp.

## Kiến thức liên quan

- [[Service]]
- [[Service client]]
- [[Node]]
- [[Topic]]
- [[Action]]
- [[ros2 CLI]]

## Bước tiếp theo

- [[Tìm hiểu về parameter]]

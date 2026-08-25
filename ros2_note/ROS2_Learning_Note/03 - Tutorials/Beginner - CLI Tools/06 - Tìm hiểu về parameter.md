---
aliases:
  - Understanding parameters
  - Tìm hiểu về parameter
tags:
  - ros2
  - parameter
  - cli
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html
translation-status: complete
---

# Tìm hiểu về parameter

## Nguồn

- Lyrical: [Understanding parameters](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- Jazzy: [Understanding parameters](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- Humble: [Understanding parameters](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)

## Mục tiêu

Lấy, đặt, lưu và nạp lại [[Parameter|parameter]] bằng command line.

## Điều kiện tiên quyết

- Source ROS 2 trong mỗi terminal mới.
- Cài và chạy `turtlesim` theo [[Sử dụng turtlesim, ros2 và rqt]].

## Nội dung

Parameter là giá trị cấu hình của [[Node|node]]. Mỗi node có tập parameter riêng, có thể là integer, float, boolean, string hoặc list.

### Khởi động turtlesim

```console
$ ros2 run turtlesim turtlesim_node
```

```console
$ ros2 run turtlesim turtle_teleop_key
```

### Liệt kê và đọc parameter

```console
$ ros2 param list
/teleop_turtle:
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  scale_angular
  scale_linear
  use_sim_time
/turtlesim:
  background_b
  background_g
  background_r
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  use_sim_time
```

`/turtlesim` có parameter RGB cho màu nền; mọi node đều có `use_sim_time`. Cú pháp đọc type và giá trị hiện tại:

```console
$ ros2 param get <node_name> <parameter_name>
```

```console
$ ros2 param get /turtlesim background_g
Integer value is: 86
```

Trong Lyrical, có thể bỏ `<node_name>` để truy vấn cùng một parameter trên mọi node:

```console
$ ros2 param get <parameter_name>
```

```console
$ ros2 param get use_sim_time
```

### Đặt parameter lúc runtime

```console
$ ros2 param set <node_name> <parameter_name> <value>
```

```console
$ ros2 param set /turtlesim background_r 150
Set parameter successful
```

Màu nền turtlesim đổi trong phiên hiện tại. `set` không lưu vĩnh viễn.

### Lưu ra YAML và nạp vào node đang chạy

```console
$ ros2 param dump <node_name>
```

```console
$ ros2 param dump /turtlesim > turtlesim.yaml
```

Tệp `turtlesim.yaml` có schema sau:

```yaml
/turtlesim:
  ros__parameters:
    background_b: 255
    background_g: 86
    background_r: 150
    qos_overrides:
      /parameter_events:
        publisher:
          depth: 1000
          durability: volatile
          history: keep_last
          reliability: reliable
    use_sim_time: false
```

Nạp một file vào node đang chạy:

```console
$ ros2 param load <node_name> <parameter_file>
```

```console
$ ros2 param load /turtlesim turtlesim.yaml
Set parameter background_b successful
Set parameter background_g successful
Set parameter background_r successful
Set parameter qos_overrides./parameter_events.publisher.depth failed: parameter 'qos_overrides./parameter_events.publisher.depth' cannot be set because it is read-only
Set parameter qos_overrides./parameter_events.publisher.durability failed: parameter 'qos_overrides./parameter_events.publisher.durability' cannot be set because it is read-only
Set parameter qos_overrides./parameter_events.publisher.history failed: parameter 'qos_overrides./parameter_events.publisher.history' cannot be set because it is read-only
Set parameter qos_overrides./parameter_events.publisher.reliability failed: parameter 'qos_overrides./parameter_events.publisher.reliability' cannot be set because it is read-only
Set parameter use_sim_time successful
```

Read-only parameter chỉ sửa được lúc startup, nên các `qos_overrides` báo lỗi khi `load` vào node đang chạy.

### Dùng parameter file khi khởi động node

```console
$ ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

Dừng turtlesim đang chạy rồi dùng file đã lưu:

```console
$ ros2 run turtlesim turtlesim_node --ros-args --params-file turtlesim.yaml
```

Khi tệp parameter được dùng lúc startup, gồm cả read-only parameter, các giá trị đều được cập nhật.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Không còn ví dụ giải thích namespace parameter phân cách bằng dấu chấm, cũng không có cú pháp `ros2 param get <parameter_name>` không chỉ rõ node. `list`, `get` có node, `set`, `dump`, `load` và `--params-file` giữ nguyên.

> [!warning] ROS 2 Humble
> Có cùng khác biệt với Jazzy; các command và YAML parameter-file chính vẫn giống Lyrical.

## Kiến thức liên quan

- [[Parameter]]
- [[Node]]
- [[Service]]
- [[ros2 CLI]]

## Bước tiếp theo

- [[Tìm hiểu về action]]

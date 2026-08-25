---
aliases:
  - Using turtlesim, ros2, and rqt
tags:
  - ros2
  - turtlesim
  - rqt
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
translation-status: complete
---

# Sử dụng turtlesim, ros2 và rqt

## Nguồn

- Lyrical: [Using turtlesim, ros2, and rqt](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)
- Jazzy: [Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)
- Humble: [Using turtlesim, ros2, and rqt](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)

## Mục tiêu

Cài và dùng [[turtlesim]], [[ros2 CLI]] và [[rqt]] để làm quen trực quan với node, topic, service và action.

## Điều kiện tiên quyết

- Hoàn thành [[Cấu hình môi trường ROS 2]].
- Source setup file ROS 2 trong mọi terminal mới dùng ở bên dưới.

## Nội dung

`turtlesim` là simulator nhẹ để học ROS 2. `ros2` là công cụ CLI quản lý, introspect và tương tác với hệ ROS 2; `rqt` là GUI làm các thao tác tương tự command line theo cách trực quan hơn.

### Cài và kiểm tra `turtlesim`

Trên Ubuntu, cài package của distribution đang dùng:

```console
$ sudo apt update
$ sudo apt install ros-{DISTRO}-turtlesim
```

Lyrical cũng ghi command RHEL:

```console
$ sudo dnf install ros-{DISTRO}-turtlesim
```

Trên macOS và Windows, archive ROS 2 đã cài cần chứa repository `ros_tutorials`. Kiểm tra các executable của package:

```console
$ ros2 pkg executables turtlesim
turtlesim draw_square
turtlesim mimic
turtlesim turtle_teleop_key
turtlesim turtlesim_node
```

### Khởi chạy và điều khiển turtle

Trong terminal thứ nhất:

```console
$ ros2 run turtlesim turtlesim_node
[INFO] [turtlesim]: Starting turtlesim with node name /turtlesim
[INFO] [turtlesim]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]
```

Một cửa sổ simulator xuất hiện cùng `turtle1`. Mở terminal mới, source ROS 2, rồi chạy node điều khiển:

![Cửa sổ turtlesim hiển thị turtle1 ở trung tâm vùng mô phỏng](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/turtlesim.png)

*Nguồn ảnh: [turtlesim.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/images/turtlesim.png).*

```console
$ ros2 run turtlesim turtle_teleop_key
```

Đặt focus ở terminal `turtle_teleop_key`, dùng các phím mũi tên để di chuyển turtle. Mỗi lần nhấn chỉ di chuyển ngắn rồi dừng; đường đi được vẽ bằng pen. Có ba cửa sổ cần dùng: terminal `turtlesim_node`, terminal `turtle_teleop_key` và cửa sổ simulator.

Để xem thành phần đang có trong ROS graph, dùng các command sau:

```console
$ ros2 node list
$ ros2 topic list
$ ros2 service list
$ ros2 action list
```

### Cài và mở `rqt`

Trên Ubuntu:

```console
$ sudo apt update
$ sudo apt install ros-{DISTRO}-rqt ros-{DISTRO}-rqt-common-plugins
```

Lyrical còn cung cấp command RHEL:

```console
$ sudo dnf install 'ros-{DISTRO}-rqt*'
```

Các archive chuẩn macOS và Windows chứa sẵn `rqt` cùng plugin. Khởi chạy:

```console
$ rqt
```

Lần đầu cửa sổ có thể trống. Chọn **Plugins** > **Services** > **Service Caller**. Nếu menu **Services** chưa xuất hiện, đóng `rqt` và chạy:

```console
$ rqt --force-discover
```

![Cửa sổ rqt Service Caller với danh sách Service và nút refresh](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/rqt-service-caller.png)

*Nguồn ảnh: [rqt.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/images/rqt.png).*

Trong Service Caller, nhấn nút refresh cạnh danh sách **Service**, rồi chọn `/spawn`.

### Tạo turtle thứ hai và đổi pen

Trong Service Caller của `/spawn`, double-click vào cặp nháy đơn trong cột **Expression**; nhập tên duy nhất, ví dụ `turtle2`, cho trường `name` kiểu `string`. Nhập tọa độ hợp lệ như `x = 1.0` và `y = 1.0`, sau đó nhấn **Call**. Turtle mới xuất hiện và danh sách service có `/turtle2/...` cùng `/turtle1/...`.

Nếu đặt lại tên đang tồn tại, terminal `turtlesim_node` báo:

```console
[ERROR] [turtlesim]: A turtle named [turtle1] already exists
```

Chọn service `/set_pen` để chỉnh pen của `turtle1`. `r`, `g`, `b` nhận giá trị từ 0 đến 255 và `width` là độ dày nét. Đặt `r` thành `255`, `width` thành `5`, rồi nhấn **Call**; điều khiển lại `turtle1` để quan sát nét đỏ.

### Remapping cho `turtle2`

`turtle2` chưa có teleop node. Mở terminal mới, source ROS 2, rồi remap topic `cmd_vel` và action `rotate_absolute` của teleop node:

```console
$ ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel --remap turtle1/rotate_absolute:=turtle2/rotate_absolute
```

Terminal này điều khiển `turtle2`; terminal teleop ban đầu vẫn điều khiển `turtle1` khi đang được focus.

### Đóng ứng dụng

Để dừng simulator, nhập `Ctrl + C` trong terminal `turtlesim_node` và `q` trong từng terminal `turtle_teleop_key`.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Các executable, command runtime, thao tác `rqt`, remapping và cách đóng ứng dụng giống Lyrical. Jazzy ghi nhóm cài `turtlesim` là Linux (với `apt`) thay vì tách Ubuntu/RHEL; phần `rqt` vẫn có command RHEL.

> [!warning] ROS 2 Humble
> Thao tác runtime và GUI giống Lyrical. Bảng installation trong Humble không liệt kê command RHEL cho `turtlesim` hoặc `rqt`; chỉ dùng command package mà tài liệu Humble của platform bạn nêu rõ.

## Kiến thức liên quan

- [[turtlesim]]
- [[ros2 CLI]]
- [[rqt]]
- [[Node]]
- [[Topic]]
- [[Service]]
- [[Action]]

## Bước tiếp theo

- [[Tìm hiểu về node]]

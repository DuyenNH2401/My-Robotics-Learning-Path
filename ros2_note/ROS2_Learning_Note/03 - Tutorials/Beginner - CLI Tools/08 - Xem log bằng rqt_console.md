---
aliases:
  - Using rqt_console to view logs
  - rqt_console
tags: [ros2, rqt, logging, cli]
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
translation-status: complete
---

# Xem log bằng rqt_console

## Nguồn

- Lyrical: [Using `rqt_console` to view logs](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html)
- Jazzy: [Using `rqt_console` to view logs](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html)
- Humble: [Using `rqt_console` to view logs](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html)

## Mục tiêu

Dùng [[rqt_console]] để introspect [[Logging|log message]].

## Điều kiện tiên quyết

- Hoàn thành [[Sử dụng turtlesim, ros2 và rqt]] và source ROS 2 trong từng terminal mới.
- Đã cài `rqt_console` và `turtlesim`.

## Nội dung

`rqt_console` là GUI thu thập log theo thời gian để xem có tổ chức hơn, lọc, lưu và nạp lại file đã lưu. [[Node|Node]] dùng log để thông báo sự kiện và trạng thái, thường nhằm cung cấp thông tin cho người dùng.

### Khởi động `rqt_console`

```console
$ ros2 run rqt_console rqt_console
```

![Cửa sổ rqt_console: vùng log phía trên, bộ lọc severity ở giữa và bộ lọc highlight phía dưới](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/rqt-console.png)

*Nguồn ảnh: [console.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/images/console.png).*

Vùng đầu hiển thị log của hệ thống. Vùng giữa loại trừ các severity level; nút dấu cộng bên phải thêm bộ lọc loại trừ. Vùng dưới highlight message chứa chuỗi nhập vào và cũng cho phép thêm bộ lọc.

Mở terminal mới và chạy:

```console
$ ros2 run turtlesim turtlesim_node
```

### Tạo message để quan sát

Cho turtle liên tục đâm tường bằng topic sau:

```console
$ ros2 topic pub -r 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}"
```

`rqt_console` sẽ lặp lại cùng message severity `Warn`. Nhấn `Ctrl+C` ở terminal đang chạy `ros2 topic pub` để dừng.

![rqt_console hiển thị các message Warn lặp lại khi turtle đâm tường](../../05%20-%20Tài%20nguyên/Hình%20ảnh/Beginner%20CLI/rqt-console-warn.png)

*Nguồn ảnh: [warn.png — ROS 2 Lyrical documentation](https://raw.githubusercontent.com/ros2/ros2_documentation/lyrical/source/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/images/warn.png).*

### Logger level

Severity theo thứ tự từ cao xuống thấp là `Fatal`, `Error`, `Warn`, `Info`, `Debug`. Không có chuẩn tuyệt đối, nhưng:

- `Fatal`: hệ thống sắp kết thúc để tự bảo vệ.
- `Error`: lỗi nghiêm trọng ngăn hoạt động đúng, nhưng không nhất thiết gây hư hại.
- `Warn`: hoạt động bất thường hoặc kết quả chưa lý tưởng, có thể là dấu hiệu vấn đề sâu hơn nhưng chưa làm hỏng chức năng.
- `Info`: cập nhật sự kiện/trạng thái để xác nhận trực quan rằng hệ thống chạy như mong đợi.
- `Debug`: chi tiết từng bước thực thi.

Mức mặc định là `Info`: chỉ thấy mức mặc định và các mức nghiêm trọng hơn; vì thế bình thường chỉ `Debug` bị ẩn. Ví dụ, mặc định `Warn` chỉ hiện `Warn`, `Error`, `Fatal`. Đặt mức mặc định khi khởi động `/turtlesim`:

```console
$ ros2 run turtlesim turtlesim_node --ros-args --log-level WARN
```

Các message `Info` ban đầu không còn xuất hiện vì chúng có ưu tiên thấp hơn `Warn`.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Nội dung, command, GUI, thứ tự level và hành vi giống Lyrical.

> [!warning] ROS 2 Humble
> Nội dung, command, GUI, thứ tự level và hành vi giống Lyrical.

## Kiến thức liên quan

- [[Logging]]
- [[rqt_console]]
- [[Introspection]]
- [[Node]]
- [[Topic]]

## Bước tiếp theo

- [[Khởi chạy nhiều node]]

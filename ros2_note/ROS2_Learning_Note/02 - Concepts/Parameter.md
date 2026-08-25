---
aliases:
  - parameter
tags:
  - ros2
  - concept
  - parameter
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Concepts/Basic/About-Parameters.html
  jazzy: https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html
  humble: https://docs.ros.org/en/humble/Concepts/Basic/About-Parameters.html
translation-status: complete
---

# Parameter

[[Parameter|Parameter]] là giá trị cấu hình (setting) của một [[Node|node]]. Mỗi node tự duy trì tập parameter của mình; giá trị có thể là integer, float, boolean, string hoặc list. Parameter có thể được xem và, nếu node cho phép, cấu hình lúc runtime; một số parameter là read-only và chỉ đặt được khi khởi động node.

Giá trị đặt bằng `ros2 param set` chỉ áp dụng cho phiên hiện tại. Có thể lưu vào YAML bằng `ros2 param dump`, nạp lại vào node đang chạy bằng `ros2 param load`, hoặc truyền file parameter khi launch node.

## Thực hành

- [[Tìm hiểu về parameter]] dùng `ros2 param` với `turtlesim`.

## Liên quan

- [[Node]]
- [[Service]]

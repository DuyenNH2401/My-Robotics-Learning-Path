---
aliases:
  - node
tags:
  - ros2
  - concept
  - node
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Concepts/Basic/About-Nodes.html
  jazzy: https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html
  humble: https://docs.ros.org/en/humble/Concepts/Basic/About-Nodes.html
translation-status: complete
---

# Node

Node là thành phần cơ bản của [[ROS graph]], chịu trách nhiệm cho một mục đích mô-đun, chẳng hạn điều khiển motor hoặc publish dữ liệu sensor. Nhiều node phối hợp tạo thành hệ robot; cách tách này giúp thay thế, kiểm thử và tái sử dụng từng phần.

Một node gửi hoặc nhận dữ liệu qua [[Topic|topic]], service, action và parameter. Một executable (program C++ hoặc Python) có thể chứa một hay nhiều node, vì vậy tên executable không nhất thiết là tên node đang chạy.

## Thực hành

- [[Tìm hiểu về node]] dùng `ros2 node list`, remapping và `ros2 node info` để quan sát node.
- [[Tìm hiểu về topic]] quan sát kết nối node qua topic.

## Liên quan

- [[ROS graph]]
- [[Topic]]
- [[Publisher]]
- [[Subscriber]]

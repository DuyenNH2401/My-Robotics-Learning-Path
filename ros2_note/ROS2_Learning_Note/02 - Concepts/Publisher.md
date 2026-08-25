---
aliases:
  - publisher
tags:
  - ros2
  - concept
  - publisher
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Concepts/Basic/Interfaces-Topics-Services-Actions.html
  jazzy: https://docs.ros.org/en/jazzy/Concepts/Basic/Interfaces-Topics-Services-Actions.html
  humble: https://docs.ros.org/en/humble/Concepts/Basic/Interfaces-Topics-Services-Actions.html
translation-status: complete
---

# Publisher

Publisher là endpoint của một [[Node|node]] gửi message lên một [[Topic|topic]]. Publisher không xác định node nào sẽ nhận message; mọi [[Subscriber|subscriber]] tương thích với topic có thể nhận luồng dữ liệu. Quan hệ tách rời này cho phép nhiều bên tiêu thụ cùng một dữ liệu mà không sửa publisher.

## Thực hành

- [[Tìm hiểu về topic]] cho thấy `/teleop_turtle` publish `Twist` lên `/turtle1/cmd_vel`.

## Liên quan

- [[Topic]]
- [[Subscriber]]
- [[ROS graph]]

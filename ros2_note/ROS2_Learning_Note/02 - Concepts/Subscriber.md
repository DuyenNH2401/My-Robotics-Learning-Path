---
aliases:
  - subscriber
tags:
  - ros2
  - concept
  - subscriber
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

# Subscriber

Subscriber là endpoint của một [[Node|node]] nhận message từ một [[Topic|topic]]. Subscriber nhận dữ liệu khi có publisher và type message tương thích, nhưng không điều khiển publisher hay yêu cầu phản hồi. Một topic có thể có nhiều subscriber độc lập.

## Thực hành

- [[Tìm hiểu về topic]] dùng `ros2 topic echo` để tạo subscriber quan sát message.

## Liên quan

- [[Topic]]
- [[Publisher]]
- [[ROS graph]]

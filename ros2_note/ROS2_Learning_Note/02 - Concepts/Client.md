---
aliases:
  - service client
  - action client
  - client
tags:
  - ros2
  - concept
  - client
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

# Client

Trong ROS 2, từ *client* phải luôn đi cùng ngữ cảnh giao tiếp cụ thể:

- **Service client** gửi request tới service server và nhận một response. Xem [[Service]].
- **Action client** gửi goal tới action server, nhận feedback liên tục và result cuối cùng; nó cũng có thể yêu cầu cancel goal. Xem [[Action]].

Vì vậy, khi mô tả endpoint cụ thể, dùng [[Client|service client]] hoặc [[Client|action client]], không dùng từ `client` mơ hồ.

## Liên quan

- [[Service]]
- [[Action]]
- [[Node]]

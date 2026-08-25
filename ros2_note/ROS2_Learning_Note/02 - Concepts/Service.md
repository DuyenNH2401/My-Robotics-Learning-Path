---
aliases:
  - service
tags:
  - ros2
  - concept
  - service
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

# Service

[[Service|Service]] là cách các [[Node|node]] trong [[ROS graph]] giao tiếp theo mẫu request/response: một [[Service client]] gửi request tới service server, server xử lý rồi trả về một response. Type service định nghĩa hai phần message, request ở trên và response ở dưới dấu `---`.

Không dùng service cho lời gọi liên tục hoặc tác vụ mất nhiều thời gian. [[Topic]] phù hợp với luồng dữ liệu liên tục; [[Action]] phù hợp với tác vụ dài vì có feedback và có thể cancel.

## Thực hành

- [[Tìm hiểu về service]] introspect và gọi service bằng `ros2 service`.

## Liên quan

- [[Service client]]
- [[Node]]
- [[Topic]]
- [[Action]]

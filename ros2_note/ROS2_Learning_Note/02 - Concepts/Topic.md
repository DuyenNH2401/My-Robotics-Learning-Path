---
aliases:
  - topic
tags:
  - ros2
  - concept
  - topic
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

# Topic

Topic là bus message trong [[ROS graph]] để các [[Node|node]] trao đổi luồng dữ liệu. Một topic có thể nối bất kỳ số [[Publisher|publisher]] và [[Subscriber|subscriber]] nào: one-to-many, many-to-one hoặc many-to-many. Các endpoint phải dùng type message tương thích.

Dùng topic khi dữ liệu được stream và bên nhận không cần trả lời ngay. Khác với service (request/response) và action (tác vụ dài có feedback và cancel), publisher không chờ phản hồi từ subscriber.

## Thực hành

- [[Tìm hiểu về topic]] dùng `ros2 topic` và `rqt_graph` để introspect topic.

## Liên quan

- [[Node]]
- [[Publisher]]
- [[Subscriber]]
- [[ROS graph]]

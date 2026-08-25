---
aliases:
  - action
  - action server
  - action client
tags:
  - ros2
  - concept
  - action
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

# Action

[[Action|Action]] dành cho tác vụ chạy lâu. Một action gồm goal, feedback và result; [[Action client]] gửi goal tới [[Action server]], server xác nhận goal, phát feedback đều đặn và trả result khi kết thúc. Client có thể cancel goal, và server có thể abort goal.

Action được xây trên topic và service. Không như [[Service]] chỉ trả một response, action có feedback và cancel; không như [[Topic]] là luồng một chiều, action có goal và result có liên hệ với từng goal. Ví dụ điển hình là điều hướng robot tới một vị trí.

## Thực hành

- [[Tìm hiểu về action]] introspect `/turtle1/rotate_absolute` và gửi goal.

## Liên quan

- [[Action client]]
- [[Action server]]
- [[Service]]
- [[Topic]]
- [[Node]]

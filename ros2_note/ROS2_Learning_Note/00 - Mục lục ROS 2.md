---
aliases:
  - ROS 2 Index
tags:
  - ros2
  - index
area: get-started
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/
  jazzy: https://docs.ros.org/en/jazzy/
  humble: https://docs.ros.org/en/humble/
translation-status: complete
---

# Mục lục ROS 2

Mục lục này theo dõi thứ tự học và trạng thái biên dịch của kho kiến thức ROS 2 tiếng Việt. Nội dung chính theo ROS 2 Lyrical; Jazzy và Humble dùng để đối chiếu khi cần.

## Get Started

- [x] [[Bước đầu với ROS - Lộ trình học]]

## Concepts

- [x] [[Node]]
- [x] [[Topic]]
- [x] [[Publisher]]
- [x] [[Subscriber]]
- [x] [[Service]]
- [x] [[Client]]
- [x] [[Action]]
- [x] [[Parameter]]

| Mẫu giao tiếp | Khi dùng | Đặc tính |
| --- | --- | --- |
| [[Topic]] | Luồng dữ liệu liên tục | Publisher/subscriber, một chiều |
| [[Service]] | Request/response ngắn | [[Service client]] nhận một response |
| [[Action]] | Tác vụ dài | [[Action client]], goal, feedback, result và cancel |

## Tutorials

### Beginner CLI Tools

- [x] [[Cấu hình môi trường ROS 2]]
- [x] [[Sử dụng turtlesim, ros2 và rqt]]
- [x] [[Tìm hiểu về node]]
- [x] [[Tìm hiểu về topic]]
- [x] [[Tìm hiểu về service]]
- [x] [[Tìm hiểu về parameter]]
- [x] [[Tìm hiểu về action]]
- [ ] [[Xem log bằng rqt_console]]
- [ ] [[Khởi chạy nhiều node]]
- [ ] [[Ghi và phát lại dữ liệu]]

## How-to Guides

Nhóm này sẽ được bổ sung sau khi hoàn thiện các tutorial trong phạm vi.

## Tài nguyên

- [[Quy ước thuật ngữ ROS 2]]
- [[Template - Tutorial ROS 2]]

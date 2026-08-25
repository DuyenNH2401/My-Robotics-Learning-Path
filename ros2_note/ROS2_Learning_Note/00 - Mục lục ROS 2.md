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
- [x] [[Logging]]
- [x] [[Launch file]]
- [x] [[rosbag]]

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
- [x] [[Xem log bằng rqt_console]]
- [x] [[Khởi chạy nhiều node]]
- [x] [[Ghi và phát lại dữ liệu]]

## How-to Guides

Nhóm này sẽ được bổ sung sau khi hoàn thiện các tutorial trong phạm vi.

## Planned notes

Các wikilink sau là khái niệm hoặc công cụ được dùng trong ghi chú hiện có; chúng được giữ làm mục tiêu điều hướng cho các plan tiếp theo.

- [[Client library]]
- [[Introspection]]
- [[Message]]
- [[Quality of Service]]
- [[ROS]]
- [[ROS 2 distribution]]
- [[ROS graph]]
- [[ROS Interface]]
- [[ros2 CLI]]
- [[rqt]]
- [[turtlesim]]
- [[Workspace]]

## Tài nguyên

- [[Quy ước thuật ngữ ROS 2]]
- [[Template - Tutorial ROS 2]]

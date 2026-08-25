---
aliases:
  - First steps with ROS
  - Lộ trình nhập môn ROS
tags:
  - ros2
area: get-started
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/First-Steps.html
  jazzy: https://docs.ros.org/en/jazzy/First-Steps.html
  humble: https://docs.ros.org/en/humble/First-Steps.html
translation-status: complete
---

# Bước đầu với ROS — Lộ trình học

> [!info] Nguồn
> Nội dung được biên dịch và biên tập từ [First steps with ROS — learning path](https://docs.ros.org/en/lyrical/First-Steps.html) trong tài liệu ROS 2 Lyrical chính thức.

[[ROS|ROS (Robot Operating System)]] là một hệ sinh thái mã nguồn mở cung cấp framework, công cụ và thư viện để xây dựng, triển khai, vận hành và bảo trì các ứng dụng robot. Note này giới thiệu một chuỗi bài viết và hoạt động thực hành nhằm làm quen với những khái niệm chính của ROS. Sau khi hoàn thành lộ trình, bạn sẽ có kiến thức nền tảng cần thiết để bắt đầu phát triển ứng dụng với ROS.

## Nội dung

- [[#Tóm tắt]]
- [[#Điều kiện tiên quyết]]
- [[#Các bước thực hiện]]
  - [[#1. Tìm hiểu các khái niệm nền tảng của ROS]]
  - [[#2. Cài đặt ROS và turtlesim]]
  - [[#3. Làm quen với các thành phần giao tiếp chính]]
  - [[#4. Tìm hiểu introspection thông qua log]]
  - [[#5. Tìm hiểu cách sử dụng launch file]]
  - [[#6. Ghi và phát lại dữ liệu]]
- [[#Bước tiếp theo]]

## Tóm tắt

ROS framework đóng vai trò như một hệ thống “đường ống”, cho phép các bộ phận khác nhau của robot giao tiếp với nhau. Framework này bao gồm cơ chế truyền [[Message|message]], các interface tiêu chuẩn, cùng khả năng hỗ trợ nhiều ngôn ngữ lập trình và nền tảng khác nhau.

Trước khi sử dụng ROS để phát triển hoặc bảo trì ứng dụng, bạn cần hiểu những khái niệm nền tảng của framework. Công cụ [[turtlesim]] và các tutorial trên trang tài liệu ROS 2 sẽ giúp bạn nhanh chóng làm quen với chúng.

## Điều kiện tiên quyết

Không có. Các bước trong note này sẽ hướng dẫn bạn tải xuống và cài đặt mọi thành phần cần thiết để học kiến thức ROS cơ bản.

## Các bước thực hiện

### 1. Tìm hiểu các khái niệm nền tảng của ROS

Trước tiên, hãy tìm hiểu các thành phần cơ bản của ROS framework:

- [Giới thiệu về ROS](https://docs.ros.org/en/lyrical/About-ROS.html)
- [[Node|Node]] — [tài liệu chính thức](https://docs.ros.org/en/lyrical/Concepts/Basic/About-Nodes.html)
- [[ROS Interface|Interface]] gồm [[Topic|topic]], [[Service|service]] và [[Action|action]] — [tài liệu chính thức](https://docs.ros.org/en/lyrical/Concepts/Basic/Interfaces-Topics-Services-Actions.html)
- [[Parameter|Parameter]] — [tài liệu chính thức](https://docs.ros.org/en/lyrical/Concepts/Basic/About-Parameters.html)

### 2. Cài đặt ROS và turtlesim

Bản cài đặt ROS cung cấp các package thiết yếu để làm việc với ROS. Nếu đã quen với Linux, nền tảng được khuyến nghị là Ubuntu và cài đặt bằng các package `deb`. Nếu chưa quen với Linux, Windows với các file binary là một lựa chọn thay thế phù hợp.

- [Các phương án cài đặt ROS 2](https://docs.ros.org/en/lyrical/Installation.html)

[[turtlesim]] là một công cụ mô phỏng 2D gọn nhẹ dành cho người mới. Công cụ này giúp bạn học các khái niệm cốt lõi của ROS trong một môi trường trực quan và đơn giản. Trước khi chạy tutorial, hãy hoàn thành [[Cấu hình môi trường ROS 2]].

- [[Sử dụng turtlesim, ros2 và rqt|Cài đặt và thiết lập turtlesim]]

### 3. Làm quen với các thành phần giao tiếp chính

Sử dụng [[turtlesim]] để làm quen với những thành phần giao tiếp chính và thử cơ chế truyền message trong ROS framework. Hoàn thành lần lượt các tutorial sau:

1. [[Tìm hiểu về node]] — [Understanding nodes](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
2. [[Tìm hiểu về topic]] — [Understanding topics](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
3. [[Tìm hiểu về service]] — [Understanding services](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html)
4. [[Tìm hiểu về parameter]] — [Understanding parameters](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
5. [[Tìm hiểu về action]] — [Understanding actions](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)

### 4. Tìm hiểu introspection thông qua log

[[Introspection]] cho phép bạn quan sát thông tin về cách một hệ thống đang hoạt động. [[Node|Node]] sử dụng [[Logging|log]] để xuất các message về sự kiện và trạng thái theo nhiều cách khác nhau.

Để thực hành introspection thông qua log, hãy hoàn thành tutorial về `rqt_console`:

- [[Xem log bằng rqt_console]] — [tài liệu chính thức](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html)

### 5. Tìm hiểu cách sử dụng launch file

[[Launch file|Launch file]] cho phép khởi chạy và cấu hình đồng thời nhiều process chứa các ROS [[Node|node]]. Nhờ đó, bạn không cần mở nhiều terminal rồi nhập lại thông tin cấu hình cho từng node.

Hãy hoàn thành tutorial sau:

- [[Khởi chạy nhiều node]] — [tài liệu chính thức](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)

### 6. Ghi và phát lại dữ liệu

Trong một số trường hợp, việc phát lại dữ liệu rất hữu ích để:

- tái tạo kết quả của các bài test và thí nghiệm;
- debug hành vi của robot;
- chia sẻ công việc với người khác.

Hãy hoàn thành tutorial về [[rosbag|ghi và phát lại dữ liệu]]:

- [[Ghi và phát lại dữ liệu]] — [Recording and playing back data](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

## Bước tiếp theo

Để hoàn thiện kiến thức về ROS framework, bạn nên tiếp tục làm quen với [[Client library|client library]] của ROS:

- [Beginner: Client libraries](https://docs.ros.org/en/lyrical/Tutorials/Beginner-Client-Libraries.html)

## Các khái niệm liên quan

- [[ROS]]
- [[Node]]
- [[Message]]
- [[ROS Interface]]
- [[Topic]]
- [[Service]]
- [[Action]]
- [[Parameter]]
- [[Introspection]]
- [[Logging]]
- [[Launch file]]
- [[rosbag]]
- [[Client library]]
- [[turtlesim]]

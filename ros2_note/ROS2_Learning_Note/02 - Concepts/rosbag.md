---
aliases: [ros2 bag, bag file]
tags: [ros2, concept, rosbag]
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
translation-status: complete
---

# rosbag

`ros2 bag` ghi dữ liệu đi qua [[Topic|topic]], [[Service|service]] và [[Action|action]] vào database để phát lại và kiểm tra sau này. Đây là công cụ hữu ích để debug, tái tạo test/thí nghiệm và chia sẻ dữ liệu làm việc.

Playback tái tạo dữ liệu đã ghi, không tự đảm bảo tái hiện hoàn toàn hệ thống: node đang chạy, timing, state và cấu hình phải tương thích. Ví dụ, `turtlesim` có thể không đi lại đúng 100% do nhạy với khác biệt nhỏ của timing.

## Thực hành

- [[Ghi và phát lại dữ liệu]] ghi, `info` và phát lại dữ liệu topic, service và action.

## Liên quan

- [[Topic]]
- [[Service]]
- [[Action]]
- [[Introspection]]

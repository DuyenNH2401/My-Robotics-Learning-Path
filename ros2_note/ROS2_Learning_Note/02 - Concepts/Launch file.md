---
aliases: [launch, ROS 2 Launch]
tags: [ros2, concept, launch]
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
translation-status: complete
---

# Launch file

Launch file mô tả cách khởi động và cấu hình đồng thời một số executable chứa ROS 2 [[Node|node]]. Chạy một file với `ros2 launch` sẽ khởi động toàn hệ thống, gồm node và cấu hình, thay cho nhiều terminal và các command lặp lại.

Launch file có thể viết bằng Python, XML hoặc YAML. Note này chỉ giới thiệu mục đích và cách chạy file có sẵn; việc tự tạo launch file thuộc tutorial Client Libraries/Launch chuyên sâu hơn.

## Thực hành

- [[Khởi chạy nhiều node]] chạy `ros2 launch turtlesim multisim.launch.py` để khởi động hai turtlesim node.

## Liên quan

- [[Node]]
- [[turtlesim]]

---
tags:
  - ros2
  - launch
  - launch-files
  - python
  - cli
  - beginner
created: 2026-08-25
aliases:
  - Khởi chạy Nodes với Launch Files
  - Launching nodes
---

# 🚀 Khởi chạy Nodes với Launch Files (Launching Nodes)

> [!INFO] **Mục tiêu bài học**
> Sử dụng công cụ dòng lệnh `ros2 launch` để khởi động đồng thời nhiều [[03 - Understanding Nodes|Node]] và tự động hóa cấu hình hệ thống robot chỉ bằng một lệnh duy nhất.
> - **Cấp độ:** Beginner
> - **Thời lượng ước tính:** 5 phút
> - **Bài trước:** [[08 - Using RQt Console|Quản lý Log với RQt Console]]
> - **Bài tiếp theo:** [[10 - Recording and Playing Back Data|Ghi và Phát lại dữ liệu với ros2 bag]]

---

## 📖 Bối cảnh (Background)

Trong các bài học trước, bạn phải mở từng terminal riêng lẻ cho mỗi node (`turtlesim_node`, `turtle_teleop_key`, `rqt`, v.v.). Khi phát triển hệ thống robot thực tế với hàng chục node chạy đồng thời (driver cảm biến, điều hướng, thị giác máy tính...), việc mở hàng chục terminal và nhập lại từng dòng cấu hình là bất khả thi.

**Launch File (Tệp tin khởi chạy)** ra đời để giải quyết vấn đề này:
- Cho phép định nghĩa danh sách các node cần chạy, namespace, tham số (`parameters`), và quy tắc ánh xạ (`remapping`).
- Khởi động và cấu hình toàn bộ hệ thống robot cùng một lúc với một lệnh đơn giản: `ros2 launch`.

---

## 🛠️ Thực hành chạy Launch File (Tasks)

### 1. Khởi chạy đồng thời 2 cửa sổ Turtlesim
Chạy lệnh sau trên terminal:

```bash
ros2 launch turtlesim multisim.launch.py
```

Lệnh này sẽ thực thi tệp tin launch `multisim.launch.py` có trong package `turtlesim`.

Hai cửa sổ mô phỏng Turtlesim độc lập sẽ xuất hiện trên màn hình!

---

### 2. Cấu trúc một Launch File viết bằng Python
Dưới đây là mã nguồn bên trong file `multisim.launch.py`:

```python
from launch import LaunchDescription
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        # Khởi chạy node thứ 1 trong namespace 'turtlesim1'
        launch_ros.actions.Node(
            namespace='turtlesim1',
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),
        # Khởi chạy node thứ 2 trong namespace 'turtlesim2'
        launch_ros.actions.Node(
            namespace='turtlesim2',
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),
    ])
```

> [!NOTE] **Các định dạng Launch File hỗ trợ trong ROS 2:**
> 1. **Python (`.launch.py`):** Phổ biến nhất, linh hoạt, hỗ trợ xử lý logic điều kiện phức tạp.
> 2. **XML (`.launch.xml`):** Cú pháp thẻ ngắn gọn, trực quan, quen thuộc với người dùng ROS 1.
> 3. **YAML (`.launch.yaml`):** Cú pháp phân cấp sạch sẽ, dễ đọc cấu hình tham số.

---

### 3. Điều khiển các Node độc lập
Vì hai node được gán hai **namespace** khác nhau (`/turtlesim1` và `/turtlesim2`), các topic của chúng cũng được tách biệt hoàn toàn:

Mở 2 terminal mới để điều khiển rùa 1 và rùa 2 quay theo các hướng ngược nhau:

```bash
# Terminal điều khiển rùa 1
ros2 topic pub /turtlesim1/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"

# Terminal điều khiển rùa 2
ros2 topic pub /turtlesim2/turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -1.8}}"
```

---

## 📌 Tóm tắt (Summary)
- `ros2 launch` là công cụ chuẩn mực trong ROS 2 để quản lý vòng đời và vận hành hệ thống nhiều node.
- Việc sử dụng `namespace` trong launch file giúp nhân bản (duplicate) và quản lý nhiều robot cùng loại một cách dễ dàng mà không sợ trùng tên topic hay service.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[08 - Using RQt Console|Quản lý Log với RQt Console]]
- ➡️ Bài tiếp theo: [[10 - Recording and Playing Back Data|Ghi và Phát lại dữ liệu với ros2 bag]]

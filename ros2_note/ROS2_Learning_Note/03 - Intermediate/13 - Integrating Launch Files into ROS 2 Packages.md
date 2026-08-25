---
tags:
  - ros2
  - launch
  - packaging
  - colcon
  - intermediate
created: 2026-08-25
aliases:
  - Tích hợp Launch File vào Package
  - Integrating launch files into ROS 2 packages
---

# 📦 Tích hợp Launch File vào ROS 2 Package (Integrating launch files into packages)

> [!INFO] **Mục tiêu bài học**
> Học cách tổ chức cấu trúc thư mục chuẩn cho các file launch bên trong một package, cấu hình `setup.py` (với Python) hoặc `CMakeLists.txt` (với C++) để `colcon` tự động cài đặt các file launch vào thư mục `share/`, cho phép gọi lệnh `ros2 launch <package_name> <launch_file>`.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 10 phút
> - **Bài trước:** [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]
> - **Bài tiếp theo:** [[14 - Using Substitutions in Launch Files|Sử dụng Substitutions trong Launch File]]

---

## 📖 Bối cảnh & Quy chuẩn (Conventions)

Theo quy ước chuẩn của cộng đồng ROS 2:
- Toàn bộ file launch của một package luôn được đặt trong thư mục con mang tên **`launch/`** ở cấp cao nhất của package đó.
- Để lệnh `ros2 launch <package_name> <file>` tìm thấy file sau khi build, hệ thống build (`colcon`) phải copy thư mục `launch/` vào đường dẫn `install/<package_name>/share/<package_name>/launch/`.

---

## 🛠️ Cấu hình cài đặt Launch File

### 1. Đối với Package Python (`ament_python`)

Cấu trúc thư mục:
```text
py_launch_example/
├── launch/
│   └── my_script_launch.py (hoặc .xml / .yaml)
├── package.xml
├── py_launch_example/
└── setup.py
```

Mở file `setup.py` và bổ sung cấu hình trong tham số `data_files`:
```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'py_launch_example'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # Bổ sung dòng này để cài đặt toàn bộ file trong thư mục launch
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    # ...
)
```

---

### 2. Đối với Package C++ (`ament_cmake`)

Cấu trúc thư mục:
```text
cpp_launch_example/
├── CMakeLists.txt
├── launch/
│   └── my_script_launch.py
├── package.xml
└── src/
```

Mở file `CMakeLists.txt` và thêm lệnh `install(DIRECTORY ...)` trước `ament_package()`:
```cmake
# Cài đặt thư mục launch vào share/<project_name>
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)
```

---

### 3. Cập nhật `package.xml`
Khai báo dependency thực thi tới gói `ros2launch`:

```xml
<exec_depend>ros2launch</exec_depend>
```

---

## 🚀 Biên dịch và Chạy thử nghiệm

```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select py_launch_example
source install/setup.bash

# Khởi chạy file launch thông qua tên package:
ros2 launch py_launch_example my_script_launch.xml
```

---

## 📌 Tóm tắt (Summary)
- Luôn đặt file launch trong thư mục `launch/`.
- Với Python dùng `glob('launch/*')` trong `setup.py`, với C++ dùng `install(DIRECTORY launch ...)` trong `CMakeLists.txt`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[12 - Creating a Launch File|Tạo Launch File chuyên sâu]]
- ➡️ Bài tiếp theo: [[14 - Using Substitutions in Launch Files|Sử dụng Substitutions trong Launch File]]

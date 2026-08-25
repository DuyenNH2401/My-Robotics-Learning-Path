---
tags:
  - ros2
  - launch
  - substitutions
  - launch-arguments
  - intermediate
created: 2026-08-25
aliases:
  - Sử dụng Substitutions trong Launch File
  - Using substitutions
---

# 🔄 Sử dụng Substitutions trong Launch File (Using Substitutions)

> [!INFO] **Mục tiêu bài học**
> Làm chủ **Substitutions (Biến thay thế động)** trong Launch File: tìm đường dẫn package (`find-pkg-share`), đọc biến môi trường (`env`), truyền và lấy giá trị tham số cấu hình (`var`), đánh giá biểu thức logic (`eval`, `equals`, `and`, `or`) để tạo các launch file tái sử dụng linh hoạt.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[13 - Integrating Launch Files into ROS 2 Packages|Tích hợp Launch File vào Package]]
> - **Bài tiếp theo:** [[15 - Using Event Handlers in Launch Files|Sử dụng Event Handlers trong Launch File]]

---

## 📖 Bối cảnh (Background)

Khi viết launch file, nhiều giá trị không thể gán cứng tại thời điểm viết mã mà chỉ có thể xác định khi hệ thống đang chạy (runtime) — ví dụ: đường dẫn cài đặt của package trên máy người dùng, tham số người dùng nhập từ terminal, hoặc biến môi trường hệ thống.

**Substitutions** là các biến đặc biệt chỉ được tính toán và giải mã giá trị thực tế tại thời điểm thực thi của launch description.

---

## 📚 Bảng tra cứu các Substitutions phổ biến

| Cú pháp XML / YAML | Class trong Python | Ý nghĩa / Chức năng |
| :--- | :--- | :--- |
| `$(find-pkg-share <pkg>)` | `FindPackageShare` | Trả về đường dẫn tuyệt đối đến thư mục `share/<pkg>` đã cài đặt. |
| `$(var <name>)` | `LaunchConfiguration` | Lấy giá trị của một biến/đối số launch argument. |
| `$(env <NAME> <default>)` | `EnvironmentVariable` | Đọc giá trị của biến môi trường hệ điều hành. |
| `$(eval '<python_expr>')` | `PythonExpression` | Tính toán giá trị của một biểu thức Python bất kỳ. |
| `$(equals A B)` | `EqualsSubstitution` | Trả về `true` nếu chuỗi A bằng B. |
| `$(not-equals A B)` | `NotEqualsSubstitution` | Trả về `true` nếu chuỗi A khác B. |
| `$(and A B)` | `AndSubstitution` | Phép toán Logic AND giữa 2 điều kiện boolean. |
| `$(or A B)` | `OrSubstitution` | Phép toán Logic OR giữa 2 điều kiện boolean. |

---

## 🛠️ Ví dụ thực hành lồng ghép Launch Files

### 1. File Launch con (`launch/example_substitutions_launch.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<launch>
  <!-- 1. Khai báo các đối số đầu vào (Launch Arguments) kèm giá trị mặc định -->
  <arg name="turtlesim_ns" default="turtlesim1" description="Namespace cua Turtlesim" />
  <arg name="use_provided_red" default="False" description="Co su dung mau do duoc cung cap khong" />
  <arg name="new_background_r" default="200" description="Gia tri mau do cho background" />

  <!-- 2. Sử dụng $(var turtlesim_ns) để gán namespace cho node -->
  <node pkg="turtlesim" namespace="$(var turtlesim_ns)" exec="turtlesim_node" name="sim" />
  
  <!-- 3. Gọi Service spawn với tham số thay thế động -->
  <executable cmd="ros2 service call $(var turtlesim_ns)/spawn turtlesim_msgs/srv/Spawn '{x: 5, y: 2, theta: 0.2}'" />
  
  <!-- 4. Thay đổi màu nền sau 2 giây nếu thỏa mãn điều kiện logic -->
  <timer period="2.0">
    <executable cmd="ros2 param set $(var turtlesim_ns)/sim background_r $(var new_background_r)"
      if="$(and $(equals $(var new_background_r) 200) $(var use_provided_red))" />
  </timer>
</launch>
```

---

### 2. File Launch cha gọi File con (`launch/example_main_launch.xml`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<launch>
  <let name="background_r" value="200" />

  <!-- Sử dụng $(find-pkg-share ...) để tìm chính xác file launch con -->
  <include file="$(find-pkg-share launch_tutorial)/launch/example_substitutions_launch.xml">
    <let name="turtlesim_ns" value="turtlesim2" />
    <let name="use_provided_red" value="True" />
    <let name="new_background_r" value="$(var background_r)" />
  </include>
</launch>
```

---

## 🚀 Truyền đối số linh hoạt từ dòng lệnh CLI

Kiểm tra danh sách các đối số mà file launch hỗ trợ:
```bash
ros2 launch launch_tutorial example_substitutions_launch.xml --show-args
```

Truyền giá trị tùy chỉnh trực tiếp lúc khởi chạy:
```bash
ros2 launch launch_tutorial example_substitutions_launch.xml \
  turtlesim_ns:='turtlesim3' \
  use_provided_red:='True' \
  new_background_r:=200
```

---

## 📌 Tóm tắt (Summary)
- Substitutions giúp bạn xây dựng các file launch tổng quát, có thể tái sử dụng cho nhiều robot hoặc môi trường khác nhau mà không cần sửa code.
- Sử dụng kết hợp `find-pkg-share`, `var`, `env` và các phép toán logic `if / unless`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[13 - Integrating Launch Files into ROS 2 Packages|Tích hợp Launch File vào Package]]
- ➡️ Bài tiếp theo: [[15 - Using Event Handlers in Launch Files|Sử dụng Event Handlers trong Launch File]]

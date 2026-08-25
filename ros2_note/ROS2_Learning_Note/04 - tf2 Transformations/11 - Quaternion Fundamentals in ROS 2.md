---
tags:
  - ros2
  - tf2
  - math
  - quaternion
  - rpy
  - euler-angles
  - intermediate
created: 2026-08-25
aliases:
  - Cơ bản về Quaternion trong ROS 2
  - Quaternion fundamentals
---

# 🧭 Cơ bản về Quaternion trong ROS 2 (Quaternion Fundamentals)

> [!INFO] **Mục tiêu bài học**
> Nắm vững biểu diễn toán học của **Quaternion** $(x, y, z, w)$ trong không gian 3D, khắc phục hiện tượng khóa khớp (*Gimbal Lock*), chuyển đổi qua lại giữa góc **Roll-Pitch-Yaw (RPY / Euler)** và Quaternion, thực hiện các phép nhân quay, đảo ngược (*Inverse*) và tính góc quay tương đối trong C++ và Python.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[10 - Time Travel with tf2 (C++)|Du hành Thời gian với tf2 (C++)]]
> - **Bài tiếp theo:** [[12 - Debugging tf2 Problems|Chẩn đoán và Debug lỗi tf2]]

---

## 📖 Bối cảnh (Background)

Trong không gian 3 chiều, có 3 cách biểu diễn hướng quay (Orientation):
1. **Góc Euler (Roll - Pitch - Yaw):** Dễ hình dung với trực giác con người, nhưng gặp lỗi toán học **Gimbal Lock** (mất 1 bậc tự do khi góc pitch đạt $\pm 90^\circ$).
2. **Ma trận quay ($3 \times 3$ Rotation Matrix):** Tốn bộ nhớ (9 phần tử) và khó chuẩn hóa.
3. **Quaternion (Bộ 4 số thực $x, y, z, w$):** Nhỏ gọn, tối ưu tính toán, triệt tiêu hoàn toàn Gimbal Lock và nội suy góc quay mượt mà (SLERP).

> [!IMPORTANT] **Quy ước Quaternion trong ROS 2:**
> Trong ROS 2, thành phần vô hướng **$w$ luôn nằm ở vị trí CUỐI CÙNG** trong bộ 4 số: $(x, y, z, w)$.  
> - **Identity Quaternion (Góc quay bằng 0):** $(0.0, 0.0, 0.0, 1.0)$.  
> - **Độ lớn chuẩn (Magnitude):** $\sqrt{x^2 + y^2 + z^2 + w^2} = 1.0$. Nếu sai khác 1, ROS 2 sẽ cảnh báo và bạn cần chuẩn hóa bằng hàm `q.normalize()`.

---

## 🔀 Kiểu dữ liệu và Chuyển đổi trong ROS 2

### 1. Trong C++ (`tf2_geometry_msgs`)

| Kiểu dữ liệu | Thư viện | Mục đích |
| :--- | :--- | :--- |
| `tf2::Quaternion` | `tf2/LinearMath/Quaternion.hpp` | Thực hiện các phép toán hình học, xoay, chuẩn hóa. |
| `geometry_msgs::msg::Quaternion` | `geometry_msgs/msg/quaternion.hpp` | Định dạng tin nhắn gửi qua ROS Topic/tf. |

```cpp
#include <tf2/LinearMath/Quaternion.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

// 1. Tạo tf2::Quaternion từ góc Roll, Pitch, Yaw (đơn vị: Radians)
tf2::Quaternion tf2_quat;
tf2_quat.setRPY(0.0, 0.0, 1.5707); // Quay 90 độ quanh trục Z

// 2. Chuyển đổi sang message ROS 2
geometry_msgs::msg::Quaternion msg_quat = tf2::toMsg(tf2_quat);

// 3. Chuyển đổi ngược lại từ message sang tf2::Quaternion
tf2::Quaternion tf2_quat_from_msg;
tf2::fromMsg(msg_quat, tf2_quat_from_msg);
```

---

### 2. Trong Python

Trong Python, ROS 2 dùng mảng/list chuẩn `[x, y, z, w]` tương thích với tin nhắn `geometry_msgs.msg.Quaternion`:

```python
from geometry_msgs.msg import Quaternion

quat_list = [0.0, 0.0, 0.7071, 0.7071]
msg_quat = Quaternion(x=quat_list[0], y=quat_list[1], z=quat_list[2], w=quat_list[3])
```

---

## ⚙️ 4 Phép toán Quaternion Thường Dùng Nhất

### 1. Chuyển đổi từ RPY sang Quaternion
Quy tắc: Luôn hình dung góc quay theo hệ trục cố định RPY (Roll quanh X, Pitch quanh Y, Yaw quanh Z) rồi chuyển đổi sang Quaternion:

```python
# python
q = quaternion_from_euler(roll, pitch, yaw)
```

---

### 2. Áp dụng phép quay (Nhân 2 Quaternion)
Muốn quay một tư thế $q_{\text{orig}}$ thêm một góc $q_{\text{rot}}$, ta thực hiện **nhân Quaternion**:
$$q_{\text{new}} = q_{\text{rot}} \times q_{\text{orig}}$$

> [!WARNING] **Thứ tự phép nhân:**
> Phép nhân Quaternion **không có tính giao hoán** ($A \times B \neq B \times A$). Góc quay mới $q_{\text{rot}}$ luôn phải được nhân vào bên TRÁI của tư thế ban đầu!

*Trong C++:*
```cpp
tf2::Quaternion q_orig, q_rot, q_new;
q_orig.setRPY(0.0, 0.0, 0.0);
q_rot.setRPY(3.14159, 0.0, 0.0); // Quay 180 độ quanh X

q_new = q_rot * q_orig;
q_new.normalize(); // Luôn chuẩn hóa sau khi nhân
```

---

### 3. Đảo ngược Quaternion (Quaternion Inversion)
Để quay ngược lại góc quay ban đầu, ta chỉ cần **đổi dấu 3 thành phần $x, y, z$** (giữ nguyên $w$):
$$q^{-1} = (-x, -y, -z, w)$$

---

### 4. Tính góc quay tương đối giữa 2 tư thế (Relative Rotation)
Giả sử robot có tư thế cũ $q_1$ và tư thế mới $q_2$. Góc quay tương đối $q_r$ được tính bằng:
$$q_2 = q_r \times q_1 \implies q_r = q_2 \times q_1^{-1}$$

---

## 📌 Tóm tắt (Summary)
- Quaternion giải quyết triệt để lỗi Gimbal Lock trong hệ thống robot 3D.
- Thứ tự thành phần trong ROS 2 là $(x, y, z, w)$ với $w$ ở cuối cùng.
- Luôn sử dụng `setRPY` khi khởi tạo và gọi `normalize()` khi tính toán nhân chuỗi quay.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[10 - Time Travel with tf2 (C++)|Du hành Thời gian với tf2 (C++)]]
- ➡️ Bài tiếp theo: [[12 - Debugging tf2 Problems|Chẩn đoán và Debug lỗi tf2]]

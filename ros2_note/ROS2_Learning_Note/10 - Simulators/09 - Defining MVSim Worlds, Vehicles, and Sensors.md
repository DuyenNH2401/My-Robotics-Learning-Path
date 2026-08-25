---
tags:
  - ros2
  - mvsim
  - world-definition
  - xml
  - dynamics
  - sensors
  - noise-models
  - elevation-map
  - advanced
created: 2026-08-25
aliases:
  - Định nghĩa Thế giới, Robot và Cảm biến trong MVSim
  - Defining worlds, robots, and sensors
---

# 🗺️ Định nghĩa Thế giới, Robot và Cảm biến trong MVSim (MVSim World XML)

> [!INFO] **Mục tiêu bài học**
> Học cách tự tạo file thế giới mô phỏng **`.world.xml`** trong MVSim: cấu hình động lực học bánh vi sai (**Differential**) và bẻ lái kiểu ô tô (**Ackermann**), nhúng các mô hình xe có sẵn (**TurtleBot3, Clearpath Jackal**), thiết lập mô hình nhiễu cảm biến thực tế (**IMU bias drift, Lidar noise**) và sinh địa hình tự động bằng **Bản đồ Độ cao (Elevation Maps)** & **Vòng lặp XML**.
> - **Cấp độ:** Advanced
> - **Thời lượng ước tính:** 30 phút
> - **Mục lục tổng quan:** [[ROS 2 Learning Path]]
> - **Bài trước:** [[08 - Getting Started with MVSim Simulator|Bắt đầu với Phần mềm Mô phỏng MVSim]]

---

## 📖 Cấu trúc Một File Thế giới MVSim Tối giản (`my_world.world.xml`)

```xml
<mvsim_world version="1.0">
  <!-- 1. Chu kỳ bước thời gian mô phỏng vật lý (5 mili-giây) -->
  <simul_timestep>5e-3</simul_timestep>

  <!-- 2. Cấu hình góc nhìn Camera GUI ban đầu -->
  <gui>
      <cam_distance>15</cam_distance>
  </gui>

  <!-- 3. Lưới sàn mặt đất -->
  <element class="ground_grid" />

  <!-- 4. Khai báo một Robot bánh vi sai -->
  <vehicle name="robot1">
    <init_pose>0 0 0</init_pose>  <!-- Tọa độ ban đầu: x y yaw(độ) -->

    <!-- Mô hình động lực học vi sai -->
    <dynamics class="differential">
        <l_wheel pos="0.0  0.5" mass="4.0" width="0.20" diameter="0.40" />
        <r_wheel pos="0.0 -0.5" mass="4.0" width="0.20" diameter="0.40" />
        <chassis mass="15.0" zmin="0.05" zmax="0.6" />
        
        <!-- Bộ điều khiển bám vận tốc Twist PID -->
        <controller class="twist_pid">
            <KP>4.15</KP> <KI>1.91</KI> <KD>0.0</KD>
            <max_torque>14.44</max_torque>
        </controller>
    </dynamics>
  </vehicle>
</mvsim_world>
```

Khởi chạy nhanh file này với:
```bash
mvsim launch my_world.world.xml
```

---

## 🏎️ Sử dụng Thư viện Xe & Cảm biến Định nghĩa sẵn (Predefined XMLs)

Thay vì phải tự khai báo từng thông số bánh xe, MVSim cung cấp sẵn thư viện phong phú:

```xml
<mvsim_world version="1.0">
  <simul_timestep>5e-3</simul_timestep>
  <element class="ground_grid" />

  <!-- 1. Nạp định nghĩa xe Jackal UGV 4 bánh vi sai -->
  <include file="$(ros2 pkg prefix mvsim)/share/mvsim/definitions/jackal.vehicle.xml"
           default_sensors="true" />

  <!-- 2. Thả xe vào vị trí x=2m, y=1m, xoay 90 độ -->
  <vehicle name="r1" class="jackal">
    <init_pose>2.0 1.0 90</init_pose>
  </vehicle>

  <!-- 3. Thêm tường gạch có cửa ra vào -->
  <element class="vertical_plane">
    <x0>-10</x0> <y0>-10</y0>
    <x1>-10</x1> <y1>10</y1>
    <z>0.0</z> <height>3.0</height>
    <thickness>0.2</thickness>
    <door>
      <position>0.5</position> <!-- Vị trí cửa ở giữa bức tường -->
      <width>1.2</width>       <!-- Rộng 1.2 mét -->
      <z_max>2.1</z_max>
      <name>main_door</name>
    </door>
  </element>
</mvsim_world>
```

---

## 📡 Cấu hình Mô hình Nhiễu Cảm biến Thực tế (Sensor Noise)

MVSim hỗ trợ mô phỏng nhiễu đo lường vật lý chính xác:

### 1. Cảm biến IMU với Độ trôi Lệch (Bias Drift):
```xml
<sensor class="imu" name="imu1">
  <pose>0 0 0.5 0 0 0</pose>
  <rate_hz>100</rate_hz>
  <!-- Nhiễu Con quay hồi chuyển Gyroscope -->
  <gyroscope_noise>
    <noise_std>1e-3</noise_std>
    <bias_initial_std>1e-4</bias_initial_std>
    <bias_drift>1e-6</bias_drift>
  </gyroscope_noise>
</sensor>
```

### 2. Cảm biến Lidar 2D / 3D:
```xml
<sensor class="laser" name="laser1">
  <pose>0.15 0 0.3 0 0 0</pose>
  <rate_hz>10</rate_hz>
  <ray_count>360</ray_count>
  <fov_degrees>360</fov_degrees>
  <range_max>20.0</range_max>
  <range_std_noise>0.01</range_std_noise> <!-- Độ lệch chuẩn sai số đo khoảng cách (m) -->
  <raytrace_3d>true</raytrace_3d>
</sensor>
```

---

## 🌄 Môi trường Nâng cao & Sinh Địa hình Thủ tục (Procedural Generation)

MVSim hỗ trợ các yếu tố môi trường chuyên biệt:
- **`occupancy_grid`**: Nạp file ảnh `.png` bản đồ 2D để kiểm thử thuật toán định vị AMCL/Nav2.
- **`elevation_map`**: Nạp ảnh độ cao Grayscale để tạo địa hình đồi núi gồ ghề cho xe việt dã.
- **Biến số và Vòng lặp XML (`<for>`, `<if>`):** Tự động sinh hàng trăm chướng ngại vật ngẫu nhiên chỉ với vài dòng lệnh XML.

---

## 📌 Tóm tắt (Summary)
- MVSim kết hợp sự đơn giản của cấu trúc XML với hiệu năng vượt trội của engine Box2D, là sự bổ sung hoàn hảo cho hệ sinh thái công cụ mô phỏng của ROS 2.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[08 - Getting Started with MVSim Simulator|Bắt đầu với Phần mềm Mô phỏng MVSim]]
- 🚀 Trở về: [[ROS 2 Learning Path|Lộ trình học ROS 2 Tổng thể]]

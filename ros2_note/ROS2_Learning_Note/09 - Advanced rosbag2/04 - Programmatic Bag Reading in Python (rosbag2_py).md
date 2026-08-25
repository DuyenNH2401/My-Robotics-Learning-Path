---
tags:
  - ros2
  - rosbag2
  - bag-reading
  - python
  - rclpy
  - rosbag2_py
  - playback
  - advanced
created: 2026-08-25
aliases:
  - Đọc Dữ liệu rosbag2 bằng Python
  - Reading from a bag file (Python)
---

# 🐍 Đọc Dữ liệu rosbag2 bằng Python (Programmatic Bag Reading with Python)

> [!INFO] **Mục tiêu bài học**
> Học cách sử dụng thư viện **`rosbag2_py`** trong Python để nạp và đọc file bag: khởi tạo **`SequentialReader`**, đọc tuần tự từng bản tin với **`read_next()`**, trích xuất tên topic, dữ liệu nhị phân và phát lại lên mạng ROS 2 bằng `create_publisher`.
> - **Cấp độ:** Advanced
> - **Thời lượng ước tính:** 15 phút
> - **Mục lục tổng quan:** [[ROS 2 Learning Path]]
> - **Bài trước:** [[03 - Programmatic Bag Reading in C++ (rosbag2_transport)|Đọc Dữ liệu rosbag2 bằng C++ (rosbag2_transport)]]
> - **Bài tiếp theo:** [[05 - Developing Custom rqt_bag Plugins (Python)|Phát triển Plugin Tùy biến cho rqt_bag (Python)]]

---

## 🛠️ Triển khai mã nguồn Python (`simple_bag_reader.py`)

```python
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
import rosbag2_py
from std_msgs.msg import String

class SimpleBagReader(Node):

    def __init__(self):
        super().__init__('simple_bag_reader')
        
        # 1. Khởi tạo SequentialReader
        self.reader = rosbag2_py.SequentialReader()
        
        # 2. Cấu hình đường dẫn tới thư mục file Bag (mcap)
        storage_options = rosbag2_py.StorageOptions(
            uri='my_bag',
            storage_id='mcap'
        )
        converter_options = rosbag2_py.ConverterOptions('', '')
        self.reader.open(storage_options, converter_options)

        # 3. Tạo Publisher phát lại dữ liệu
        self.publisher = self.create_publisher(String, 'chatter', 10)
        
        # Timer phát lại chu kỳ 10 Hz (0.1 giây)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        # Duyệt qua từng bản tin còn lại trong file bag
        while self.reader.has_next():
            # msg trả về tuple: (topic_name, serialized_data, timestamp)
            topic_name, serialized_data, timestamp = self.reader.read_next()
            
            if topic_name != 'chatter':
                continue
            
            # Xuất bản dữ liệu tuần tự hóa trực tiếp ra topic
            self.publisher.publish(serialized_data)
            self.get_logger().info(f"Đã phát lại bản tin từ topic: {topic_name}")
            break

def main(args=None):
    try:
        with rclpy.init(args=args):
            sbr = SimpleBagReader()
            rclpy.spin(sbr)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

if __name__ == '__main__':
    main()
```

---

## 📌 Tóm tắt (Summary)
- `rosbag2_py.SequentialReader` cho phép tích hợp nhanh chóng dữ liệu ghi hình vào các Notebook Jupyter, xử lý dữ liệu Pandas/NumPy và các mô hình thị giác máy tính PyTorch/TensorFlow.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Phiên bản C++: [[03 - Programmatic Bag Reading in C++ (rosbag2_transport)|Đọc Dữ liệu rosbag2 bằng C++ (rosbag2_transport)]]
- ➡️ Bài tiếp theo: [[05 - Developing Custom rqt_bag Plugins (Python)|Phát triển Plugin Tùy biến cho rqt_bag (Python)]]

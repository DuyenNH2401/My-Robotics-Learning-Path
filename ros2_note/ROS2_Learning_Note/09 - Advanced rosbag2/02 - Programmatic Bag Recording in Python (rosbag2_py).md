---
tags:
  - ros2
  - rosbag2
  - recording
  - python
  - rclpy
  - rosbag2_py
  - synthetic-data
  - advanced
created: 2026-08-25
aliases:
  - Ghi rosbag2 Trực tiếp từ Node Python
  - Recording a bag from a node (Python)
---

# 🐍 Ghi rosbag2 Trực tiếp từ Node Python (Programmatic Bag Recording with Python)

> [!INFO] **Mục tiêu bài học**
> Học cách sử dụng thư viện Python **`rosbag2_py`** để tạo và ghi file bag: khởi tạo **`SequentialWriter`**, thiết lập tùy chọn lưu trữ **`StorageOptions`** (định dạng MCAP), đăng ký thông tin **`TopicMetadata`**, tuần tự hóa bản tin bằng **`serialize_message()`** và tự động sinh tập dữ liệu huấn luyện.
> - **Cấp độ:** Advanced
> - **Thời lượng ước tính:** 15 phút
> - **Mục lục tổng quan:** [[ROS 2 Learning Path]]
> - **Bài trước:** [[01 - Programmatic Bag Recording in C++ (rosbag2_cpp)|Ghi rosbag2 Trực tiếp từ Node C++ (rosbag2_cpp)]]
> - **Bài tiếp theo:** [[03 - Programmatic Bag Reading in C++ (rosbag2_transport)|Đọc Dữ liệu rosbag2 bằng C++ (rosbag2_transport)]]

---

## 🛠️ 3 Phương pháp Ghi Bag trong Python

### Cách 1: Ghi dữ liệu nhận từ Subscription (`simple_bag_recorder.py`)

```python
import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from std_msgs.msg import String
import rosbag2_py

class SimpleBagRecorder(Node):
    def __init__(self):
        super().__init__('simple_bag_recorder')
        
        # 1. Khởi tạo SequentialWriter
        self.writer = rosbag2_py.SequentialWriter()

        # 2. Cấu hình StorageOptions và ConverterOptions
        storage_options = rosbag2_py.StorageOptions(
            uri='my_bag',
            storage_id='mcap' # Chuẩn lưu trữ MCAP
        )
        converter_options = rosbag2_py.ConverterOptions('', '')
        self.writer.open(storage_options, converter_options)

        # 3. Đăng ký thông tin TopicMetadata
        topic_info = rosbag2_py.TopicMetadata(
            id=0,
            name='chatter',
            type='std_msgs/msg/String',
            serialization_format='cdr'
        )
        self.writer.create_topic(topic_info)

        # 4. Subscription nhận bản tin và ghi vào Bag
        self.subscription = self.create_subscription(
            String, 'chatter', self.topic_callback, 10
        )

    def topic_callback(self, msg):
        # Bắt buộc: Phải tuần tự hóa sang dạng nhị phân CDR trước khi ghi
        serialized_msg = serialize_message(msg)
        timestamp_ns = self.get_clock().now().nanoseconds
        self.writer.write('chatter', serialized_msg, timestamp_ns)

def main(args=None):
    rclpy.init(args=args)
    node = SimpleBagRecorder()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

### Cách 2: Tự động Sinh Dữ liệu Giả lập bằng Timer (`data_generator_node.py`)

```python
import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from example_interfaces.msg import Int32
import rosbag2_py

class DataGeneratorNode(Node):
    def __init__(self):
        super().__init__('data_generator_node')
        self.data = Int32()
        self.data.data = 0
        
        self.writer = rosbag2_py.SequentialWriter()
        self.writer.open(
            rosbag2_py.StorageOptions(uri='timed_synthetic_bag', storage_id='mcap'),
            rosbag2_py.ConverterOptions('', '')
        )

        topic_info = rosbag2_py.TopicMetadata(
            id=0, name='synthetic', type='example_interfaces/msg/Int32', serialization_format='cdr'
        )
        self.writer.create_topic(topic_info)

        # Timer chu kỳ 1 giây
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.writer.write('synthetic', serialize_message(self.data), self.get_clock().now().nanoseconds)
        self.data.data += 1
```

---

### Cách 3: Sinh Dữ liệu Cực Nhanh với Script độc lập (`data_generator_executable.py`)

```python
from rclpy.clock import Clock
from rclpy.duration import Duration
from rclpy.serialization import serialize_message
from example_interfaces.msg import Int32
import rosbag2_py

def main():
    writer = rosbag2_py.SequentialWriter()
    writer.open(
        rosbag2_py.StorageOptions(uri='big_synthetic_bag', storage_id='mcap'),
        rosbag2_py.ConverterOptions('', '')
    )

    topic_info = rosbag2_py.TopicMetadata(
        id=0, name='synthetic', type='example_interfaces/msg/Int32', serialization_format='cdr'
    )
    writer.create_topic(topic_info)

    time_stamp = Clock().now()
    # Tạo ngay 100 mẫu tin tức thì
    for i in range(100):
        data = Int32(data=i)
        writer.write('synthetic', serialize_message(data), time_stamp.nanoseconds)
        time_stamp += Duration(seconds=1)

if __name__ == '__main__':
    main()
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng `serialize_message()` từ `rclpy.serialization` để chuyển đổi object Python thành định dạng CDR tương thích với `rosbag2_py`.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Phiên bản C++: [[01 - Programmatic Bag Recording in C++ (rosbag2_cpp)|Ghi rosbag2 Trực tiếp từ Node C++ (rosbag2_cpp)]]
- ➡️ Bài tiếp theo: [[03 - Programmatic Bag Reading in C++ (rosbag2_transport)|Đọc Dữ liệu rosbag2 bằng C++ (rosbag2_transport)]]

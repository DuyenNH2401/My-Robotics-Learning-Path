---
tags:
  - ros2
  - cpp
  - rclcpp
  - node-interfaces
  - lifecycle-node
  - intermediate
created: 2026-08-25
aliases:
  - Sử dụng Node Interfaces Template Class (C++)
  - Using the Node Interfaces Template Class (C++)
---

# 🧬 Sử dụng Node Interfaces Template Class trong C++ (rclcpp::NodeInterfaces)

> [!INFO] **Mục tiêu bài học**
> Tìm hiểu cách sử dụng template class **`rclcpp::node_interfaces::NodeInterfaces<>`** để viết các hàm và thư viện dùng chung, có khả năng tương thích liền mạch với cả **Node thông thường (`rclcpp::Node`)** lẫn **Lifecycle Node (`rclcpp_lifecycle::LifecycleNode`)**.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 10 phút
> - **Bài trước:** [[07 - Composing Multiple Nodes in a Single Process|Kết hợp nhiều Node trong một Tiến trình]]
> - **Bài tiếp theo:** [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]

---

## 📖 Vấn đề cốt lõi (The Problem)

Trong ROS 2, hai lớp cơ bản là `rclcpp::Node` và `rclcpp_lifecycle::LifecycleNode` **không cùng chung một cây kế thừa (no shared base class)**.

Nếu bạn viết một hàm tiện ích nhận tham số là `std::shared_ptr<rclcpp::Node>`:
```cpp
void print_node_info(rclcpp::Node::SharedPtr node) {
  RCLCPP_INFO(node->get_logger(), "Node name: %s", node->get_name());
}
```
Hàm này sẽ **bị lỗi biên dịch (compile error)** khi bạn truyền vào một con trỏ `LifecycleNode::SharedPtr`.

---

## 💡 Giải pháp: Node Interfaces Architecture

Kiến trúc ROS 2 chia nhỏ chức năng của một Node thành các interface độc lập:
- `NodeBaseInterface`: Chức năng cơ bản (tên node, context, namespace).
- `NodeLoggingInterface`: Chức năng ghi nhật ký (logger).
- `NodeParametersInterface`: Quản lý parameters.
- `NodeTopicsInterface`: Quản lý publisher/subscriber.
- `NodeServicesInterface`: Quản lý service/client.
- `NodeWaitablesInterface`: Quản lý timer và waitables.

Cả `rclcpp::Node` và `rclcpp_lifecycle::LifecycleNode` đều cung cấp các interface này!

---

## 🛠️ Triển khai chuẩn với `rclcpp::NodeInterfaces<>`

Template `rclcpp::node_interfaces::NodeInterfaces<>` cho phép gom nhóm chính xác các interface mà hàm của bạn cần và hỗ trợ **tự động ép kiểu ngầm định (implicit conversion)** từ đối tượng node:

```cpp
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "rclcpp/node_interfaces/node_interfaces.hpp"

// 1. Định nghĩa kiểu Interface gom nhóm NodeBase và NodeLogging
using MyNodeInterfaces = rclcpp::node_interfaces::NodeInterfaces<
  rclcpp::node_interfaces::NodeBaseInterface,
  rclcpp::node_interfaces::NodeLoggingInterface
>;

// 2. Hàm tiện ích nhận MyNodeInterfaces làm tham số
void node_info(MyNodeInterfaces interfaces)
{
  auto base_interface = interfaces.get_node_base_interface();
  auto logging_interface = interfaces.get_node_logging_interface();
  
  RCLCPP_INFO(
    logging_interface->get_logger(),
    "Thong tin Node Name: %s",
    base_interface->get_name()
  );
}

// Node thông thường
class SimpleNode : public rclcpp::Node
{
public:
  SimpleNode(const std::string & name) : Node(name) {}
};

// Node Lifecycle
class SimpleLifecycleNode : public rclcpp_lifecycle::LifecycleNode
{
public:
  SimpleLifecycleNode(const std::string & name) : LifecycleNode(name) {}
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto normal_node = std::make_shared<SimpleNode>("My_Standard_Node");
  auto lc_node = std::make_shared<SimpleLifecycleNode>("My_Lifecycle_Node");

  // Truyền đối tượng (dereference pointer) -> Tự động chuyển đổi kiểu!
  node_info(*normal_node);
  node_info(*lc_node);

  rclcpp::shutdown();
  return 0;
}
```

Kết quả thực thi:
```text
[INFO] [My_Standard_Node]: Thong tin Node Name: My_Standard_Node
[INFO] [My_Lifecycle_Node]: Thong tin Node Name: My_Lifecycle_Node
```

---

## 📌 Ưu điểm của `rclcpp::NodeInterfaces<>`
1. **Tính đa hình cao:** Viết code một lần, dùng được cho mọi loại Node trong hệ sinh thái ROS 2.
2. **Ngắn gọn & Dễ đọc:** Tránh việc phải truyền hàng dài các con trỏ interface riêng lẻ vào danh sách tham số hàm.
3. **An toàn kiểu dữ liệu:** Trình biên dịch kiểm tra tại compile-time, đảm bảo node cung cấp đúng các interface cần thiết.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[07 - Composing Multiple Nodes in a Single Process|Kết hợp nhiều Node trong một Tiến trình]]
- ➡️ Bài tiếp theo: [[09 - Publishing Messages using YAML Files|Publish Message qua File YAML]]

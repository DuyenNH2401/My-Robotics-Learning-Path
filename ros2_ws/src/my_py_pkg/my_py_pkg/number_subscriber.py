import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64


class NumberSubscriber(Node):
    def __init__(self):
        super().__init__("number_subscriber")
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(
            Int64, "number", self.number_callback, 10
        )
        self.get_logger().info("Number subscriber node has been started.")

    def number_callback(self, msg):
        self.counter_ += 1
        self.get_logger().info(f"Received number: {msg.data}, count: {self.counter_}")


def main(args=None):
    rclpy.init(args=args)
    node = NumberSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

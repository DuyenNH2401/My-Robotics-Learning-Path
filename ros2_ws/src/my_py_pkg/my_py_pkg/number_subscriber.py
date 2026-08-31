import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from my_robot_interfaces.msg import HardwareStatus


class NumberSubscriber(Node):
    def __init__(self):
        super().__init__("number_subscriber")
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(
            HardwareStatus, "HardwareStatus", self.number_callback, 10
        )
        self.get_logger().info("Number subscriber node has been started.")

    def number_callback(self, msg):
        self.counter_ += 1
        self.get_logger().info(
            f"Received hardware status: {msg.version}, temperature: {msg.temperature}, motors ready: {msg.are_motors_ready}, count: {self.counter_}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = NumberSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

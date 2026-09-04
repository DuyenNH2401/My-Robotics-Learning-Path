import rclpy
from example_interfaces.msg import Int64
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus


class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__("number_publisher")
        self.declare_parameter("number", 2)
        self.declare_parameter("publish_period", 1.0)

        self.number_ = self.get_parameter("number").value
        self.publish_period_ = self.get_parameter("publish_period").value

        # self.number_publisher_ = self.create_publisher(
        #     HardwareStatus, "HardwareStatus", 10
        # )
        self.number_publisher_ = self.create_publisher(Int64, "number", 10)
        self.number_timer_ = self.create_timer(self.publish_period_, self.my_publish_number)
        self.get_logger().info("Number publisher node has been started.")

    def publish_number(self):
        msg = Int64()
        msg.data = self.number_
        self.number_publisher_.publish(msg)

    def my_publish_number(self):
        msg = Int64()
        msg.data = self.number_
        # msg.temperature = 25.0
        # msg.are_motors_ready = True
        self.number_publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

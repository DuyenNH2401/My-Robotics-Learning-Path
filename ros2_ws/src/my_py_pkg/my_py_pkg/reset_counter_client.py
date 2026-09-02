from my_robot_interfaces.srv import ResetCounter
import rclpy
from rclpy.node import Node


class ResetCounterClient(Node):
    def __init__(self):
        super().__init__("reset_counter_client")
        self.client_ = self.create_client(ResetCounter, "reset_counter")

    def call_reset_counter(self, value):
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Waiting for the reset_counter service to be available..."
            )
        request = ResetCounter.Request()
        request.reset_value = value
        future = self.client_.call_async(request)
        future.add_done_callback(self.callback_reset_counter_response)

    def callback_reset_counter_response(self, future):
        response = future.result()
        self.get_logger().info(f"Success flag: {response.success}")
        self.get_logger().info(f"Message: {response.message}")


def main(args=None):
    rclpy.init(args=args)
    node = ResetCounterClient()
    node.call_reset_counter(5)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

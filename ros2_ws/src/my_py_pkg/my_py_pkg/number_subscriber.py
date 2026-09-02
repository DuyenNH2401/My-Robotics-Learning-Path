import rclpy
from rclpy.node import Node

from my_robot_interfaces.msg import HardwareStatus
from my_robot_interfaces.srv import ResetCounter


class NumberSubscriber(Node):
    def __init__(self):
        super().__init__("number_subscriber")
        self.counter_ = 0
        self.number_subscriber_ = self.create_subscription(
            HardwareStatus, "HardwareStatus", self.number_callback, 10
        )

        self.reset_counter_services_ = self.create_service(
            ResetCounter, "reset_counter", self.callback_reset_counter
        )

        self.get_logger().info("Number subscriber node has been started.")

    def number_callback(self, msg):
        self.counter_ += 1
        self.get_logger().info(
            f"Received hardware status: {msg.version}, temperature: {msg.temperature}, motors ready: {msg.are_motors_ready}, count: {self.counter_}"
        )

    def callback_reset_counter(
        self, request: ResetCounter.Request, response: ResetCounter.Response
    ):
        if request.reset_value < 0:
            response.success = False
            response.message = "Reset value must be non-negative."
            return response
        elif request.reset_value > self.counter_:
            response.success = False
            response.message = (
                "Reset value must be less than or equal to the current counter value."
            )
            return response
        else:
            self.counter_ = request.reset_value
            self.get_logger().info(f"Counter reset to: {self.counter_}")
            response.success = True
            response.message = "Success"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = NumberSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

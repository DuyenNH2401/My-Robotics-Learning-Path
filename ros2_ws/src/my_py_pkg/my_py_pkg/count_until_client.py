import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import CountUntil


class CountUntilClient(Node):
    def __init__(self):
        super().__init__("count_until_client")
        self.count_until_client_ = ActionClient(self, CountUntil, "count_until")

    def send_goal(self, target_number, delay):
        self.count_until_client_.wait_for_server()
        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.delay = delay
        future = self.count_until_client_.send_goal_async(goal)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future :ClientGoalHandle):
        self.goal_handle_ = future.result()
        if self.goal_handle_.accepted:
            self.get_logger().info("Goal accepted")
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().info("Goal rejected")

    def goal_result_callback(self, future :ClientGoalHandle):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info("Canceled")

        self.get_logger().info(f"Result: {result.final_number}")


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClient()
    node.send_goal(5, 0.5)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
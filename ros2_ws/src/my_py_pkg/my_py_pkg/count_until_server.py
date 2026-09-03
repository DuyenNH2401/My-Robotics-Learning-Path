import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from my_robot_interfaces.action import CountUntil


class CountUntilServer(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.count_until_server_ = ActionServer(self, CountUntil, "count_until",
                                                goal_callback=self.goal_callback,
                                                cancel_callback=self.cancel_callback,
                                                callback_group=ReentrantCallbackGroup(),
                                                execute_callback=self.execute_callback)


    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("Count Until Goal received")

        if goal_request.target_number <=0:
            self.get_logger().warn("Reject the goal, target number must be greater than 0")
            return GoalResponse.REJECT
        self.get_logger().info("Count Until Goal received")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Count until cancel received")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        target_number = goal_handle.request.target_number
        delay = goal_handle.request.delay
        result = CountUntil.Result()
        feedback = CountUntil.Feedback()
        counter = 0

        self.get_logger().info("Executing the goal.")
        for i in range(target_number):
            if goal_handle.is_cancel_requested:
                self.get_logger().info("Canceled")
                goal_handle.canceled()
                result.final_number = counter
                return result
            counter += 1
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(str(counter))

            time.sleep(delay)

        goal_handle.succeed()
        result.final_number = counter
        return result

def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServer()
    rclpy.spin(node, MultiThreadedExecutor())
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.action.server import ServerGoalHandle
from my_robot_interfaces.action import CountUntil


class CountUntilServer(Node):
    def __init__(self):
        super().__init__("count_until")
        self.count_until_server_ = ActionServer(self, CountUntil, "count_until", goal_callback=self.goal_callback, execute_callback=self.execute_callback)


    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("Count Until Goal received")

        if goal_request.target_number <=0:
            self.get_logger().warn("Reject the goal, target number must be greater than 0")
            return GoalResponse.REJECT
        self.get_logger().info("Count Until Goal received")
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        target_number = goal_handle.target_number
        delay = goal_handle.delay
        result = CountUntil.Result()
        counter = 0

        self.get_logger().info("Executing the goal.")
        for i in range(target_number):
            counter += 1
            self.get_logger().info(str(counter))
            time.sleep(delay)

        goal_handle.succeed()
        result.final_number = counter
        return result

def main(args=None):
    rclpy.init(args=args)
    count_until_server = CountUntilServer()
    rclpy.spin(count_until_server)
    count_until_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



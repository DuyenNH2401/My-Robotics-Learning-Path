import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim_msgs.msg import Pose


class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        self.publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(
            Pose, "turtle1/pose", self.pose_callback, 10
        )
        self.get_logger().info("Turtle Controller has been started.")

    def pose_callback(self, pose: Pose):
        cmd = Twist()

        self.x_ = pose.x
        self.y_ = pose.y
        self.theta_ = pose.theta

        if self.x_ < 5.5:
            cmd.linear.x = 1.0
            cmd.angular.z = 1.0
            self.publisher_.publish(cmd)
        else:
            cmd.linear.x = 2.0
            cmd.angular.z = 2.0
            self.publisher_.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

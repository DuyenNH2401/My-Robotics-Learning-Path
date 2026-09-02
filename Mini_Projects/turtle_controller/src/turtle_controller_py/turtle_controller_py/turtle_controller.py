import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim_msgs.msg import Pose
from turtlesim_msgs.srv import SetPen
from turtle_interface.srv import ActiveTurtle



class TurtleController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0
        self.prev_x_ = 0.0
        self.is_active = 0

        self.publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.subscriber_ = self.create_subscription(
            Pose, "turtle1/pose", self.pose_callback, 10
        )

        self.active_turtle_service_ = self.create_service(ActiveTurtle, "turtle1/active_turtle", self.callback_active_turtle)
        self.set_color_client_ = self.create_client(SetPen, "turtle1/set_pen")

        self.get_logger().info("Turtle Controller has been started.")

    def pose_callback(self, pose: Pose):

        if not self.is_active:
            return

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

        if self.prev_x_ < 5.5 and self.x_ >= 5.5:
            self.get_logger().info("Change side, color set to Red")
            self.call_set_pen((255, 0, 0))

        if self.prev_x_ > 5.5 and self.x_ <= 5.5:
            self.get_logger().info("Change side, color set to green")
            self.call_set_pen((0, 255, 0))

        self.prev_x_ = self.x_

    def call_set_pen(self, color):
        while not self.set_color_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                "Waiting for the set pen service..."
            )
        r, g, b = color
        request = SetPen.Request()
        if self.x_ < 5.5:
            request.r = r
            request.g = g
            request.b = b
        else:
            request.r = r
            request.g = g
            request.b = b

        future = self.set_color_client_.call_async(request)

    def callback_active_turtle(self, request: ActiveTurtle.Request, response: ActiveTurtle.Response):
        self.is_active = request.active_turtle
        if request.active_turtle:
            response.message = "Starting the turtle"
        else:
            response.message = "Stopping the turtle"
        return response


def main(args=None):
    rclpy.init(args=args)
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

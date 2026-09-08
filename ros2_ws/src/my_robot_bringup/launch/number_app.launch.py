from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    number_publisher_node = Node(
        package="my_py_pkg",
        executable="number_publisher",
        name="number_publisher",
    )

    number_subscriber_node = Node(
        package="my_py_pkg",
        executable="number_subscriber",
        name="number_subscriber",
    )

    ld.add_action(number_publisher_node)
    ld.add_action(number_subscriber_node)

    return ld

#
# number_publisher1 = Node(
#     package="my_py_pkg",
#     executable="number_publisher",
#     name="num_pub1",
#     remappings=[("/number", "/my_number")],
#     parameters=[
#         {"number": 3},
#         {"publish_period": 1.5}
#     ]
# )
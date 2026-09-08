import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    yaml_path = os.path.join(
        get_package_share_directory('my_turtle_bringup'),
        'config',
        'turtle_params.yaml'
    )
    turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
        #namespace="t1",
        parameters=[yaml_path]
    )

    turtle_controller_node = Node(
        package="turtle_controller_py",
        executable="turtle_controller",
        #namespace="t1",
        parameters=[yaml_path]
    )

    return LaunchDescription([turtlesim_node, turtle_controller_node])
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Path to your Xacro file
    pkg_path = os.path.join(
        get_package_share_directory('navigation_bot')
    )
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')

    # Convert Xacro -> XML
    robot_description_config = xacro.process_file(xacro_file)

    # Create robot_state_publisher node
    params = {
        'robot_description': robot_description_config.toxml(),
        'use_sim_time': use_sim_time
    }
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Create joint_state_publisher node
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        # If you want to use sim time, you can add that as well
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'
        ),
        node_joint_state_publisher,
        node_robot_state_publisher,
    ])

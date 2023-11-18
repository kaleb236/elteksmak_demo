from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='elteksmak_demo',
            executable='mqtt_sub',
            name='mqtt_sub',
        )
    ])
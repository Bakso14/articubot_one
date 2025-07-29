import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'my_bot'  # <--- Ganti sesuai package kamu

    # Jalankan robot_state_publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory(package_name), 'launch', 'rsp.launch.py')
        ]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Jalankan Gazebo Harmonic (bukan gazebo_ros)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ])
    )

    # Gantilah spawn_entity.py dengan ros_gz_sim create
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-topic', 'robot_description',
            '-name', 'my_bot'
        ],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])

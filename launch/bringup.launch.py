from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():

    pkg_share = FindPackageShare("l298n_bringup")

    robot_description = {
        "robot_description": Command([
            "xacro ",
            PathJoinSubstitution([pkg_share, "urdf", "robot.urdf.xacro"])
        ])
    }

    diff_drive_yaml = PathJoinSubstitution(
        [pkg_share, "config", "diff_drive.yaml"]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, diff_drive_yaml],
        output="screen"
    )

    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    return LaunchDescription([
        control_node,
        joint_state_spawner,
        diff_drive_spawner
    ])

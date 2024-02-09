from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context):
    params = LaunchConfig('params_file').perform(context)
    print(f'Reading parameters from {params}')

    if not params:
        params = PathJoinSubstitution(
            FindPackageShare('ublox_gps'),
            'config',
            'zed_f9p.yaml'
        )
    
    ublox_gps_node = Node(
        package='ublox_gps',
        executable='ublox_gps_node',
        output='both',
        parameters=[params]
    )

    return [ublox_gps_node]


def generate_launch_description():
    # return launch.LaunchDescription([
    #     ublox_gps_node,
    #     launch.actions.RegisterEventHandler(
    #         event_handler=launch.event_handlers.OnProcessExit(
    #             target_action=ublox_gps_node,
    #             on_exit=[launch.actions.EmitEvent(
    #                 event=launch.events.Shutdown())],
    #         )),
    #     ])

    return LaunchDescription([
        LaunchArg('params_file', default_value='',
            description='path to ros parameter definition file'),
        OpaqueFunction(function=launch_setup)
    ])

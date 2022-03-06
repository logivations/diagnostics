import launch
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

analyzer_params_file_path = get_package_share_directory("diagnostic_aggregator") + "/analyzers.yaml"


def generate_launch_description():

    aggregator_node = ExecuteProcess(
        cmd=[
            "@AGGREGATOR_NODE@",
            "--ros-args",
            "--params-file",
            analyzer_params_file_path
        ],
        name='aggregator_node',
        emulate_tty=True,
        output='screen')

    # example node launch
    diag_publisher = Node(
        package='diagnostic_aggregator',
        executable='example_pub.py')

    return launch.LaunchDescription([
        aggregator_node,
        diag_publisher,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=aggregator_node,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )),
    ])

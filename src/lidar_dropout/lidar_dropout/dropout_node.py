import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import PointCloud2


class PointCloudDropoutNode(Node):

    def __init__(self):
        super().__init__('pointcloud_dropout_node')

        # 기본 dropout 비율은 30%
        self.declare_parameter('dropout_ratio', 0.3)
        self.dropout_ratio = (
            self.get_parameter('dropout_ratio')
            .get_parameter_value()
            .double_value
        )

        # dropout 비율이 올바른 범위인지 검사
        if not 0.0 <= self.dropout_ratio < 1.0:
            raise ValueError(
                'dropout_ratio는 0.0 이상, 1.0 미만이어야 합니다.'
            )

        # 같은 조건에서 실험 결과를 재현하기 위한 난수 생성기
        self.random_generator = np.random.default_rng(seed=42)

        # 원본 Point Cloud를 받는 subscriber
        self.subscription = self.create_subscription(
            PointCloud2,
            '/velodyne_points',
            self.pointcloud_callback,
            qos_profile_sensor_data
        )

        # dropout 결과를 보내는 publisher
        self.publisher = self.create_publisher(
            PointCloud2,
            '/velodyne_points_dropout',
            qos_profile_sensor_data
        )

        self.frame_count = 0

        self.get_logger().info(
            f'Dropout node 시작: 제거 비율 = '
            f'{self.dropout_ratio * 100:.0f}%'
        )

    def pointcloud_callback(self, input_msg):
        total_points = input_msg.width * input_msg.height

        if total_points == 0:
            self.get_logger().warning('빈 Point Cloud가 입력되었습니다.')
            return

        keep_ratio = 1.0 - self.dropout_ratio
        keep_count = max(1, int(total_points * keep_ratio))

        # 유지할 포인트의 인덱스를 무작위로 선택
        selected_indices = self.random_generator.choice(
            total_points,
            size=keep_count,
            replace=False
        )

        # 원본 배열 순서가 너무 뒤섞이지 않도록 정렬
        selected_indices.sort()

        expected_data_size = total_points * input_msg.point_step

        if len(input_msg.data) != expected_data_size:
            self.get_logger().error(
                '현재 Point Cloud에는 행 패딩이 있어 '
                '이 코드로 처리할 수 없습니다.'
            )
            return

        # 각 포인트를 point_step 바이트 단위로 분리
        point_array = np.frombuffer(
            input_msg.data,
            dtype=np.uint8
        ).reshape(total_points, input_msg.point_step)

        # 선택한 포인트만 남김
        dropout_array = point_array[selected_indices]

        # 새로운 PointCloud2 메시지 생성
        output_msg = PointCloud2()
        output_msg.header = input_msg.header
        output_msg.height = 1
        output_msg.width = keep_count
        output_msg.fields = input_msg.fields
        output_msg.is_bigendian = input_msg.is_bigendian
        output_msg.point_step = input_msg.point_step
        output_msg.row_step = keep_count * input_msg.point_step
        output_msg.data = dropout_array.tobytes()
        output_msg.is_dense = input_msg.is_dense

        self.publisher.publish(output_msg)

        self.frame_count += 1

        # 로그가 너무 많이 나오지 않도록 10프레임마다 출력
        if self.frame_count % 10 == 0:
            removed_count = total_points - keep_count

            self.get_logger().info(
                f'프레임 {self.frame_count}: '
                f'원본 {total_points}개 → '
                f'제거 {removed_count}개 → '
                f'유지 {keep_count}개'
            )


def main(args=None):
    rclpy.init(args=args)

    node = PointCloudDropoutNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

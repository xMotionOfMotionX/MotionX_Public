import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from ackermann_msgs.msg import AckermannDriveStamped
import numpy as np

class F1TenthToMotionX(Node):
    def __init__(self):
        super().__init__('motionx_adapter')
        # 1. 시뮬레이터로부터 데이터를 받을 구독자 (Subscriber)
        self.create_subscription(Imu, '/imu', self.imu_callback, 10)
        
        # 2. MotionX 미들웨어 규격으로 다시 쏴줄 발행자 (Publisher)
        # 이 데이터가 나중에 젯슨으로 넘어갑니다.
        self.motion_pub = self.create_publisher(Imu, '/motionx/raw_inertia', 10)
        self.get_logger().info('MotionX Adapter is running...')

    def imu_callback(self, msg):
        # 위험 감지 로직 (간단한 버전)
        # 가속도의 급격한 변화(Jerk) 계산
        accel_x = msg.linear_acceleration.x
        if abs(accel_x) > 8.0:  # 임계값 예시: 8m/s^2 이상이면 위험
            self.get_logger().warn('⚠️ Abnormal Motion Detected! Emergency Signal Ready.')
        
        # 데이터를 MotionX 표준 토픽으로 다시 발행
        self.motion_pub.publish(msg)

def main():
    rclpy.init()
    node = F1TenthToMotionX()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

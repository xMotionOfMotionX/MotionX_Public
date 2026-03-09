import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class VirtualMotionXCore(Node):
    def __init__(self):
        super().__init__('virtual_motionx_core')
        # 1. 어댑터로부터 데이터를 받는 구독자
        self.create_subscription(Imu, '/motionx/raw_inertia', self.process_callback, 10)
        
        # 2. 계산된 보정값을 쏠 발행자 (이게 있어야 Foxglove에 뜹니다)
        self.pub = self.create_publisher(Imu, '/motionx/stabilized_vector', 10)
        self.get_logger().info('🚀 Virtual MotionX Core (Jetson Dummy) Started!')

    def process_callback(self, msg):
        # 멀미 저감 보정값 계산 (예시: 반대 방향으로 50% 상쇄)
        msg.linear_acceleration.x *= -0.5
        msg.linear_acceleration.y *= -0.5
        
        # 3. 보정된 데이터를 새로운 토픽으로 발행
        self.pub.publish(msg)
        self.get_logger().info('✅ Stabilizing... Correction Vector Published.')

def main(args=None):
    rclpy.init(args=args)
    node = VirtualMotionXCore()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

# 직접 실행을 위해 필수인 블록
if __name__ == "__main__":
    main()
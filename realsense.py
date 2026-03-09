import pyrealsense2 as rs
import numpy as np
import cv2

class MotionXStabilizer:
    def __init__(self):
        # 리얼센스 파이프라인 설정
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  #초당 30 프레임 30fps
        
        #센서 데이터 수집 (RealSense & RGB)
        self.pipeline.start(config)
        self.prev_gray = None

    def run(self):
        try:
            while True:
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                frame = np.asanyarray(color_frame.get_data())
                curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if self.prev_gray is not None:
                    # 1. Optical Flow로 차량의 움직임 벡터 계산, (예: 차량이 왼쪽으로 회전하면 영상 속의 모든 사물은 오른쪽으로 쏠린다. 이 현상을 벡터 (방향과 크기)로 계산)
                    flow = cv2.calcOpticalFlowFarneback(self.prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                    avg_motion = np.mean(flow, axis=(0, 1)) #전체적인 흔들림의 평균값 계산

                    # 2. 역방향 모션 보정 (Reverse Motion Compensation)
                    # 움직임의 반대 방향으로 이미지를 이동시켜 안정화
                    M = np.float32([[1, 0, -avg_motion[0]], [0, 1, -avg_motion[1]]])  #역방향 행렬 생성
                    stabilized = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))  #이미지 밀기

                    # 결과 화면 출력
                    cv2.imshow('MotionX Original', frame)
                    cv2.imshow('MotionX Stabilized', stabilized)

                self.prev_gray = curr_gray

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.pipeline.stop()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    stabilizer = MotionXStabilizer()
    stabilizer.run()
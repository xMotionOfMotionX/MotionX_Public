import cv2
import numpy as np
import os
import csv

class MotionXFileAnalyzer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.prev_gray = None
        # 데이터 저장을 위한 준비
        self.motion_logs = []

    def analyze(self):
        print(f"--- 분석 시작: {os.path.basename(self.video_path)} ---")
        
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # 1. 전처리 (흑백 전환 및 크기 조절로 속도 향상)
            frame_resized = cv2.resize(frame, (640, 480))
            curr_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            if self.prev_gray is not None:
                # 2. Optical Flow 계산 (흔들림 벡터 추출)
                flow = cv2.calcOpticalFlowFarneback(self.prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                avg_motion = np.mean(flow, axis=(0, 1)) # [dx, dy] 평균값

                # 데이터 로그 추가
                self.motion_logs.append(avg_motion)

                # 3. 역방향 보정 시각화 (테스트용)
                M = np.float32([[1, 0, -avg_motion[0]], [0, 1, -avg_motion[1]]])
                stabilized = cv2.warpAffine(frame_resized, M, (640, 480))

                cv2.imshow('Original', frame_resized)
                cv2.imshow('Stabilized (MotionX)', stabilized)

            self.prev_gray = curr_gray

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.save_to_csv()

    # def save_to_csv(self):
    #     output_name = os.path.basename(self.video_path).replace(".mp4", "_motion.csv")
    #     with open(output_name, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['dx', 'dy']) # 헤더
    #         writer.writerows(self.motion_logs)
    #     print(f"✅ 데이터 저장 완료: {output_name}")

    def save_to_csv(self):
        output_name = os.path.basename(self.video_path).replace(".mp4", "_motion_cleaned.csv")
        
        # 임계값 설정 (예: 움직임 크기가 0.01 이상일 때부터 시작, 정지구간 제거 (재생 버튼 클릭 전과 그 후 멈춰 있는 구간 제거))
        threshold = 0.01
        start_index = 0
        
        for i, motion in enumerate(self.motion_logs):
            magnitude = np.sqrt(motion[0]**2 + motion[1]**2)
            if magnitude > threshold:
                start_index = i
                break
                
        cleaned_data = self.motion_logs[start_index:] # 진짜 데이터만 슬라이싱

        with open(output_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['dx', 'dy'])
            writer.writerows(cleaned_data)
        print(f"✅ 정제된 데이터 저장 완료 (버린 프레임: {start_index}개): {output_name}")

if __name__ == "__main__":
    video_folder = "Jetson/Windows"
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

    for video_file in video_files:
        full_path = os.path.join(video_folder, video_file)
        analyzer = MotionXFileAnalyzer(full_path)
        analyzer.analyze()
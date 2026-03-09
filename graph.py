import pandas as pd
import matplotlib.pyplot as plt

# 1. 데이터 불러오기 (파일명은 본인의 CSV 이름으로 수정하세요)
df = pd.read_csv('data/RealSense Viewer v2.57.5 2026-01-31 08-32-48_motion_cleaned.csv')

# 2. 그래프 그리기
plt.figure(figsize=(12, 5))
plt.plot(df['dx'], label='Horizontal (Left/Right)', color='#1f77b4', alpha=0.8)
plt.plot(df['dy'], label='Vertical (Up/Down)', color='#ff7f0e', alpha=0.8)

# 3. 꾸미기
plt.title('Vehicle Motion Signature Analysis (MotionX)', fontsize=15)
plt.xlabel('Frame Number', fontsize=12)
plt.ylabel('Motion Magnitude (Pixels)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

# 4. 저장 및 출력
plt.savefig('graphs/motion_analysis_result.png') # 깃허브에 올릴 이미지 파일
plt.show()
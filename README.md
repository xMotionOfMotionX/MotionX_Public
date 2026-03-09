# MotionX: Visual-Inertial Anti-Motion Integrated Simulator (Sim to Sim to Sim to Sim to Sim then Real)

MotionX is an AI-powered solution designed to mitigate motion sickness and prevent dangerous collision in autonomous vehicles by synchronizing visual and inertial data between various simulators.

## 🚀 First Test Overview
This project focuses on real-time visual motion compensation. By analyzing the vehicle's movement through an Intel RealSense camera, our algorithm calculates the reverse motion vector to stabilize the visual flow for passengers.

## 🛠 Tech Stack
- **Simulators**: F1tenth Gym, Donkey Car, Isaac Sim, MuJoCo, Carla
- **Hardware**: NVIDIA Jetson Orin Nano, Intel RealSense D435i
- **Software**: Python, OpenCV, ROS 2, pyrealsense2


## 📺 Demo
[Check out our data acquisition demo on YouTube](https://youtu.be/Dv3aUmfnNwM?si=ZvAskxh2yRYUGfJl)

## 📁 Project Structure
- `main.py`: Real-time motion analysis and compensation algorithm.
- `requirements.txt`: List of dependencies.
- data/: Raw motion logs (CSV files with $dx, dy$ values).
- graphs/: Visualization graphs 



[Winning Point]
- Universal Middleware: With Jetson, it can be connected to any simulator or car data

- Edge AI Optimization: With the Use of GPU, Optical Flow can be calculated in real time, which allows accurate compensation.

- Safety Layer: Not only anti motion sickness but also detecting dangerous motion to stop the car for safety.

"MotionX는 단순히 멀미를 줄이는 도구가 아닙니다. 차량의 물리적 관성(Inertia)과 승객의 시각적 경험(Visual)을 연결하는 표준 운영 체제를 지향합니다."


[Simulator / Main Area / Motion Data Structure]
-F1tenth	Gym / Autonomous Racing / ROS 2 Topics (/imu, /odom)	
-MuJoCo / Contact Physics, Walking Robot / Sensor XML + mjData Struct (XML로 센서를 정의하면 Python/C++ API의 mjData 구조체로 가속도, 힘 데이터가 나옵니다.)
-Isaac Sim / NVIDIA Omniverse AI / ROS2 Bridge, Python API (NVIDIA 전용. USD 기반 데이터가 ROS 2나 Python API로 바로 꽂힙니다.)
-Donkey Sim / Beginner Autonomous Driving / Socker, JSON (유니티 기반이며, 보통 소켓 통신을 통해 JSON 형식으로 차량의 속도와 각도를 쏴줍니다.)
-CARLA / City Autonomous Driving / Python API, ROS2 Bridge (가장 방대한 센서군(IMU, GNSS 등)을 Python 객체나 ROS 토픽으로 제공합니다.) 


[Strategy]: 
입력 (Input): 각 시뮬레이터의 특성에 맞는 '통역사' 파일을 만듭니다. (carla_adapter.py, donkey_adapter.py 등)

규격화 (Standardize): 형식이 뭐든 간에 우리 미들웨어 내부에서는 똑같은 MotionX_Inertia 메시지로 변환합니다.

판단 (Core): 젯슨 오린 나노에 있는 MotionX Core는 이 데이터가 어디서 왔는지 상관하지 않고 똑같은 '안티 모션' 알고리즘과 '위험 감지' 로직을 돌립니다.

1st Step: Running F1tenth Gym and Donkey car using the same python algorithm.

다중 시뮬레이터 대통합 (알고리즘 하나로 모두 동작), 모션 데이터 추출, 그리고 역방향 모션 생성
Raw Socket later, work on gym.donkeycar and ROS2 connection first.
1. Run pure_pursuit_node.py and waypoint same file in donkey car, translate the ROS2 topics for donkey car.
2. Run pure_pursuit_node.py in Jetson (or VMWare), translate the topics and connect with socket in donkey car (Macbook) 

The RAW UNITY DATA of Donkey Car Simulator does not use position data --> try pure pursuit and MPC with other simulators later. (Donkey sim data contains speed, yaw, accel/gyro IMU sensor, and odom wheel rotation data. We will integrate these motion data later on)

--> Follow the gap integration with lidar data test. (no position data required)
liar data is ok, bridge translator between F1tenth and Donkeycar is on the way. Mocking nodes within the system of Donkey car is necessary to connect ROS2 F1tenth algorithm to JSON topics in Donkey Car.
Sim to Sim on going.

잘못된 모션엑스 브릿지 디버깅 포인트. 
1. 조향 민감도(Scale) 조절 실패: 근본 원인(알고리즘 오판)을 놔두고 출력값만 줄이려 해서 효과가 없었습니다.
2. 시야각(FOV) 정밀 컷팅 실패: 딱 180도만 잘라주니, 측면 사각지대를 보지 못해 코너에서 바로 충돌했습니다.
3. 좌우 배열 반전(Mirroring) 실패: 시뮬레이터 간의 '센서 방향'과 '조향 방향'이 이중으로 반전되어 우연히 맞던 것을 억지로 뒤집어 벽으로 돌진하게 만들었습니다.
4. 스무딩(Smoothing) 필터 추가 실패: 조향에 지연 시간(Delay)을 발생시켜 와블(Wobble) 현상을 오히려 악화시켰습니다.

모션엑스 브릿지로 f1tenth ftg 코드를 동키카에 연동시킨것과, ftg 코드 자체에서 ros2 대신 donkey car json 토픽 형식으로 바꾼 코드 자체를 돌릴때 자동차의 반응이 똑같음. 즉, 브릿지는 잘 만들었고, F1tenth 에서 잘 돌아가던게 donkey car에서 와블 후 벽에 박는 이유는 맵과 자동차의 스케일이 달라 bubble radius 등 맞춰야 할 값들이 다른 것. 스케일만 맞추면 잘 동작할 것으로 보임. 
f1tenth car: f1tenth map  =  donkey car : donkey map
1. scale_factor for lidar range: calculated value is necessary because of max_gap_safe_dist in original algorithm
2. donkey car steering is more sensitive, 
3. throttle gain makes the velocity similar. 
4. steering penalty (against velocity)is also necessary
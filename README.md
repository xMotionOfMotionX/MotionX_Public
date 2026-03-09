# MotionX: Motion Data & Anti-Motion Integration
### "Bridging the Gap between Visual Flow and Physical Inertia"

## 📺 Pilot Demo: Sim-to-Sim Data Integration
[![](https://img.youtube.com/vi/JsVlAP03GSE/0.jpg)](https://youtu.be/JsVlAP03GSE)
> *Extracting F1TENTH racing data to synchronize with Donkey Car dynamics.*

---

## 🎯 Our Mission: Data for Inverse Motion
Unlike typical autonomous controllers, **MotionX** focuses on extracting high-fidelity motion profiles from diverse simulators to solve the **Visual-Inertial Gap**.

* **Why Multi-Sim?** To gather diverse $G$-force, $Yaw$, and $Inertia$ data in a risk-free environment.
* **The Goal:** Use the extracted data to calculate **Reverse Motion Vectors**, providing a foundation for anti-motion sickness solutions and visual stabilization.
* **Data Standardization:** Whether it's F1TENTH or CARLA, all telemetry is normalized into the MotionX data structure for immediate motion analysis.



---

## 🛠 Current Phase: Sim-to-Sim Data Bridge
We are currently synchronizing **F1TENTH (High-speed Racing)** and **Donkey Car (Small-scale Dynamics)** to validate our data extraction pipeline.

* **Lidar Scaling (9.9x):** Adjusting spatial perception to match different environment scales.
* **Motion Telemetry:** Mapping ROS 2 topics to JSON-based simulator sockets.
* **Dynamic Response:** Real-time throttle/steering adjustment to observe physical inertia changes.

---

## 📁 Tech Highlights
* **Platform:** NVIDIA Jetson Orin Nano (Real-time Edge Analysis)
* **Pipeline:** Simulators → MotionX Bridge → **Inverse Motion Calculation** → Real-world Stabilization.
* **Stack:** ROS 2, Python, OpenCV (Optical Flow for visual compensation).

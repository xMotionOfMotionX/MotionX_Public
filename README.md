# MotionX: Universal Simulation Bridge
### "Write Once, Run Anywhere: Zero Code Change Robotics Middleware"

## 📺 Pilot Demo: Sim-to-Sim Data Integration
[![](https://img.youtube.com/vi/JsVlAP03GSE/0.jpg)](https://youtu.be/JsVlAP03GSE)
> *Extracting F1TENTH racing data to synchronize with Donkey Car dynamics.*

---

## 🎯 Our Mission: Simulation Interoperability
MotionX solves the **Simulator Lock-in** problem by providing a standardized middleware. We reduce the algorithm porting time from **2 weeks to less than 24 hours**.

* **Standardization:** All telemetry (G-force, Yaw, Inertia) is normalized into the MotionX data structure.
* **Zero Code Change:** Switch between F1TENTH, Donkey Car, and Isaac Sim without altering a single line of your original controller code.
* **Human-Centered Safety:** We quantify motion safety and comfort (Anti-motion sickness) as a 'Safety Index' before real-world deployment.



---

## 🛠 Current Phase: Sim-to-Sim Data Bridge
We are currently synchronizing **F1TENTH (High-speed Racing)** and **Donkey Car (Small-scale Dynamics)** to validate our "Zero Code Change" data extraction pipeline.

* **Scale Matching (Lidar 9.9x):** Adjusting spatial perception to match different environment scales.
* **Motion Telemetry:** Mapping ROS 2 topics to JSON-based simulator sockets.
* **Dynamic Response:** Real-time throttle/steering adjustment to observe physical inertia changes.

---

## 📁 Tech Highlights
* **Pipeline:** Simulators → MotionX Bridge → **Other Simulators** → Real-world Stabilization.
* **Stack:** ROS 2, JSON, C++, Python, OpenCV (Optical Flow for visual compensation).
* **Future:** Expanding the bridge to high performance robotics simulators

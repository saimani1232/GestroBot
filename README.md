# GestroBot
# Gesture-Controlled 3D Robot Interface 🤖✋

This project demonstrates a **real-time gesture recognition system** that controls a 3D humanoid robot using hand gestures. It combines **computer vision**, **machine learning**, and **real-time 3D simulation**.

---

## 🚀 Features

* **Real-time gesture detection** using webcam
* **Control a humanoid robot** in Unreal Engine via gestures
* Recognizes multiple gestures:

  * "Forward"
  * "Stop"
  * "Rally"
* Displays current gesture and corresponding keyboard keys being simulated
* Responsive, intuitive interface between gesture and robot behavior

---

## 🧠 Technologies Used

* **Python**: For gesture detection logic
* **OpenCV**: Real-time webcam video processing
* **MediaPipe**: Hand tracking and landmark detection
* **Unreal Engine**: 3D humanoid simulation (not included in repo due to size)
* **Socket/Key Simulation (optional)**: For interfacing gesture output with Unreal Engine

---

## 📂 Project Structure

```
Gesture-Controlled-Robot/
├── gesture_control.py         # Main Python file with MediaPipe + OpenCV logic
├── utils/
│   └── gesture_classifier.py  # Classifies gestures from hand landmarks
├── README.md
```

---

## 📽️ Working Demo (LinkedIn Post)

> 🔗 [Watch the live demo on LinkedIn](https://www.linkedin.com/posts/sai-mani-macherla-5a16072a2_robotics-computervision-machinelearning-activity-7331705675099635712-G1_B?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEkPmokB9dZL_6zTVI_IshOlrOfnrN2pxHw)

**Preview from the demo:**

* Left: Hand tracking and gesture recognition
* Right: Humanoid robot in Unreal Engine responding to commands

![Demo Screenshot](path/to/demo_image.png) *(add image or link here)*

---

## ⚙️ How It Works

1. OpenCV captures webcam frames
2. MediaPipe tracks hand landmarks
3. Gestures are classified using finger positions
4. Actions (like `W`, `Shift`, etc.) are triggered
5. Unreal Engine reads those inputs to move the humanoid

---

## 🔮 Future Improvements

* Add more gestures: turn left, right, jump
* Bi-hand interaction for richer control
* Sound or haptic feedback
* Remote robot control over network
* Custom gesture training using ML

---

## 📦 Note on Unreal Engine Files

Due to large file size, the Unreal Engine project is **not included** here. To view the simulation:

* Clone this repo
* Run the gesture control Python script
* Integrate with your own Unreal Engine project manually (refer to demo for idea)

If you're interested in the UE4/UE5 setup, feel free to reach out!

---

## 📫 Contact

Feel free to connect or ask questions:

* **LinkedIn**: [SaiMani](www.linkedin.com/in/sai-mani-macherla-5a16072a2)
* **GitHub**: [github.com/saimani](https://github.com/saimani1232)

---

### 🌟 If you find this helpful, don't forget to star the repo!

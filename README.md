# 🎮 AI-Based Head-Controlled Subway Surfers using Computer Vision

This project is a **hands-free game control system** that allows a user to play **Subway Surfers** using **head movements captured through a webcam**.  
Instead of using a keyboard or touch controls, the player controls the game by simply moving their head left, right, up, or down.

The project uses **computer vision and pose estimation** to make gaming more **accessible, interactive, and inclusive**.

---

## 🌟 Why I Built This Project (Motivation & Impact)

While playing **Subway Surfers** during my free time, I started thinking beyond the game itself. Most of us play games without even realizing how dependent we are on our hands. But what about people who **cannot use their hands due to paralysis or physical disabilities**? What options do they have when they are bored or want to enjoy a game?

Entertainment is important for mental well-being, yet accessibility in gaming is often ignored. This thought pushed me to build a system where **head movement alone is enough to play a game**.

This project is not just about fun. It shows how **AI and computer vision can be used to build assistive systems** using simple hardware like a webcam and open-source tools. Even small ideas like this can help make technology more inclusive.

---

## 📌 Project Overview

The system uses **MediaPipe Pose** and **OpenCV** to track the user’s **nose position**, which acts as a stable reference point for detecting head movement.

Before gameplay starts, the system performs a short **calibration step**, where the user looks straight at the camera. This position is treated as the neutral center.

Once calibrated:

- Moving the head **left or right** moves the character left or right  
- Moving the head **up** makes the character jump  
- Moving the head **down** makes the character roll  

Keyboard actions are triggered in the background, allowing natural control without touching the keyboard.

---

## 🚀 Key Features

- Real-time webcam-based head tracking  
- AI-based pose detection using MediaPipe  
- Calibration for different users and camera setups  
- Hands-free control using head movements  
- Automatic detection and activation of the game window  
- Visual feedback and FPS display  
- Simple and modular code structure  

---

## 🛠️ Technologies Used

| Purpose | Tool |
|------|------|
| Programming | Python |
| Video Processing | OpenCV |
| Pose Detection | MediaPipe Pose |
| Keyboard Simulation | pynput |
| Window Handling | pygetwindow |
| Math Operations | NumPy |

---

## 🧠 How the System Works

<img width="406" height="773" alt="image" src="https://github.com/user-attachments/assets/a7e97621-e1ee-448c-b2bb-9feeabad8cd0" />


---

## 🎯 Head Movement to Game Action Mapping

| Head Movement | Action Detected | In-Game Effect |
|--------------|---------------|---------------|
| Head moves left | LEFT | Move left |
| Head moves right | RIGHT | Move right |
| Head moves up | UP | Jump |
| Head moves down | DOWN | Roll |

---

## 🧪 Calibration Logic

To keep the system comfortable and accurate:

- Collects **30 nose position samples**
- Calculates the average as the neutral center
- Uses frame-based thresholds to reduce noise
- Applies a short cooldown to avoid repeated accidental actions

This makes the control stable and user-friendly.

---

## ⚙️ Installation & Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/pose2play-head-controlled-gaming.git
cd pose2play-head-controlled-gaming
```

### Step 2: Install Required Libraries

Ensure **Python 3.10.x** is installed on your system, then run the following command:

```bash
pip install opencv-python mediapipe numpy pynput pygetwindow
```

### Step 3: Run the Project

Once all required libraries are installed, run the main Python script using the command below:

```bash
python hand_game_control.py
```

## ▶️ How to Use

1. Open **Subway Surfers** in your browser:  
   https://poki.com/en/g/subway-surfers

2. Make sure your webcam is working properly

3. Sit comfortably and look straight at the camera during the calibration phase

4. Move your head to control the game:
   - Left / Right → Move character
   - Up → Jump
   - Down → Roll

5. Press **`q`** to exit the application


---

## Working of the project built


https://github.com/user-attachments/assets/d3355c55-bc53-4f12-b3cd-5dcabd6768a2



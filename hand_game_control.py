import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller, Key
import time
import pygetwindow as gw  # For window management

# Initialize MediaPipe Pose Detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize Keyboard Controller
keyboard = Controller()

# Window management variables
last_window_check_time = 0
window_check_interval = 2.0  # Check for window every 2 seconds
target_window = None
browser_keywords = ['Poki', 'Subway Surfers', 'Chrome', 'Firefox', 'Edge']  # Common browser window titles

# Function to find and activate the game window
def activate_game_window():
    global target_window, last_window_check_time
    
    current_time = time.time()
    
    # Only check for window periodically (to avoid performance issues)
    if current_time - last_window_check_time < window_check_interval and target_window:
        # Try to reactivate the previously found window
        try:
            if target_window.exists and not target_window.isActive:
                target_window.activate()
                time.sleep(0.05)  # Small delay for window activation
                return True
        except:
            target_window = None  # Window no longer exists
    
    # Search for the game window
    for keyword in browser_keywords:
        try:
            windows = gw.getWindowsWithTitle(keyword)
            for window in windows:
                # Check if this is likely the game window
                if keyword in ['Poki', 'Subway Surfers'] or (
                    'subway' in window.title.lower() or 'surfers' in window.title.lower()):
                    target_window = window
                    if not window.isActive:
                        window.activate()
                    time.sleep(0.05)
                    last_window_check_time = current_time
                    return True
        except Exception as e:
            print(f"Error searching for window with keyword '{keyword}': {e}")
            continue
    
    # If no specific window found, try to activate the last active window
    try:
        all_windows = gw.getAllWindows()
        if all_windows:
            # Prefer windows that look like browsers
            browser_windows = [w for w in all_windows if any(
                browser in w.title for browser in ['Chrome', 'Firefox', 'Edge', 'Safari'])]
            if browser_windows:
                target_window = browser_windows[0]
                if not target_window.isActive:
                    target_window.activate()
                time.sleep(0.05)
                last_window_check_time = current_time
                return True
    except Exception as e:
        print(f"Error in fallback window activation: {e}")
    
    return False

# Function to get FPS
def calculate_fps(prev_time):
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    return fps, prev_time

# Main loop
cap = cv2.VideoCapture(0)
prev_time = 0
last_action_time = 0
action_cooldown = 0.5  # Cooldown time between actions (in seconds)

# Add a variable to store the last action
last_action = None
action_duration = 0.5  # Duration to maintain the last action (in seconds)

# Calibration variables
calibrated = False
center_x, center_y = 0, 0
calibration_samples = []
samples_needed = 30

print("=" * 60)
print("SUBWAY SURFERS POSE CONTROL SETUP")
print("=" * 60)
print("\nINSTRUCTIONS:")
print("1. Open Subway Surfers in your browser at: https://poki.com/en/g/subway-surfers")
print("2. Start the game and get ready to play")
print("3. For calibration: Sit comfortably and look straight ahead")
print("4. Move your head to control the character:")
print("   - Left/Right: Move character left/right")
print("   - Up: Jump")
print("   - Down: Roll")
print("5. Press 'q' in the camera window to quit")
print("=" * 60)
print("\nStarting calibration... Look straight at the camera.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape
    
    # Draw center lines and detection zones
    center_x_display, center_y_display = frame_width // 2, frame_height // 2
    cv2.line(frame, (center_x_display, 0), (center_x_display, frame_height), (0, 255, 0), 2)  # Vertical line
    cv2.line(frame, (0, center_y_display), (frame_width, center_y_display), (0, 255, 0), 2)  # Horizontal line
    
    # Draw detection zones
    zone_margin = 50
    cv2.rectangle(frame, (0, 0), (center_x_display - zone_margin, center_y_display - zone_margin), (0, 100, 255), 2)  # Up-Left
    cv2.rectangle(frame, (center_x_display + zone_margin, 0), (frame_width, center_y_display - zone_margin), (0, 100, 255), 2)  # Up-Right
    cv2.rectangle(frame, (0, center_y_display + zone_margin), (center_x_display - zone_margin, frame_height), (0, 100, 255), 2)  # Down-Left
    cv2.rectangle(frame, (center_x_display + zone_margin, center_y_display + zone_margin), (frame_width, frame_height), (0, 100, 255), 2)  # Down-Right

    # Process pose detection
    results = pose.process(rgb_frame)
    action = None

    if results.pose_landmarks:
        # Extract key landmarks
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

        # Convert normalized coordinates to pixel coordinates
        nose_x, nose_y = int(nose.x * frame_width), int(nose.y * frame_height)

        # Draw landmarks
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Draw nose point
        cv2.circle(frame, (nose_x, nose_y), 10, (0, 0, 255), -1)
        
        # Calibration phase
        if not calibrated:
            calibration_samples.append((nose_x, nose_y))
            if len(calibration_samples) >= samples_needed:
                # Calculate average position for calibration
                avg_x = sum([s[0] for s in calibration_samples]) / len(calibration_samples)
                avg_y = sum([s[1] for s in calibration_samples]) / len(calibration_samples)
                center_x, center_y = int(avg_x), int(avg_y)
                calibrated = True
                print(f"\nCalibration complete! Center position: ({center_x}, {center_y})")
                print("You can now control the game with head movements!")
        else:
            # Determine action based on nose position relative to calibrated center
            mid_x, mid_y = center_x, center_y
            
            # Calculate movement thresholds (adaptive to frame size)
            x_threshold = frame_width * 0.1  # 10% of frame width
            y_threshold = frame_height * 0.1  # 10% of frame height
            
            # Check for movements
            if nose_x < mid_x - x_threshold:  # Move left
                action = "LEFT"
                cv2.putText(frame, "<-- LEFT", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            elif nose_x > mid_x + x_threshold:  # Move right
                action = "RIGHT"
                cv2.putText(frame, "RIGHT -->", (frame_width - 200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            elif nose_y < mid_y - y_threshold:  # Move up
                action = "UP"
                cv2.putText(frame, "UP", (center_x_display - 30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            elif nose_y > mid_y + y_threshold:  # Move down
                action = "DOWN"
                cv2.putText(frame, "DOWN", (center_x_display - 40, frame_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Handle actions and simulate key presses
    current_time = time.time()
    
    if calibrated and action and action != last_action and current_time - last_action_time > action_cooldown:
        # Activate game window before sending key press
        window_activated = activate_game_window()
        
        print(f"Action performed: {action}")  # Print the action in the terminal
        
        # Simulate the corresponding key press
        if action == "LEFT":
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        elif action == "RIGHT":
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        elif action == "UP":
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        elif action == "DOWN":
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        
        last_action_time = current_time
        last_action = action  # Update the last action

    # Maintain the last action for a short duration
    if current_time - last_action_time <= action_duration:
        display_action = last_action
    else:
        display_action = "None"

    # Display information on the frame
    fps, prev_time = calculate_fps(prev_time)
    
    # Status overlay
    status_y = 30
    cv2.putText(frame, f"FPS: {int(fps)}", (10, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    if calibrated:
        cv2.putText(frame, f"Action: {display_action}", (10, status_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Center: ({center_x}, {center_y})", (10, status_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, "Calibrated - Game Control ACTIVE", (frame_width - 300, status_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        calibration_progress = min(len(calibration_samples) / samples_needed * 100, 100)
        cv2.putText(frame, f"Calibrating... {int(calibration_progress)}%", (10, status_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        cv2.putText(frame, "Look straight ahead", (frame_width // 2 - 100, frame_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        # Draw calibration progress bar
        bar_width = 200
        bar_height = 20
        bar_x = frame_width // 2 - bar_width // 2
        bar_y = frame_height // 2 + 40
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), 2)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_width * calibration_progress / 100), bar_y + bar_height), (0, 200, 255), -1)

    # Show the frame
    cv2.imshow("Subway Surfers Pose Control - Press 'q' to quit", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nExiting Subway Surfers Pose Control...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Program terminated successfully.")
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time
import pydirectinput  

# Initialize pydirectinput
pydirectinput.PAUSE = 0.2  # Slight pause between key events

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Store previous hand positions for motion tracking
hand_positions = deque(maxlen=10)
index_positions = deque(maxlen=20)

# Define keyboard key mappings for each gesture
# Updated key mapping for Forward to use shift+w
GESTURE_KEY_MAPPINGS = {
    "Forward": ["shift", "w"],  # Hold shift+w key for Forward gesture
    "Stop": None,               # No key press for Stop (releases other keys)
    "Attack": "k",              # Press 'k' key for Attack gesture
    "Move Forward": "w",        # Hold 'w' for Move Forward (without shift)
    "Enemy Spotted": "j",       # Press 'j' key for Enemy Spotted
    "Cover": "c",               # Press 'c' key for Cover
    "Rally": "l",               # Press 'l' key for Rally - we'll use a simpler gesture detection
    "Unknown": None             # No key press for unknown gestures
}

# Track the currently active keys and gestures
current_gesture = "Unknown"
active_keys = set()
last_gesture_time = time.time()
gesture_cooldown = 0.5  # Cooldown time in seconds to prevent rapid switching

# Function to classify gestures based on hand landmarks
def classify_gesture(hand_landmarks):
    fingers_up = []
    
    # Define landmark indexes for fingers
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    finger_dips = [
        mp_hands.HandLandmark.INDEX_FINGER_DIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_DIP,
        mp_hands.HandLandmark.PINKY_DIP
    ]

    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    palm_base = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Check if fingers are up
    for tip, dip in zip(finger_tips, finger_dips):
        fingers_up.append(1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y else 0)

    # Store hand position for motion tracking
    hand_positions.append(wrist.z)
    index_positions.append((index_tip.x, index_tip.y))

    # Thumb condition (left or right hand)
    thumb_extended = thumb_tip.x > thumb_ip.x if thumb_tip.x > wrist.x else thumb_tip.x < thumb_ip.x

    # Gesture Classification
    if sum(fingers_up) == 0 and not thumb_extended:
        return "Forward"  # Fist - now mapped to shift+w

    elif sum(fingers_up) == 4 and thumb_extended:
        return "Stop"  # Open Palm

    elif sum(fingers_up) == 0 and thumb_extended:
        return "Attack"  # Superman-style

    elif fingers_up == [1, 0, 0, 0] and not thumb_extended:
        return "Move Forward"  # Index finger up

    elif fingers_up == [1, 1, 0, 0] and not thumb_extended:
        return "Enemy Spotted"  # Two fingers forward

    elif fingers_up == [0, 1, 1, 1] and not thumb_extended:
        return "Cover"  # Three fingers up (middle, ring, pinky)
    
    # NEW DISTINCT RALLY GESTURE: Pinky finger only (like "hang loose" without thumb)
    elif fingers_up == [1, 0, 0, 1] and not thumb_extended:
        return "Rally"  # Spider man

    return "Unknown"

# Function to control the robot with continuous key holding
def control_robot(gesture):
    global current_gesture, active_keys, last_gesture_time
    
    # Check if the gesture has changed and cooldown period has passed
    current_time = time.time()
    if (gesture != current_gesture and 
        gesture != "Unknown" and 
        current_time - last_gesture_time >= gesture_cooldown):
        
        # If the gesture is "Stop", release all currently held keys
        if gesture == "Stop":
            for key in active_keys:
                pydirectinput.keyUp(key)
            active_keys.clear()
            print(f"Action triggered: {gesture} - Released all keys")
        
        # For other gestures, handle the appropriate key presses
        else:
            key_to_press = GESTURE_KEY_MAPPINGS.get(gesture)
            
            # If this gesture needs a key press
            if key_to_press is not None:
                # For the Forward gesture that now uses shift+w
                if gesture == "Forward" and isinstance(key_to_press, list):
                    # Only press if not already pressed
                    for key in key_to_press:
                        if key not in active_keys:
                            pydirectinput.keyDown(key)
                            active_keys.add(key)
                    print(f"Action triggered: {gesture} - Holding keys: {'+'.join(key_to_press)}")
                
                # For movement keys that should be held (continuous actions)
                elif gesture == "Move Forward":
                    # Only press if not already pressed
                    if key_to_press not in active_keys:
                        pydirectinput.keyDown(key_to_press)
                        active_keys.add(key_to_press)
                        print(f"Action triggered: {gesture} - Holding key: {key_to_press}")
                
                # For action keys that should be single presses (discrete actions)
                elif gesture in ["Attack", "Enemy Spotted", "Cover", "Rally"]:
                    # Press and release for action gestures
                    pydirectinput.press(key_to_press)
                    print(f"Action triggered: {gesture} - Pressed key: {key_to_press}")
        
        # Update current gesture and time
        current_gesture = gesture
        last_gesture_time = current_time

# Start video capture
cap = cv2.VideoCapture(0)

print("Gesture Recognition Started. Press 'q' to quit.")
print("Mapped gestures:")
for gesture, key in GESTURE_KEY_MAPPINGS.items():
    if key is not None:
        if gesture == "Forward":
            print(f"- {gesture}: Holding 'shift+w' continuously")
        elif gesture == "Move Forward":
            print(f"- {gesture}: Holding 'w' continuously")
        elif gesture in ["Attack", "Enemy Spotted", "Cover", "Rally"]:
            print(f"- {gesture}: Pressing '{key}' once")
    elif gesture == "Stop":
        print(f"- {gesture}: Releasing all held keys")

# Add a visual guide for recognizing gestures
print("\nGesture Guide:")
print("- Forward: Closed fist")
print("- Stop: Open palm with all fingers extended")
print("- Attack: Closed fist with thumb extended (Superman style)")
print("- Move Forward: Only index finger extended")
print("- Enemy Spotted: Index and middle fingers extended (peace sign)")
print("- Cover: Middle, ring, and pinky fingers extended")
print("- Rally: Only pinky finger extended")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB for MediaPipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Convert frame back to BGR for OpenCV display
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # Draw status information
    cv2.putText(frame, f"Current gesture: {current_gesture}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if active_keys:
        cv2.putText(frame, f"Keys held: {', '.join(active_keys)}", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No keys pressed", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect gesture
            gesture = classify_gesture(hand_landmarks)
            
            # Control the robot based on the detected gesture
            control_robot(gesture)

            # Display detected gesture (not necessarily the active one)
            cv2.putText(frame, f"Detected: {gesture}", (10, 90), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('Gesture Recognition for Robot Control', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Release all keys before exiting
        for key in active_keys:
            pydirectinput.keyUp(key)
        break

cap.release()
cv2.destroyAllWindows()
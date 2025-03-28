import cv2
import math as m
import mediapipe as mp
import tkinter.messagebox as mb

# ============================= Helper Functions =============================#

def find_distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points."""
    if None not in [x1, y1, x2, y2]:
        return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return None

def find_angle(x1, y1, x2, y2):
    """Calculate inclination angle between two points."""
    if None not in [x1, y1, x2, y2] and y1 != 0:
        try:
            theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
            return int((180 / m.pi) * theta)
        except ValueError:
            return None
    return None

# ============================= Constants & Initializations =============================#

good_frames, bad_frames = 0, 0  # Frame counters
font = cv2.FONT_HERSHEY_SIMPLEX  # Font for text overlays

# Colours for visual feedback
COLORS = {
    "blue": (255, 127, 0), "red": (50, 50, 255), "green": (127, 255, 0),
    "dark_blue": (127, 20, 0), "light_green": (127, 233, 100),
    "yellow": (0, 255, 255), "pink": (255, 0, 255)
}

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# ============================= Main Execution =============================#

def main():
    global good_frames, bad_frames
    
    cap = cv2.VideoCapture(0)  # Open webcam
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default FPS if unavailable
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Error: Frame capture failed.")
            break
        
        h, w = image.shape[:2]  # Get frame dimensions
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe
        keypoints = pose.process(image_rgb)  # Detect landmarks
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)  # Convert back to BGR
        
        lm = keypoints.pose_landmarks
        if not lm:
            print("Warning: No landmarks detected.")
            continue
        
        # Extract key landmark coordinates
        lmPose = mp_pose.PoseLandmark
        keypoints_dict = {}
        for landmark in ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_EAR", "LEFT_HIP"]:
            key = getattr(lmPose, landmark)
            keypoints_dict[landmark] = (
                int(lm.landmark[key].x * w), int(lm.landmark[key].y * h)
            )
        
        # Calculate offsets and angles
        offset = find_distance(*keypoints_dict["LEFT_SHOULDER"], *keypoints_dict["RIGHT_SHOULDER"])
        neck_angle = find_angle(*keypoints_dict["LEFT_SHOULDER"], *keypoints_dict["LEFT_EAR"])
        torso_angle = find_angle(*keypoints_dict["LEFT_HIP"], *keypoints_dict["LEFT_SHOULDER"])
        
        # Determine posture condition
        good_posture = neck_angle is not None and torso_angle is not None and neck_angle < 35 and torso_angle < 15
        color = COLORS["green"] if good_posture else COLORS["red"]
        
        # Draw nodes and lines with conditional colors
        for landmark in keypoints_dict:
            cv2.circle(image, keypoints_dict[landmark], 5, color, -1)  # Draw nodes
        
        cv2.line(image, keypoints_dict["LEFT_SHOULDER"], keypoints_dict["RIGHT_SHOULDER"], color, 2)
        cv2.line(image, keypoints_dict["LEFT_SHOULDER"], keypoints_dict["LEFT_EAR"], color, 2)
        cv2.line(image, keypoints_dict["LEFT_HIP"], keypoints_dict["LEFT_SHOULDER"], color, 2)
        
        # Camera alignment check
        alignment_text = f"{int(offset)} Aligned" if offset and offset < 100 else f"{int(offset)} Not Aligned"
        cv2.putText(image, alignment_text, (w - 250, 30), font, 0.9, color, 2)
        
        # Posture evaluation
        posture_text = f"Neck: {neck_angle}°  Torso: {torso_angle}°" if neck_angle and torso_angle else "Posture: N/A"
        if good_posture:
            good_frames += 1
            bad_frames = 0
        else:
            bad_frames += 1
            good_frames = 0
        
        # Display text overlay
        cv2.putText(image, posture_text, (10, 30), font, 0.9, color, 2)
        
        # Pose time tracking
        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames
        time_text = f"Good Posture Time: {good_time:.1f}s" if good_time > 0 else f"Bad Posture Time: {bad_time:.1f}s"
        cv2.putText(image, time_text, (10, h - 20), font, 0.9, color, 2)
        
        # Posture warning alert
        if bad_time > 5:
            mb.showwarning("Warning", "Poor posture detected!")
            bad_frames = 0  # Reset counter after warning
        
        cv2.imshow('Posture Monitor', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

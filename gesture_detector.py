"""
Gesture Detector Module
Handles webcam capture and MediaPipe hand tracking.
"""

import cv2
import mediapipe as mp
from typing import Optional, List, Tuple
import time


class GestureDetector:
    """Detects hand landmarks from webcam feed using MediaPipe."""
    
    def __init__(self, camera_index: int = 0, 
                 min_detection_confidence: float = 0.7,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the gesture detector.
        
        Args:
            camera_index: Index of the camera to use (default: 0)
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
        """
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # Track only one hand for simplicity
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.mp_draw = mp.solutions.drawing_utils
        
    def start(self) -> bool:
        """
        Start the webcam capture.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_index}")
                return False
            
            self.running = True
            print(f"✓ Camera {self.camera_index} started successfully")
            return True
        except Exception as e:
            print(f"Error starting camera: {e}")
            return False
    
    def stop(self):
        """Stop the webcam capture and release resources."""
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✓ Camera stopped")
    
    def get_hand_landmarks(self, show_preview: bool = False) -> Optional[List[Tuple[float, float, float]]]:
        """
        Capture a frame and extract hand landmarks.
        
        Args:
            show_preview: If True, display the camera feed with landmarks
            
        Returns:
            List of 21 (x, y, z) landmark tuples, or None if no hand detected
        """
        if not self.running or not self.cap:
            return None
        
        success, frame = self.cap.read()
        if not success:
            return None
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        landmarks = None
        
        if results.multi_hand_landmarks:
            # Get the first hand's landmarks
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract normalized coordinates
            landmarks = [
                (lm.x, lm.y, lm.z) 
                for lm in hand_landmarks.landmark
            ]
            
            # Draw landmarks if preview is enabled
            if show_preview:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        # Show preview window if enabled
        if show_preview:
            cv2.imshow('Manipulus - Hand Tracking', frame)
            cv2.waitKey(1)
        
        return landmarks
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()

"""
Gesture Classifier Module
Converts hand landmarks to recognized gestures using geometric rules.
"""

from typing import Optional, List, Tuple
import time
import math


class GestureClassifier:
    """Classifies hand landmarks into gesture labels."""
    
    # MediaPipe hand landmark indices
    WRIST = 0
    THUMB_TIP = 4
    THUMB_IP = 3
    THUMB_MCP = 2
    INDEX_TIP = 8
    INDEX_PIP = 6
    INDEX_MCP = 5
    MIDDLE_TIP = 12
    MIDDLE_PIP = 10
    RING_TIP = 16
    RING_PIP = 14
    PINKY_TIP = 20
    PINKY_PIP = 18
    
    def __init__(self, debounce_seconds: float = 1.0):
        """
        Initialize the gesture classifier.
        
        Args:
            debounce_seconds: Minimum time between same gesture triggers
        """
        self.debounce_seconds = debounce_seconds
        self.last_gesture = None
        self.last_gesture_time = 0
    
    def classify(self, landmarks: Optional[List[Tuple[float, float, float]]]) -> Optional[str]:
        """
        Classify hand landmarks into a gesture.
        
        Args:
            landmarks: List of 21 (x, y, z) landmark tuples
            
        Returns:
            Gesture name ('thumbs_up', 'peace', 'open_palm', 'closed_fist') or None
        """
        if landmarks is None or len(landmarks) != 21:
            return None
        
        # Detect gesture using geometric rules
        gesture = self._detect_gesture(landmarks)
        
        # Apply debouncing
        if gesture:
            current_time = time.time()
            if gesture == self.last_gesture:
                if current_time - self.last_gesture_time < self.debounce_seconds:
                    return None  # Too soon, ignore
            
            # Update last gesture
            self.last_gesture = gesture
            self.last_gesture_time = current_time
            return gesture
        
        return None
    
    def _detect_gesture(self, landmarks: List[Tuple[float, float, float]]) -> Optional[str]:
        """
        Detect gesture from landmarks using geometric rules.
        
        Args:
            landmarks: List of 21 (x, y, z) landmark tuples
            
        Returns:
            Gesture name or None
        """
        # Check gestures in order - most specific first to avoid false positives
        
        # 1. Open Palm: All fingers extended (check first, most distinct)
        if self._is_open_palm(landmarks):
            return 'open_palm'
        
        # 2. Peace Sign: Index + middle extended, others closed
        if self._is_peace_sign(landmarks):
            return 'peace'
        
        # 3. Closed Fist: All fingers closed (check before thumbs up!)
        if self._is_closed_fist(landmarks):
            return 'closed_fist'
        
        # 4. Thumbs Up: Thumb extended up, other fingers closed (last, most prone to false positives)
        if self._is_thumbs_up(landmarks):
            return 'thumbs_up'
        
        return None
    
    def _is_finger_extended(self, landmarks: List[Tuple[float, float, float]], 
                           tip_idx: int, pip_idx: int) -> bool:
        """Check if a finger is extended by comparing tip and PIP joint positions."""
        tip = landmarks[tip_idx]
        pip = landmarks[pip_idx]
        wrist = landmarks[self.WRIST]
        
        # Calculate distances from wrist
        tip_dist = math.sqrt((tip[0] - wrist[0])**2 + (tip[1] - wrist[1])**2)
        pip_dist = math.sqrt((pip[0] - wrist[0])**2 + (pip[1] - wrist[1])**2)
        
        # Finger is extended if tip is farther from wrist than PIP joint
        return tip_dist > pip_dist * 1.1
    
    def _is_thumb_extended_up(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Check if thumb is extended upward."""
        thumb_tip = landmarks[self.THUMB_TIP]
        thumb_ip = landmarks[self.THUMB_IP]
        thumb_mcp = landmarks[self.THUMB_MCP]
        wrist = landmarks[self.WRIST]
        index_mcp = landmarks[self.INDEX_MCP]
        index_tip = landmarks[self.INDEX_TIP]
        middle_tip = landmarks[self.MIDDLE_TIP]
        
        # Thumb is up if tip is higher (lower y value) than IP and MCP
        # AND thumb tip is higher than the index finger base (more strict)
        thumb_vertical = thumb_tip[1] < thumb_ip[1] < thumb_mcp[1]
        thumb_above_index = thumb_tip[1] < index_mcp[1]
        
        # STRICT: Thumb must be significantly higher than all finger tips
        thumb_above_fingers = (thumb_tip[1] < index_tip[1] - 0.05 and 
                               thumb_tip[1] < middle_tip[1] - 0.05)
        
        # Also check thumb is reasonably far from wrist (actually extended)
        thumb_dist = math.sqrt((thumb_tip[0] - wrist[0])**2 + (thumb_tip[1] - wrist[1])**2)
        thumb_extended = thumb_dist > 0.2  # Increased threshold for stricter detection
        
        return thumb_vertical and thumb_above_index and thumb_above_fingers and thumb_extended
    
    def _is_thumbs_up(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect thumbs up gesture."""
        # VERY strict check - all conditions must be met
        thumb_up = self._is_thumb_extended_up(landmarks)
        
        # If thumb isn't clearly up, reject immediately
        if not thumb_up:
            return False
        
        index_closed = not self._is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP)
        middle_closed = not self._is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_closed = not self._is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        pinky_closed = not self._is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        # All fingers must be closed AND thumb must be up
        return index_closed and middle_closed and ring_closed and pinky_closed
    
    def _is_peace_sign(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect peace sign (V) gesture."""
        index_extended = self._is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP)
        middle_extended = self._is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_closed = not self._is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        pinky_closed = not self._is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        return index_extended and middle_extended and ring_closed and pinky_closed
    
    def _is_open_palm(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect open palm gesture."""
        index_extended = self._is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP)
        middle_extended = self._is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_extended = self._is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        pinky_extended = self._is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        return index_extended and middle_extended and ring_extended and pinky_extended
    
    def _is_closed_fist(self, landmarks: List[Tuple[float, float, float]]) -> bool:
        """Detect closed fist gesture."""
        index_closed = not self._is_finger_extended(landmarks, self.INDEX_TIP, self.INDEX_PIP)
        middle_closed = not self._is_finger_extended(landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP)
        ring_closed = not self._is_finger_extended(landmarks, self.RING_TIP, self.RING_PIP)
        pinky_closed = not self._is_finger_extended(landmarks, self.PINKY_TIP, self.PINKY_PIP)
        
        # Also ensure thumb is NOT extended upward (to distinguish from thumbs up)
        thumb_not_up = not self._is_thumb_extended_up(landmarks)
        
        return index_closed and middle_closed and ring_closed and pinky_closed and thumb_not_up

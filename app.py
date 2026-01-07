"""
Manipulus - Main Application
Desktop gesture control via webcam hand tracking.
"""

import rumps
import threading
import time
from gesture_detector import GestureDetector
from gesture_classifier import GestureClassifier
from intent_mapper import IntentMapper


class ManipulusApp(rumps.App):
    """Main application with menu bar integration."""
    
    def __init__(self):
        super(ManipulusApp, self).__init__(
            "Manipulus",
            icon="manipuluslogo.jpg",  # Use the existing logo
            quit_button=None  # We'll add custom quit
        )
        
        # Initialize components
        self.intent_mapper = IntentMapper("config.yaml")
        
        # Get settings from config
        camera_index = self.intent_mapper.get_setting('camera_index', 0)
        min_detection_confidence = self.intent_mapper.get_setting('min_detection_confidence', 0.7)
        min_tracking_confidence = self.intent_mapper.get_setting('min_tracking_confidence', 0.5)
        debounce_seconds = self.intent_mapper.get_setting('debounce_seconds', 1.0)
        self.show_preview = self.intent_mapper.get_setting('show_camera_preview', False)
        
        self.detector = GestureDetector(
            camera_index=camera_index,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.classifier = GestureClassifier(debounce_seconds=debounce_seconds)
        
        # State
        self.running = False
        self.detection_thread = None
        
        # Menu items
        self.start_button = rumps.MenuItem("Start Detection", callback=self.start_detection)
        self.stop_button = rumps.MenuItem("Stop Detection", callback=self.stop_detection)
        self.stop_button.set_callback(None)  # Disabled initially
        
        self.menu = [
            self.start_button,
            self.stop_button,
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
        
        print("✓ Manipulus initialized")
        print("  Click 'Start Detection' in menu bar to begin")
    
    def start_detection(self, _):
        """Start gesture detection."""
        if self.running:
            return
        
        print("\n=== Starting Gesture Detection ===")
        
        # Start camera
        if not self.detector.start():
            rumps.alert("Error", "Could not start camera")
            return
        
        # Update menu
        self.start_button.set_callback(None)  # Disable start
        self.stop_button.set_callback(self.stop_detection)  # Enable stop
        self.title = "Manipulus ●"  # Active indicator
        
        # Start detection loop in background thread
        self.running = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        
        print("✓ Detection started")
    
    def stop_detection(self, _):
        """Stop gesture detection."""
        if not self.running:
            return
        
        print("\n=== Stopping Gesture Detection ===")
        
        self.running = False
        
        # Wait for thread to finish
        if self.detection_thread:
            self.detection_thread.join(timeout=2.0)
        
        # Stop camera
        self.detector.stop()
        
        # Update menu
        self.start_button.set_callback(self.start_detection)  # Enable start
        self.stop_button.set_callback(None)  # Disable stop
        self.title = "Manipulus"  # Inactive
        
        print("✓ Detection stopped")
    
    def _detection_loop(self):
        """Main detection loop (runs in background thread)."""
        print("Detection loop started")
        
        while self.running:
            try:
                # Get hand landmarks
                landmarks = self.detector.get_hand_landmarks(show_preview=self.show_preview)
                
                # Classify gesture
                gesture = self.classifier.classify(landmarks)
                
                # Execute action if gesture detected
                if gesture:
                    print(f"\n🖐️  Detected: {gesture}")
                    action = self.intent_mapper.get_action(gesture)
                    
                    if action:
                        action.execute()
                    else:
                        print(f"  Warning: No action mapped for {gesture}")
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.05)  # 20 FPS
                
            except Exception as e:
                print(f"Error in detection loop: {e}")
                time.sleep(0.1)
        
        print("Detection loop ended")
    
    def quit_app(self, _):
        """Quit the application."""
        print("\n=== Shutting Down ===")
        self.stop_detection(None)
        rumps.quit_application()


def main():
    """Main entry point."""
    print("""
╔═══════════════════════════════════════╗
║                                       ║
║         MANIPULUS v2.0                ║
║    Gesture Control Interface          ║
║                                       ║
╚═══════════════════════════════════════╝
    """)
    
    app = ManipulusApp()
    app.run()


if __name__ == "__main__":
    main()

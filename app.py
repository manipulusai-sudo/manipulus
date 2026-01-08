"""
Manipulus Application Entry Point.
Initializes the menu bar interface and orchestrates the sensing pipeline.
"""
import rumps
import threading
import time
from gesture_detector import GestureDetector
from gesture_classifier import GestureClassifier
from intent_mapper import IntentMapper
from action_executor import ActionExecutor

class ManipulusApp(rumps.App):
    def __init__(self):
        super(ManipulusApp, self).__init__("Manipulus", icon="manipuluslogo.jpg")
        self.detector = GestureDetector()
        self.classifier = GestureClassifier()
        self.mapper = IntentMapper()
        self.executor = ActionExecutor()
        
        self.active = False
        self.thread = None
        
        # Menu structure
        self.menu = [
            "Start Sensing",
            "Stop Sensing",
            None,  # Separator
            "Calibration",
            "Preferences",
            None,
            "Quit"
        ]

    @rumps.clicked("Start Sensing")
    def start_sensing(self, _):
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self._run_pipeline, daemon=True)
            self.thread.start()
            print("[System] Sensing active.")

    @rumps.clicked("Stop Sensing")
    def stop_sensing(self, _):
        self.active = False
        print("[System] Sensing paused.")

    def _run_pipeline(self):
        """
        Main sensing loop.
        Acquires sensor data -> Classifies intent -> Executes action.
        """
        while self.active:
            # 1. Acquire raw sensor input
            # Implementation specific: Camera, Depth, or RF
            input_frame = self.detector.acquire_frame()
            
            # 2. Extract topology/features
            features = self.detector.process(input_frame)
            
            if features:
                # 3. Classify intent
                intent = self.classifier.classify(features)
                
                # 4. Map to system action
                if intent:
                    action = self.mapper.resolve(intent)
                    self.executor.execute(action)
            
            time.sleep(0.01)

if __name__ == "__main__":
    ManipulusApp().run()

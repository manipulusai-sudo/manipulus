"""
Test script to verify core Manipulus components work.
Run this to diagnose issues without needing the menu bar app.
"""

import sys

print("=" * 50)
print("MANIPULUS v2.0 - Component Test")
print("=" * 50)
print()

# Test 1: Imports
print("Test 1: Checking imports...")
try:
    import mediapipe
    import cv2
    import yaml
    print("  ✓ MediaPipe imported")
    print("  ✓ OpenCV imported")
    print("  ✓ PyYAML imported")
except ImportError as e:
    print(f"  ✗ Import error: {e}")
    sys.exit(1)

# Test 2: Config loading
print("\nTest 2: Loading configuration...")
try:
    from intent_mapper import IntentMapper
    mapper = IntentMapper("config.yaml")
    print(f"  ✓ Config loaded: {len(mapper.gesture_map)} gestures")
except Exception as e:
    print(f"  ✗ Config error: {e}")
    sys.exit(1)

# Test 3: Gesture detector initialization
print("\nTest 3: Initializing gesture detector...")
try:
    from gesture_detector import GestureDetector
    detector = GestureDetector(camera_index=0)
    print("  ✓ Gesture detector created")
except Exception as e:
    print(f"  ✗ Detector error: {e}")
    sys.exit(1)

# Test 4: Gesture classifier
print("\nTest 4: Initializing gesture classifier...")
try:
    from gesture_classifier import GestureClassifier
    classifier = GestureClassifier(debounce_seconds=1.0)
    print("  ✓ Gesture classifier created")
except Exception as e:
    print(f"  ✗ Classifier error: {e}")
    sys.exit(1)

# Test 5: Action executor
print("\nTest 5: Testing action executor...")
try:
    from action_executor import ActionFactory
    action = ActionFactory.create('play_pause')
    print("  ✓ Action factory works")
    print("  Testing action execution...")
    action.execute()
    print("  ✓ Action executed (check for notification)")
except Exception as e:
    print(f"  ✗ Action error: {e}")
    sys.exit(1)

# Test 6: Camera access (optional)
print("\nTest 6: Testing camera access...")
try:
    if detector.start():
        print("  ✓ Camera opened successfully")
        # Try to get one frame
        landmarks = detector.get_hand_landmarks(show_preview=False)
        if landmarks is None:
            print("  ⚠ No hand detected (this is normal)")
        else:
            print(f"  ✓ Hand detected! ({len(landmarks)} landmarks)")
        detector.stop()
        print("  ✓ Camera closed successfully")
    else:
        print("  ✗ Could not open camera")
        print("    This might be because:")
        print("    - Another app is using the camera")
        print("    - Camera permissions not granted")
        print("    - No camera available")
except Exception as e:
    print(f"  ✗ Camera error: {e}")
    detector.stop()

print("\n" + "=" * 50)
print("Component test complete!")
print("=" * 50)
print()
print("If all tests passed, the core functionality works.")
print("If you got an error running app.py, it might be:")
print("  - Menu bar app requires GUI environment")
print("  - rumps library issue")
print("  - macOS permissions")
print()
print("Try running: python app.py")
print("And check if a menu bar icon appears.")

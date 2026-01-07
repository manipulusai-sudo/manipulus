# Manipulus v2.0 - Quick Start Guide

![Gesture Reference](file:///Users/sabrish/.gemini/antigravity/brain/313bc310-9210-43c1-955e-561c38203019/gesture_reference_guide_1767723148092.png)

---

## Installation (One-Time Setup)

```bash
# Navigate to project
cd "/Users/sabrish/Desktop/Max Sat.Tech/manipulus v2.0"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running Manipulus

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the app
python app.py
```

The Manipulus icon will appear in your **menu bar**.

---

## Using Gestures

1. **Click** the Manipulus icon in menu bar
2. **Select** "Start Detection"
3. **Perform gestures** in front of your webcam
4. **Watch** for macOS notifications

### Gestures (v1 - Mocked Actions)

| Gesture | Action | What Happens |
|---------|--------|-------------|
| 👍 Thumbs Up | Play/Pause | Notification: "▶️ Play/Pause" |
| ✌️ Peace Sign | Next Track | Notification: "⏭️ Next Track" |
| ✋ Open Palm | Volume Up | Notification: "🔊 Volume Up" |
| ✊ Closed Fist | Volume Down | Notification: "🔉 Volume Down" |

> **Note:** All actions in v1 are **mocked** (notifications only). Ready to swap with real integrations.

---

## Stopping Detection

1. **Click** the Manipulus icon in menu bar
2. **Select** "Stop Detection"

The webcam light will turn off.

---

## Quitting

1. **Click** the Manipulus icon in menu bar
2. **Select** "Quit"

---

## Customization

Edit `config.yaml` to:
- Change gesture mappings
- Adjust debounce time
- Modify confidence thresholds
- Enable camera preview (for debugging)

**Restart the app** after editing config.

---

## Troubleshooting

### Camera not starting
- Check if another app is using the webcam
- Try changing `camera_index` in `config.yaml` (0, 1, 2...)

### Gestures not detected
- Ensure good lighting
- Try adjusting confidence thresholds in `config.yaml`
- Enable `show_camera_preview: true` to see hand tracking

### No notifications appearing
- Check macOS notification settings
- Ensure terminal/Python has notification permissions

---

## What's Next?

This is a **working prototype** with mocked actions. To add real integrations:

1. **Edit** `action_executor.py`
2. **Replace** mock implementations with real system calls
3. **Use** `system_control.py` utilities for media keys
4. **Test** with real apps (Spotify, Music, etc.)

See [README.md](file:///Users/sabrish/Desktop/Max%20Sat.Tech/manipulus%20v2.0/README.md) for full documentation.

---

**Built with ❤️ as a rapid prototype for invisible interfaces**

# Manipulus v2.0

**Desktop gesture control via webcam hand tracking**

An "invisible interface" that uses simple hand gestures to control your computer. No voice, no phone, no always-visible UI.

---

## Features

- 🖐️ **4 Simple Gestures**: Thumbs up, peace sign, open palm, closed fist
- 📹 **Standard Webcam**: Works with any RGB webcam
- 🔒 **Local-First**: No cloud, no analytics, no accounts
- ⚙️ **Configurable**: Easy YAML-based gesture mapping
- 🍎 **macOS Menu Bar**: Clean, minimal interface

---

## Gestures (v1)

| Gesture | Action | Description |
|---------|--------|-------------|
| 👍 **Thumbs Up** | Play/Pause | Toggle media playback |
| ✌️ **Peace Sign** | Next Track | Skip to next track |
| ✋ **Open Palm** | Volume Up | Increase system volume |
| ✊ **Closed Fist** | Volume Down | Decrease system volume |

> **Note**: All actions in v1 are **mocked** (notifications + console logs). Ready to swap with real integrations.

---

## Installation

### Prerequisites
- macOS (10.15+)
- Python 3.8+
- Webcam

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd "/Users/sabrish/Desktop/Max Sat.Tech/manipulus v2.0"
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the App

```bash
python app.py
```

The Manipulus icon will appear in your menu bar.

### Controls

1. **Click the menu bar icon**
2. **Select "Start Detection"**
3. **Perform gestures** in front of your webcam
4. **Notifications** will appear for each detected gesture
5. **Select "Stop Detection"** when done
6. **Select "Quit"** to exit

### Camera Preview (Optional)

To see the hand tracking visualization:

1. Edit `config.yaml`
2. Set `show_camera_preview: true`
3. Restart the app

---

## Configuration

Edit `config.yaml` to customize gesture mappings and settings:

```yaml
gestures:
  thumbs_up:
    action: play_pause
    description: "Play/Pause media"
  # ... add more gestures

settings:
  debounce_seconds: 1.0        # Cooldown between same gesture
  camera_index: 0              # Webcam index (0 = default)
  min_detection_confidence: 0.7
  min_tracking_confidence: 0.5
  show_camera_preview: false   # Set to true for debugging
```

---

## Project Structure

```
manipulus v2.0/
├── app.py                  # Main menu bar application
├── gesture_detector.py     # MediaPipe hand tracking
├── gesture_classifier.py   # Gesture recognition logic
├── intent_mapper.py        # Config → action mapping
├── action_executor.py      # Action implementations (mocked)
├── config.yaml            # Gesture configuration
├── requirements.txt       # Python dependencies
├── manipuluslogo.jpg      # Menu bar icon
└── README.md             # This file
```

---

## Architecture

```
Webcam → Gesture Detector → Classifier → Intent Mapper → Action Executor
                                              ↑
                                         config.yaml
```

**Clean separation of concerns:**
- **Detector**: MediaPipe hand tracking (21 landmarks)
- **Classifier**: Geometric rules → gesture labels
- **Mapper**: YAML config → action objects
- **Executor**: Mocked actions (ready for real integrations)

---

## Known Limitations

- **macOS only** (no Windows/Linux support in v1)
- **Single hand tracking** (no two-hand gestures)
- **Requires good lighting** for reliable detection
- **Static gestures only** (no swipes or dynamic motions)
- **Actions are mocked** (no real Spotify/Hue integration yet)
- **Manual config editing** (no GUI for customization)
- **Accessibility permissions** may be required for system control

---

## Future Enhancements

- Real integrations (Spotify, Philips Hue, etc.)
- Cross-platform support (Windows, Linux)
- Dynamic gestures (swipes, waves)
- Two-hand gestures
- GUI for configuration
- Custom gesture training
- Gesture history/analytics

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

## Technical Stack

- **MediaPipe** - Hand gesture recognition
- **OpenCV** - Webcam capture
- **rumps** - macOS menu bar app
- **PyObjC/Quartz** - macOS system control
- **PyYAML** - Configuration parsing

---

## License

MIT License - Feel free to hack and modify!

---

**Built with ❤️ as a rapid prototype for invisible interfaces**

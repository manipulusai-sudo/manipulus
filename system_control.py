"""
System Control Module
macOS system control utilities using Quartz/PyObjC.
Future: Replace mocked actions with real system control.
"""

try:
    from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap
    from Quartz import CGEventSourceCreate, kCGEventSourceStateHIDSystemState
    QUARTZ_AVAILABLE = True
except ImportError:
    QUARTZ_AVAILABLE = False
    print("Warning: Quartz not available. System control will be mocked.")


# Media key constants (for future use)
NX_KEYTYPE_SOUND_UP = 0
NX_KEYTYPE_SOUND_DOWN = 1
NX_KEYTYPE_MUTE = 7
NX_KEYTYPE_PLAY = 16
NX_KEYTYPE_NEXT = 17
NX_KEYTYPE_PREVIOUS = 18
NX_KEYTYPE_FAST = 19
NX_KEYTYPE_REWIND = 20


def send_media_key(key_type: int):
    """
    Send a media key event to the system.
    
    Args:
        key_type: Media key constant (e.g., NX_KEYTYPE_PLAY)
    """
    if not QUARTZ_AVAILABLE:
        print(f"[MOCK] Would send media key: {key_type}")
        return
    
    try:
        # Create event source
        source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
        
        # Create key down event
        key_down = CGEventCreateKeyboardEvent(source, key_type, True)
        # Create key up event
        key_up = CGEventCreateKeyboardEvent(source, key_type, False)
        
        # Post events
        CGEventPost(kCGHIDEventTap, key_down)
        CGEventPost(kCGHIDEventTap, key_up)
        
        print(f"✓ Sent media key: {key_type}")
    except Exception as e:
        print(f"Error sending media key: {e}")


def play_pause():
    """Send play/pause media key."""
    send_media_key(NX_KEYTYPE_PLAY)


def next_track():
    """Send next track media key."""
    send_media_key(NX_KEYTYPE_NEXT)


def previous_track():
    """Send previous track media key."""
    send_media_key(NX_KEYTYPE_PREVIOUS)


def volume_up():
    """Send volume up media key."""
    send_media_key(NX_KEYTYPE_SOUND_UP)


def volume_down():
    """Send volume down media key."""
    send_media_key(NX_KEYTYPE_SOUND_DOWN)


def mute():
    """Send mute media key."""
    send_media_key(NX_KEYTYPE_MUTE)


# Future: Add AppleScript integration for Spotify control
def spotify_play_pause():
    """
    Control Spotify via AppleScript.
    Future implementation.
    """
    import subprocess
    try:
        script = 'tell application "Spotify" to playpause'
        subprocess.run(['osascript', '-e', script], check=True)
        print("✓ Spotify play/pause")
    except Exception as e:
        print(f"Error controlling Spotify: {e}")


def spotify_next():
    """
    Skip to next track in Spotify.
    Future implementation.
    """
    import subprocess
    try:
        script = 'tell application "Spotify" to next track'
        subprocess.run(['osascript', '-e', script], check=True)
        print("✓ Spotify next track")
    except Exception as e:
        print(f"Error controlling Spotify: {e}")

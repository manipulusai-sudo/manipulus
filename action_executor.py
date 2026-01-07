"""
Action Executor Module
Abstract action interface with mocked implementations.
"""

from abc import ABC, abstractmethod
import subprocess
import os


class Action(ABC):
    """Base class for all actions."""
    
    @abstractmethod
    def execute(self):
        """Execute the action."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a human-readable description of the action."""
        pass


class PlayPauseAction(Action):
    """Play/Pause media action (mocked)."""
    
    def execute(self):
        print("[MOCK] Executing: Play/Pause")
        self._show_notification("Manipulus", "▶️ Play/Pause")
        # Future: Use AppleScript to control Spotify/Music
        # osascript -e 'tell application "Spotify" to playpause'
    
    def get_description(self) -> str:
        return "Play/Pause media"
    
    def _show_notification(self, title: str, message: str):
        """Show macOS notification."""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            print(f"Notification error: {e}")


class NextTrackAction(Action):
    """Next track action (mocked)."""
    
    def execute(self):
        print("[MOCK] Executing: Next Track")
        self._show_notification("Manipulus", "⏭️ Next Track")
        # Future: Use AppleScript to control Spotify/Music
        # osascript -e 'tell application "Spotify" to next track'
    
    def get_description(self) -> str:
        return "Next track"
    
    def _show_notification(self, title: str, message: str):
        """Show macOS notification."""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            print(f"Notification error: {e}")


class VolumeUpAction(Action):
    """Volume up action (mocked)."""
    
    def execute(self):
        print("[MOCK] Executing: Volume Up")
        self._show_notification("Manipulus", "🔊 Volume Up")
        # Future: Use system_control.py for real volume control
    
    def get_description(self) -> str:
        return "Increase volume"
    
    def _show_notification(self, title: str, message: str):
        """Show macOS notification."""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            print(f"Notification error: {e}")


class VolumeDownAction(Action):
    """Volume down action (mocked)."""
    
    def execute(self):
        print("[MOCK] Executing: Volume Down")
        self._show_notification("Manipulus", "🔉 Volume Down")
        # Future: Use system_control.py for real volume control
    
    def get_description(self) -> str:
        return "Decrease volume"
    
    def _show_notification(self, title: str, message: str):
        """Show macOS notification."""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], check=False)
        except Exception as e:
            print(f"Notification error: {e}")


class ActionFactory:
    """Factory for creating action instances."""
    
    _actions = {
        'play_pause': PlayPauseAction,
        'next_track': NextTrackAction,
        'volume_up': VolumeUpAction,
        'volume_down': VolumeDownAction,
    }
    
    @classmethod
    def create(cls, action_name: str) -> Action:
        """
        Create an action instance by name.
        
        Args:
            action_name: Name of the action (e.g., 'play_pause')
            
        Returns:
            Action instance
            
        Raises:
            ValueError: If action name is unknown
        """
        action_class = cls._actions.get(action_name)
        if not action_class:
            raise ValueError(f"Unknown action: {action_name}")
        return action_class()

"""
Intent Mapper Module
Maps gestures to action intents via configuration.
"""

import yaml
from pathlib import Path
from typing import Optional
from action_executor import Action, ActionFactory


class IntentMapper:
    """Maps gestures to actions using configuration."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the intent mapper.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.gesture_map = {}
        self.settings = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            self.gesture_map = config.get('gestures', {})
            self.settings = config.get('settings', {})
            
            print(f"✓ Loaded config from {self.config_path}")
            print(f"  Gestures: {len(self.gesture_map)}")
            
        except FileNotFoundError:
            print(f"Warning: Config file not found: {self.config_path}")
            self.gesture_map = {}
            self.settings = {}
        except Exception as e:
            print(f"Error loading config: {e}")
            self.gesture_map = {}
            self.settings = {}
    
    def get_action(self, gesture_name: str) -> Optional[Action]:
        """
        Get the action for a given gesture.
        
        Args:
            gesture_name: Name of the gesture (e.g., 'thumbs_up')
            
        Returns:
            Action instance or None if gesture not mapped
        """
        gesture_config = self.gesture_map.get(gesture_name)
        if not gesture_config:
            return None
        
        action_name = gesture_config.get('action')
        if not action_name:
            return None
        
        try:
            return ActionFactory.create(action_name)
        except ValueError as e:
            print(f"Error creating action: {e}")
            return None
    
    def get_setting(self, key: str, default=None):
        """
        Get a setting value.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def get_gesture_description(self, gesture_name: str) -> Optional[str]:
        """
        Get the description for a gesture.
        
        Args:
            gesture_name: Name of the gesture
            
        Returns:
            Description string or None
        """
        gesture_config = self.gesture_map.get(gesture_name)
        if gesture_config:
            return gesture_config.get('description')
        return None

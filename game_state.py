"""
Game state management for saving and loading character data.
"""
import json
import os
from typing import Optional
from datetime import datetime
from game import Character


class GameState:
    """Manages saving and loading game state."""
    
    def __init__(self, save_file: str = "game_state.json"):
        self.save_file = save_file
        self.character: Optional[Character] = None
        self.last_sync: Optional[str] = None
    
    def load(self) -> Character:
        """Load game state from file or create new character."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.character = Character.from_dict(data.get('character', {}))
                    self.last_sync = data.get('last_sync')
                    print(f"✓ Loaded character: {self.character.name}")
                    return self.character
            except Exception as e:
                print(f"Error loading game state: {e}")
        
        # Create new character
        self.character = Character("Brave Adventurer")
        print("✓ Created new character")
        return self.character
    
    def save(self):
        """Save game state to file."""
        if not self.character:
            return
        
        try:
            data = {
                'character': self.character.to_dict(),
                # Persist the existing last_sync value; do not update it on save.
                'last_sync': self.last_sync
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print("✓ Game saved")
        except Exception as e:
            print(f"Error saving game state: {e}")
    
    def get_last_sync(self) -> Optional[str]:
        """Get the last sync timestamp."""
        return self.last_sync

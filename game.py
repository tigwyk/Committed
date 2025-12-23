"""
Game mechanics for the dungeon crawler.
"""
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Item:
    """Represents an item in the game."""
    name: str
    type: str  # weapon, armor, consumable
    power: int
    description: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Mob:
    """Represents an enemy mob."""
    name: str
    hp: int
    max_hp: int
    level: int
    
    def take_damage(self, damage: int) -> bool:
        """Apply damage to mob. Returns True if mob is defeated."""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0


class Character:
    """Represents the player character."""
    
    LANGUAGE_CLASSES = {
        'Python': 'Wizard',
        'JavaScript': 'Rogue',
        'TypeScript': 'Rogue',
        'Java': 'Paladin',
        'C++': 'Warrior',
        'C': 'Warrior',
        'Go': 'Ranger',
        'Rust': 'Blacksmith',
        'Ruby': 'Bard',
        'PHP': 'Necromancer',
        'C#': 'Cleric',
        'Swift': 'Monk',
        'Kotlin': 'Samurai',
    }
    
    LANGUAGE_RACES = {
        'Python': 'Human',
        'JavaScript': 'Halfling',
        'TypeScript': 'Halfling',
        'Java': 'Dwarf',
        'C++': 'Orc',
        'C': 'Orc',
        'Go': 'Elf',
        'Rust': 'Dwarf',
        'Ruby': 'Gnome',
        'PHP': 'Undead',
        'C#': 'Human',
        'Swift': 'Elf',
        'Kotlin': 'Half-Elf',
    }
    
    def __init__(self, name: str = "Adventurer"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.hp = 100
        self.max_hp = 100
        self.character_class = "Commoner"
        self.race = "Unknown"
        self.inventory: List[Item] = []
        self.stats = {
            'total_commits': 0,
            'total_damage_dealt': 0,
            'mobs_defeated': 0,
            'items_collected': 0,
            'merge_requests_approved': 0
        }
        self.current_mob: Optional[Mob] = None
    
    def determine_class_race(self, language_stats: Dict[str, int]):
        """Determine character class and race based on most used programming language."""
        if not language_stats:
            return
        
        # Find most used language
        primary_language = max(language_stats, key=language_stats.get)
        
        # Set class and race based on language
        self.character_class = self.LANGUAGE_CLASSES.get(primary_language, "Adventurer")
        self.race = self.LANGUAGE_RACES.get(primary_language, "Human")
    
    def xp_for_next_level(self) -> int:
        """Calculate XP needed for next level."""
        return 100 * (self.level ** 1.5)
    
    def add_xp(self, amount: int):
        """Add XP and handle level ups."""
        self.xp += amount
        
        while self.xp >= self.xp_for_next_level():
            self.level_up()
    
    def level_up(self):
        """Level up the character."""
        xp_needed = int(self.xp_for_next_level())
        self.xp -= xp_needed
        self.level += 1
        
        # Increase max HP
        hp_increase = random.randint(5, 15)
        self.max_hp += hp_increase
        self.hp = self.max_hp
        
        print(f"🎉 LEVEL UP! You are now level {self.level}!")
        print(f"   Max HP increased by {hp_increase}!")
    
    def spawn_mob(self):
        """Spawn a new mob to fight."""
        mob_types = [
            ("Goblin", 20, 1),
            ("Skeleton", 30, 2),
            ("Orc", 50, 3),
            ("Troll", 80, 4),
            ("Dragon", 150, 5),
        ]
        
        # Choose mob based on player level
        suitable_mobs = [m for m in mob_types if m[2] <= self.level + 1]
        if suitable_mobs:
            mob_data = random.choice(suitable_mobs)
            hp = mob_data[1] + (self.level * 5)
            self.current_mob = Mob(
                name=mob_data[0],
                hp=hp,
                max_hp=hp,
                level=mob_data[2]
            )
    
    def attack_mob(self, damage: int) -> Optional[Item]:
        """
        Attack the current mob with damage.
        Returns an item if mob is defeated, None otherwise.
        """
        if not self.current_mob:
            self.spawn_mob()
        
        defeated = self.current_mob.take_damage(damage)
        self.stats['total_damage_dealt'] += damage
        
        if defeated:
            self.stats['mobs_defeated'] += 1
            
            # Grant XP
            xp_gained = self.current_mob.level * 25
            self.add_xp(xp_gained)
            
            # Random chance for item drop
            item = None
            if random.random() < 0.3:  # 30% chance
                item = self._generate_random_item()
                self.add_item(item)
            
            # Spawn new mob
            old_mob_name = self.current_mob.name
            self.spawn_mob()
            
            return item
        
        return None
    
    def add_item(self, item: Item):
        """Add an item to inventory."""
        self.inventory.append(item)
        self.stats['items_collected'] += 1
    
    def add_special_item(self, mr_title: str) -> Item:
        """Create a special item from a merge request approval."""
        item_types = ['weapon', 'armor', 'consumable']
        item_type = random.choice(item_types)
        
        power = random.randint(5, 20) + (self.level * 2)
        
        # Generate item name based on MR title
        prefixes = ['Legendary', 'Epic', 'Rare', 'Magical', 'Enchanted']
        prefix = random.choice(prefixes)
        
        if item_type == 'weapon':
            base_names = ['Sword', 'Axe', 'Staff', 'Bow', 'Dagger']
        elif item_type == 'armor':
            base_names = ['Helmet', 'Chestplate', 'Boots', 'Shield', 'Gauntlets']
        else:
            base_names = ['Potion', 'Elixir', 'Scroll', 'Tome', 'Amulet']
        
        item_name = f"{prefix} {random.choice(base_names)}"
        
        item = Item(
            name=item_name,
            type=item_type,
            power=power,
            description=f"Forged from the approval: {mr_title[:50]}"
        )
        
        self.add_item(item)
        self.stats['merge_requests_approved'] += 1
        
        return item
    
    def _generate_random_item(self) -> Item:
        """Generate a random item drop."""
        item_types = ['weapon', 'armor', 'consumable']
        item_type = random.choice(item_types)
        
        power = random.randint(1, 10) + self.level
        
        if item_type == 'weapon':
            names = ['Rusty Sword', 'Wooden Staff', 'Short Bow', 'Iron Dagger']
        elif item_type == 'armor':
            names = ['Leather Cap', 'Cloth Armor', 'Wooden Shield', 'Iron Boots']
        else:
            names = ['Health Potion', 'Mana Potion', 'Scroll of Knowledge']
        
        return Item(
            name=random.choice(names),
            type=item_type,
            power=power,
            description=f"A {item_type} found after battle"
        )
    
    def to_dict(self) -> Dict:
        """Convert character to dictionary for saving."""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'character_class': self.character_class,
            'race': self.race,
            'inventory': [item.to_dict() for item in self.inventory],
            'stats': self.stats,
            'current_mob': {
                'name': self.current_mob.name,
                'hp': self.current_mob.hp,
                'max_hp': self.current_mob.max_hp,
                'level': self.current_mob.level
            } if self.current_mob else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """Create character from dictionary."""
        char = cls(data.get('name', 'Adventurer'))
        char.level = data.get('level', 1)
        char.xp = data.get('xp', 0)
        char.hp = data.get('hp', 100)
        char.max_hp = data.get('max_hp', 100)
        char.character_class = data.get('character_class', 'Commoner')
        char.race = data.get('race', 'Unknown')
        
        # Load inventory
        char.inventory = [
            Item(**item_data) for item_data in data.get('inventory', [])
        ]
        
        char.stats = data.get('stats', {
            'total_commits': 0,
            'total_damage_dealt': 0,
            'mobs_defeated': 0,
            'items_collected': 0,
            'merge_requests_approved': 0
        })
        
        # Load current mob
        mob_data = data.get('current_mob')
        if mob_data:
            char.current_mob = Mob(**mob_data)
        
        return char

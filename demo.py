#!/usr/bin/env python3
"""
Demo script to test game mechanics with simulated GitLab activity.
This can be used to demonstrate the game without actual GitLab credentials.
"""
import json
from game import Character, Item
from game_state import GameState


def simulate_commits(character, num_commits):
    """Simulate processing commits."""
    print(f"\n🔄 Simulating {num_commits} commit(s)...")
    
    for i in range(num_commits):
        damage = 10 + (character.level * 2)
        
        if not character.current_mob:
            character.spawn_mob()
            print(f"   🐉 A wild {character.current_mob.name} appears!")
        
        item = character.attack_mob(damage)
        character.stats['total_commits'] += 1
        
        if item:
            print(f"   💥 You dealt {damage} damage and defeated the {character.current_mob.name}!")
            print(f"   🎁 Item dropped: {item.name}")
        else:
            print(f"   ⚔️  You dealt {damage} damage! ({character.current_mob.name} HP: {character.current_mob.hp}/{character.current_mob.max_hp})")


def simulate_merge_request_approval(character, mr_title):
    """Simulate a merge request approval."""
    print(f"\n✅ Merge Request Approved: {mr_title}")
    item = character.add_special_item(mr_title)
    print(f"   🌟 Special item obtained: {item.name} (Power: {item.power})")


def display_character_info(character):
    """Display detailed character info."""
    print("\n" + "=" * 60)
    print("📜 CHARACTER INFO:")
    print(f"   Name: {character.name}")
    print(f"   Race: {character.race} | Class: {character.character_class}")
    print(f"   Level: {character.level} | XP: {character.xp}/{int(character.xp_for_next_level())}")
    print(f"   HP: {character.hp}/{character.max_hp}")
    print("=" * 60)


def display_stats(character):
    """Display character stats."""
    print("\n📊 STATISTICS:")
    print(f"   Total Commits: {character.stats['total_commits']}")
    print(f"   Total Damage Dealt: {character.stats['total_damage_dealt']}")
    print(f"   Mobs Defeated: {character.stats['mobs_defeated']}")
    print(f"   Merge Requests Approved: {character.stats['merge_requests_approved']}")
    print(f"   Items Collected: {character.stats['items_collected']}")


def display_inventory(character):
    """Display inventory."""
    print("\n🎒 INVENTORY (Last 10 items):")
    if not character.inventory:
        print("   (empty)")
    else:
        for i, item in enumerate(character.inventory[-10:], 1):
            print(f"   {i}. {item.name} ({item.type}) - Power: {item.power}")


def main():
    """Run the demo."""
    print("=" * 60)
    print("  ⚔️  COMMITTED: Demo Mode  ⚔️")
    print("=" * 60)
    
    # Create a fresh character for the demo
    character = Character("Demo Hero")
    
    # Simulate language detection (Python developer)
    print("\n🔍 Analyzing your coding style...")
    language_stats = {'Python': 65, 'JavaScript': 20, 'Go': 15}
    character.determine_class_race(language_stats)
    print(f"   ✨ Your class has been determined: {character.race} {character.character_class}")
    
    display_character_info(character)
    
    # Simulate some commits
    print("\n" + "-" * 60)
    print("Scenario 1: Processing 5 commits")
    print("-" * 60)
    simulate_commits(character, 5)
    
    display_character_info(character)
    display_stats(character)
    
    # Simulate merge request approvals
    print("\n" + "-" * 60)
    print("Scenario 2: Approving merge requests")
    print("-" * 60)
    simulate_merge_request_approval(character, "Add authentication system")
    simulate_merge_request_approval(character, "Fix critical bug in payment processing")
    
    # More commits to level up
    print("\n" + "-" * 60)
    print("Scenario 3: Processing 20 more commits")
    print("-" * 60)
    simulate_commits(character, 20)
    
    display_character_info(character)
    display_stats(character)
    display_inventory(character)
    
    # Show current enemy
    if character.current_mob:
        print("\n⚔️  CURRENT ENEMY:")
        mob = character.current_mob
        hp_bar_length = 20
        hp_percentage = mob.hp / mob.max_hp
        filled = int(hp_bar_length * hp_percentage)
        bar = "█" * filled + "░" * (hp_bar_length - filled)
        print(f"   {mob.name} (Level {mob.level})")
        print(f"   HP: [{bar}] {mob.hp}/{mob.max_hp}")
    
    # Save the demo character
    print("\n" + "-" * 60)
    save_option = input("\nSave demo character? (y/n): ").strip().lower()
    if save_option == 'y':
        game_state = GameState("demo_save.json")
        game_state.character = character
        game_state.save()
        print("✓ Demo character saved to demo_save.json")
    
    print("\n" + "=" * 60)
    print("Demo complete! Try running './committed.py' with real GitLab credentials!")
    print("=" * 60)


if __name__ == "__main__":
    main()

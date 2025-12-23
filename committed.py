#!/usr/bin/env python3
"""
Committed - A GitLab Activity Dungeon Crawler
"""
import os
import sys
from dotenv import load_dotenv
from gitlab_client import GitLabClient
from game import Character, Item
from game_state import GameState


def display_header():
    """Display the game header."""
    print("=" * 60)
    print("  ⚔️  COMMITTED: The GitLab Dungeon Crawler  ⚔️")
    print("=" * 60)
    print()


def display_character(character: Character):
    """Display character information."""
    print("\n📜 CHARACTER INFO:")
    print(f"   Name: {character.name}")
    print(f"   Race: {character.race} | Class: {character.character_class}")
    print(f"   Level: {character.level} | XP: {character.xp}/{int(character.xp_for_next_level())}")
    print(f"   HP: {character.hp}/{character.max_hp}")
    print()


def display_current_mob(character: Character):
    """Display current mob status."""
    if character.current_mob:
        mob = character.current_mob
        hp_bar_length = 20
        hp_percentage = mob.hp / mob.max_hp
        filled = int(hp_bar_length * hp_percentage)
        bar = "█" * filled + "░" * (hp_bar_length - filled)
        
        print("\n⚔️  CURRENT ENEMY:")
        print(f"   {mob.name} (Level {mob.level})")
        print(f"   HP: [{bar}] {mob.hp}/{mob.max_hp}")
        print()


def display_stats(character: Character):
    """Display character statistics."""
    print("\n📊 STATISTICS:")
    print(f"   Total Commits: {character.stats['total_commits']}")
    print(f"   Total Damage Dealt: {character.stats['total_damage_dealt']}")
    print(f"   Mobs Defeated: {character.stats['mobs_defeated']}")
    print(f"   Merge Requests Approved: {character.stats['merge_requests_approved']}")
    print(f"   Items Collected: {character.stats['items_collected']}")
    print()


def display_inventory(character: Character):
    """Display character inventory."""
    print("\n🎒 INVENTORY:")
    if not character.inventory:
        print("   (empty)")
    else:
        for i, item in enumerate(character.inventory[-10:], 1):  # Show last 10 items
            print(f"   {i}. {item.name} ({item.type}) - Power: {item.power}")
            if item.description:
                print(f"      {item.description}")
    print()


def sync_with_gitlab(client: GitLabClient, character: Character, last_sync: str = None):
    """Sync with GitLab and process activities."""
    print("\n🔄 Syncing with GitLab...")
    
    # Get language stats and determine class/race if not set
    if character.character_class == "Commoner":
        print("   Analyzing your coding style...")
        language_stats = client.get_language_stats()
        if language_stats:
            character.determine_class_race(language_stats)
            print(f"   ✨ Your class has been determined: {character.race} {character.character_class}")
    
    # Process commits (damage to mobs)
    commits = client.get_recent_commits(since=last_sync)
    total_commits = sum(c.get('commit_count', 1) for c in commits)
    
    if total_commits > 0:
        print(f"\n   📝 Found {total_commits} new commit(s)!")
        character.stats['total_commits'] += total_commits
        
        # Each commit does damage
        for commit in commits:
            commit_count = commit.get('commit_count', 1)
            for _ in range(commit_count):
                damage = 10 + (character.level * 2)
                
                if not character.current_mob:
                    character.spawn_mob()
                    print(f"\n   🐉 A wild {character.current_mob.name} appears!")
                
                item = character.attack_mob(damage)
                
                if item:
                    print(f"   💥 You dealt {damage} damage and defeated the {character.current_mob.name}!")
                    print(f"   🎁 Item dropped: {item.name}")
                else:
                    print(f"   ⚔️  You dealt {damage} damage to the {character.current_mob.name}!")
    
    # Process merge request approvals (special items)
    approvals = client.get_approved_merge_requests(since=last_sync)
    
    if approvals:
        print(f"\n   ✅ Found {len(approvals)} approved merge request(s)!")
        
        for approval in approvals:
            item = character.add_special_item(approval.get('target_title', 'Unknown MR'))
            print(f"   🌟 Special item obtained: {item.name} (Power: {item.power})")
    
    if total_commits == 0 and not approvals:
        print("   No new activity found.")
    
    print("\n✓ Sync complete!")


def main():
    """Main game loop."""
    # Load environment variables
    load_dotenv()
    
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    gitlab_username = os.getenv('GITLAB_USERNAME')
    
    display_header()
    
    # Check for GitLab credentials
    if not gitlab_token or not gitlab_username:
        print("⚠️  GitLab credentials not found!")
        print("\nTo get started:")
        print("1. Copy .env.example to .env")
        print("2. Add your GitLab personal access token and username")
        print("3. Run the game again")
        print("\nFor now, you can explore the game in demo mode (no sync).\n")
        
        use_demo = input("Continue in demo mode? (y/n): ").strip().lower()
        if use_demo != 'y':
            return
        
        client = None
    else:
        client = GitLabClient(gitlab_url, gitlab_token, gitlab_username)
    
    # Load or create game state
    game_state = GameState()
    character = game_state.load()
    
    # Ensure character has a mob
    if not character.current_mob:
        character.spawn_mob()
    
    # Main menu loop
    while True:
        print("\n" + "─" * 60)
        print("MAIN MENU:")
        print("  1. View Character")
        print("  2. View Current Enemy")
        print("  3. View Statistics")
        print("  4. View Inventory")
        if client:
            print("  5. Sync with GitLab")
        print("  0. Save and Exit")
        print("─" * 60)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            display_character(character)
        elif choice == '2':
            display_current_mob(character)
        elif choice == '3':
            display_stats(character)
        elif choice == '4':
            display_inventory(character)
        elif choice == '5' and client:
            last_sync = game_state.get_last_sync()
            sync_with_gitlab(client, character, last_sync)
            game_state.save()
        elif choice == '0':
            game_state.save()
            print("\n👋 Thanks for playing! Your progress has been saved.")
            print("   Keep committing to grow stronger! ⚔️\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Don't forget to save next time!")
        sys.exit(0)

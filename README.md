# ⚔️ Committed - The GitLab Dungeon Crawler

A dungeon crawler game that transforms your GitLab activity into epic adventures! Your commits damage monsters, approved merge requests drop legendary items, and your character grows stronger with every contribution to your projects.

## 🎮 Features

- **Character Progression**: Level up your character based on your GitLab activity
- **Dynamic Class System**: Your character class and race are determined by your primary programming language
- **Combat System**: Each commit damages enemies in the dungeon
- **Loot System**: Approved merge requests grant special items
- **Persistent State**: Your character progress is saved between sessions
- **Real GitLab Integration**: Syncs with GitLab API to track your actual activity

## 🏆 Game Mechanics

### Character Classes & Races

Your character's class and race are automatically determined by your most-used programming language:

- **Python** → Human Wizard
- **JavaScript/TypeScript** → Halfling Rogue
- **Java** → Dwarf Paladin
- **C/C++** → Orc Warrior
- **Go** → Elf Ranger
- **Rust** → Dwarf Blacksmith
- **Ruby** → Gnome Bard
- **PHP** → Undead Necromancer
- **C#** → Human Cleric
- **Swift** → Elf Monk
- **Kotlin** → Half-Elf Samurai

### Progression

- **Commits**: Each commit deals 10 + (Level × 2) damage to enemies
- **Defeating Mobs**: Grants XP and has a chance to drop items
- **Approved Merge Requests**: Reward special legendary items
- **Level Up**: Increases max HP and unlocks stronger enemies

### Enemies

As you level up, you'll encounter increasingly powerful foes:
- Goblins (Level 1)
- Skeletons (Level 2)
- Orcs (Level 3)
- Trolls (Level 4)
- Dragons (Level 5+)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- A GitLab account with a personal access token

### Installation

1. Clone this repository:
```bash
git clone https://github.com/tigwyk/Committed.git
cd Committed
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your GitLab credentials:
```bash
cp .env.example .env
```

4. Edit `.env` and add your GitLab information:
```
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=your_personal_access_token_here
GITLAB_USERNAME=your_gitlab_username
```

### Getting a GitLab Personal Access Token

1. Go to GitLab (https://gitlab.com or your instance)
2. Click on your avatar → Preferences
3. Navigate to Access Tokens
4. Create a new token with `read_api` scope
5. Copy the token to your `.env` file

### Running the Game

```bash
python committed.py
```

Or make it executable and run directly:
```bash
chmod +x committed.py
./committed.py
```

### Try the Demo

Want to see the game in action without setting up GitLab credentials? Run the demo script:

```bash
python demo.py
```

The demo simulates GitLab activity (commits and merge request approvals) to showcase the game mechanics, character progression, combat system, and item collection.

## 🎯 How to Play

1. **Start the game**: Run `python committed.py`
2. **View your character**: See your stats, class, and level
3. **Check your enemy**: See the current monster you're fighting
4. **Sync with GitLab**: Fetch your recent activity and process it
   - Your commits will damage the current enemy
   - Defeating enemies grants XP and items
   - Approved merge requests give special legendary items
5. **Level up**: Gain XP to increase your power
6. **Collect items**: Build your inventory from drops and approvals

### Menu Options

- **View Character**: Display character stats, level, XP, and HP
- **View Current Enemy**: See the monster you're currently battling
- **View Statistics**: Check your total commits, damage dealt, and more
- **View Inventory**: Browse your collected items
- **Sync with GitLab**: Fetch and process your recent GitLab activity
- **Save and Exit**: Save your progress and quit the game

## 📊 Statistics Tracked

- Total commits processed
- Total damage dealt
- Mobs defeated
- Merge requests approved
- Items collected

## 🎨 Demo Mode

If you don't have GitLab credentials configured, you can still explore the game in demo mode. You won't be able to sync with GitLab, but you can view the character system and game mechanics.

## 🔮 Future Ideas

- Multiple character save slots
- More enemy types and boss battles
- Equipment system with equipped items
- Skill trees based on programming languages
- Party system for team projects
- Achievements and quests
- Integration with other platforms (GitHub, Bitbucket)

## 🛠️ Technical Details

### Project Structure

```
Committed/
├── committed.py       # Main game application (CLI)
├── demo.py           # Demo script with simulated GitLab activity
├── game.py           # Game mechanics (Character, Mob, Item classes)
├── game_state.py     # Save/load functionality
├── gitlab_client.py  # GitLab API integration
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment configuration
└── README.md         # This file
```

### Dependencies

- `requests`: HTTP library for GitLab API calls
- `python-dotenv`: Environment variable management

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 🎮 Have Fun!

Keep committing, keep adventuring, and may your code be bug-free! ⚔️
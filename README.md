# Stardew Balley 🌾

A parody farming game inspired by Stardew Valley, built with Pygame!

## Features

- **Tool System**: Use different tools to interact with your farm
  - **Hoe**: Till soil to prepare for planting
  - **Watering Can**: Water your crops to help them grow
  - **Axe**: Chop down trees for wood

- **Farming Mechanics**: 
  - Till soil with the hoe
  - Plant seeds (corn, tomato, wheat)
  - Water crops to make them grow
  - Watch your plants mature from seedlings to harvestable crops

- **Inventory System**: 
  - Track harvested crops
  - Collect wood from trees
  - Earn money from chopping trees

- **Interactive World**:
  - Trees that can be chopped down
  - Rocks and fences for obstacles
  - Collision detection
  - Camera system that follows the player

- **Day/Night Cycle**: Water dries up after each day cycle

## Controls

### Movement
- **Arrow Keys** - Move your character (Up, Down, Left, Right)

### Actions
- **SPACE** - Use currently selected tool
- **CTRL** - Plant currently selected seed

### Selection
- **Q** - Change tool (cycle through: hoe → axe → water)
- **E** - Change seed (cycle through: corn → tomato → wheat)

## How to Play

1. **Start Farming**: 
   - Press **Q** to select the hoe
   - Press **SPACE** to till the soil (creates brown tiles)

2. **Plant Seeds**:
   - Press **E** to select your desired seed type
   - Stand on tilled soil
   - Press **CTRL** to plant

3. **Water Your Crops**:
   - Press **Q** to select the watering can
   - Press **SPACE** on planted seeds to water them
   - Crops only grow when watered!

4. **Harvest Trees**:
   - Press **Q** to select the axe
   - Stand near a tree
   - Press **SPACE** to chop (takes 3 hits)
   - Earn wood and money!

5. **Watch Your Crops Grow**:
   - Watered plants will gradually grow
   - They go through stages: seedling → growing → mature
   - Mature plants are ready to harvest (golden appearance)

## Installation

1. **Install Python 3** (if not already installed)

2. **Clone or download this repository**

3. **Install SDL dependencies** (macOS):
   ```bash
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
   ```

4. **Create and activate virtual environment**:
   ```bash
   cd vardew-stalley
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install Pygame**:
   ```bash
   pip install pygame
   ```

6. **Run the game**:
   ```bash
   cd code
   python main.py
   ```

## Game Architecture

- `main.py` - Main game loop and initialization
- `level.py` - Game world, sprite management, and camera system
- `player.py` - Player character with movement, tools, and inventory
- `soil.py` - Farming system (soil tilling, planting, watering, crop growth)
- `sprites.py` - Game objects (trees, rocks, fences)
- `overlay.py` - UI display (tools, seeds, inventory, money, controls)
- `settings.py` - Game configuration and constants

## Tips

- Water your crops every day for them to grow
- Trees take 3 hits with the axe to chop down
- Each tree gives you 2-5 wood pieces and $10
- Watch your money and inventory in the top-right corner
- Plan your farm layout before planting!

## Future Enhancements

Potential features to add:
- Crop harvesting mechanics
- More crop varieties
- Shop system to buy seeds
- Save/load functionality
- Seasons and weather
- NPCs and dialogue
- More tools and buildings
- Day counter and calendar

## Credits

Created as a parody of Stardew Valley
Built with Pygame

Enjoy farming! 🌱

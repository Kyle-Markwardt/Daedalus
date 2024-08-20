# Labyrinth AI Training Environment

This project aims to create an environment for training an AI to play the board game Labyrinth. The environment simulates the game mechanics, including the board setup, tile pushing, player movement, and token collection.

## Project Overview

### Completed Features

- **Game Board**: The game board is initialized with tiles and tokens.
- **Place Tokens**: Tokens are placed on the board, with fixed and movable tiles correctly assigned.
- **Enable Tile Pushing**: Players can push tiles onto the board, moving rows or columns.
- **Create Player**: Player objects are created with initial positions and a hand of cards.
- **Player Tile Push**: Players can select a tile to push and execute the push action.
- **Player Move**: Players can move their piece along valid paths on the board.
- **LabyrinthEnv Outline**: A rough outline of the LabyrinthEnv class has been created to manage the game environment.
- ~~**Edge-to-Edge Jumping**: Allow players to move from one edge of the board to the opposite edge if paths are open.~~ These were my house rules, apparently not explicitly clarified in game rules but diagram showing valid moves does not include this ability.
- **Deal Cards**: Implement the card dealing mechanism for players.
- **Multiple Players**: Extend the environment to support multiple players.
- **Collect Tokens**: Enable players to collect tokens when landing on corresponding tiles.


### To-Do List

- **Fix Free Tile Display**: Currently, except for straight path tiles, the inserted piece orientation matches neither the default path orientation nor the displayed excess tile.
- **Validate Piece Movement**: Implement logic to ensure players can only move along valid paths.
- **Move Player Pieces With Tiles**: Currently pushing the row a player is on does not push the Player piece with the tile they are on.
- **Handle Player Piece Pushed Off Edge**: Implement logic to handle scenarios where a player's piece is pushed off the edge of the board.
- **Return to Home Base**: Implement the logic for players to return to their home base after collecting all tokens.
- **End Game Logic**: End game when one player has collected all tokens and returned to base.
- **Implement Scoring Weights for AI Training**: Decide and implement training weights for collecting tokens and winning the game.
- **Optimize for AI Training**: Remove or separate some debugging and visualization tools, as well as streamlining input commands.
- **Create and Train AI Agents**: Develop AI agents and train them using the environment.
- **Make Board Prettier**: Include wider paths, background image on tiles, card images.
- **Improve User Interface**: Make better commands and visualization for human users.
- **Select Number of Players and Number of AI**: Allow users to select players and AI agents.
- **Host?**: Considering making a streamlit app or something.

## Getting Started

### Prerequisites

- Python 3.11
- Required libraries: `random`, `collections`, `matplotlib`, `numpy`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kyle-Markwardt/Daedalus.git
   cd Daedalus
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to modify the README as the project progresses and additional features are implemented.

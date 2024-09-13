# Snake Game
This project implements a simple snake game using Pygame.

## Getting Started
1. Ensure you have Python and Pygame installed.
2. Clone the repository or download the files.
3. Run `main.py` to start the game.

## Requirements
- Python 3.x
- Pygame library

## Controls
- Use the arrow keys to control the snake's direction.
- The game ends when the snake collides with the wall or itself. After that, a 'Game Over' screen will display for 2 seconds.

## Project Structure
- `main.py`: Entry point for the Snake game application.
- `game.py`: Contains main game logic and periodic updates, including the definitions for the `Snake`, `Food`, and `Game` classes.
- `settings.py`: Configuration settings for the game, defining constants like screen width, height, snake size, and FPS.
- `utils.py`: Utility functions for the game, such as for drawing the grid and displaying the score.
- `README.md`: Documentation for the project, describing how to set it up and run it.
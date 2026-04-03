# Advanced Shooter Game

A Python-based desktop game built with Pygame to demonstrate advanced coding skills.

## Features

- Player-controlled spaceship with 4-directional movement and shooting cooldown
- Multiple enemy types: Fast, Slow (tougher), Tank (very tough)
- Power-ups: Health boosts and speed increases
- Scoring system with level progression
- High score persistence
- Collision detection and health system
- Game over screen with restart option
- Smooth 60 FPS gameplay

## Assets

The game uses free assets from [Kenney's Space Shooter Redux pack](https://opengameart.org/content/space-shooter-redux) (CC0 license), including:
- Player spaceship sprites
- Enemy ship sprites
- Laser bullet sprites
- Power-up sprites
- Background images
- Sound effects: laser shots, explosions, power-up collection, game over

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   python main.py
   ```

## Controls

- Arrow keys: Move
- Spacebar: Shoot (hold for continuous fire)

## Game Mechanics

- Destroy enemies to gain points
- Power-ups drop randomly from defeated enemies
- Advance levels by reaching score thresholds
- Game ends when health reaches zero
- High score is saved between sessions

## Future Enhancements

- Sound effects and background music
- More power-up types
- Boss enemies
- Multiple weapons
- Particle effects

This project showcases advanced Python skills including object-oriented programming, game state management, file I/O, sprite collision, and UI rendering.
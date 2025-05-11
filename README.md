# Master Planet

*A 2‑D Battle Game built with Pygame*&#x20;

## Table of Contents

1. [Contributors](#contributors)
2. [Description](#description)
3. [Key Features](#key-features)
4. [Technologies Used](#technologies-used)
5. [Installation](#installation)
6. [How to Run](#how-to-run)
7. [Technical Documentation](#technical-documentation)

---

## Contributors

| Name            |
| --------------- |
| Oscar Dubreuil  |
| Romain Peloux   |
| Laure Szymanski |
| Adrian Rubem    |
| Thomas Pak      |
---

## Description

This project is a side‑scrolling artillery game featuring two **Players**. Players drag‑to‑aim and release to fire daggers or axes.  Smooth camera work, multiple maps, and polished UI elements create an engaging mini‑game suitable for coursework at *Efrei Paris Panthéon‑Assas*.

---

## Key Features

* Character & weapon selection menu
* Three themed maps generated from a tile‑based `generate_map` function
* Mouse drag‑to‑aim mechanic with realistic projectile physics
* Smart camera that zooms out for cinematic shots and pans to keep action centred
* Health bars and basic particle/sound effects
* Modular object‑oriented architecture (Player, Master, Projectile, Camera)

---

## Technologies Used

| Technology                    | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| **Python ≥ 3.9**              | Core programming language                   |
| **Pygame ≥ 2.1**              | Rendering, event handling, sprites          |
| `math`, `itertools`, `typing` | Standard‑lib helpers                        |
| Custom assets                 | PNG sprites, JPG backgrounds, WAV/OGG audio |

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/https://github.com/ChuteSpyro/ProjetTransverse
   cd <repo>
   ```
2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   # Linux / macOS
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```
3. **Install Pygame (unique dependence)**

   ```bash
   pip install pygame
   ```

---

## How to Run

```bash
python main.py
```

### Controls

| Action         | Input                                |
| -------------- | ------------------------------------ |
| Navigate menus | **Left click**                       |
| Aim            | **Click & drag** from your character |
| Fire           | **Release** mouse button             |
| Quit           | **Esc** or close window              |

---

## Technical Documentation

### Game Algorithm

1. **Startup** — initialize Pygame, create window, clock, and load assets.
2. **Main Menu** — `afficher_accueil()` waits for *Play* click.
3. **Selections** — `character_and_weapon_select()` + `map_selection()` gather user choices.
4. **Initialisation** — create `Game(choix_joueurs)`; load `Map`, spawn `Player`, `Master`, and set camera bounds.
5. **Gameplay Loop** *(in **************************************`main.py`**************************************)*

   1. Handle events (`pygame.event.get()`), mouse drags, keyboard shortcuts.
   2. Update physics (gravity, projectile motion with Δt).
   3. Call `game.update(screen, camera)` → draw sprites, check collisions, update health.
   4. Smooth‑follow `Camera.update()` and blit viewport to screen.
   5. Detect win/lose; display victory banner or restart.
6. **Shutdown** — call `pygame.quit()`.

### Function Prototypes

| Module                      | Prototype                                                        | Short Description                                                              |
| --------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **accueil.py**              | `afficher_accueil(screen)`                                       | Display the main menu and wait until the player clicks **Play**.               |
| **camera.py**               | `Camera.__init__(width, height)`                                 | Create a camera with given viewport size and reset its offset.                 |
| **camera.py**               | `Camera.smooth_update(target, dt)`                               | Smoothly interpolate the camera toward the target each frame.                  |
| **camera.py**               | `Camera.update(target)`                                          | Instantly center the camera on the target sprite.                              |
| **character\_selection.py** | `character_and_weapon_select(screen)`                            | Interactive menu for players to pick characters & weapons; returns selections. |
| **character\_selection.py** | `map_selection(screen)`                                          | Let the user choose between **Earth**, **Moon**, or **Mars** maps.             |
| **game.py**                 | `Game.__init__(choix_joueurs)`                                   | Initialize the game world, entities, and sprite groups from user choices.      |
| **game.py**                 | `Game.check_collision(sprite, group)`                            | Collision test between a sprite and a group.                                   |
| **game.py**                 | `Game.update(screen, camera)`                                    | Main per‑frame update: handle physics, draw sprites, detect victory.           |
| **main.py**                 | `get_ground_y(sprite)`                                           | Compute the Y‑coordinate where the sprite touches the terrain mask.            |
| **map.py**                  | `generate_map(width, height, tile_size, map_name)`               | Procedurally build terrain surface & collision mask for the selected map.      |
| **master.py**               | `Master.__init__(game, selection)`                               | Create the second player's character, load sprite, and init stats/projectiles. |
| **master.py**               | `Master.damage(damage)`                                          | Subtract health and flag defeat when it reaches zero.                          |
| **master.py**               | `Master.launch_master_projectile(angle, selection, velocity=50)` | Spawn and fire a projectile.                                                   |
| **master.py**               | `Master.update_health_bar(surface, camera)`                      | Draw the second player's health bar relative to the camera.                    |
| **player.py**               | `Player.__init__(game, selection)`                               | Instantiate the first player character with chosen sprite & weapon.            |
| **player.py**               | `Player.damage(damage)`                                          | Reduce first player health and handle defeat.                                  |
| **player.py**               | `Player.launch_player_projectile(angle, selection, velocity=50)` | Spawn a projectile fired by the first player.                                  |
| **player.py**               | `Player.update_health_bar(surface, camera)`                      | Render the first player’s health bar in world space.                           |
| **projectile.py**           | `Projectile.__init__(user, angle, selection, velocity)`          | Construct a projectile sprite with initial velocity & rotation.                |
| **projectile.py**           | `Projectile.move(dt)`                                            | Advance the projectile, apply gravity, rotate image, test collisions.          |
| **projectile.py**           | `Projectile.remove()`                                            | Destroy the projectile.                                                        |
| **projectile.py**           | `Projectile.rotate()`                                            | Rotate the projectile sprite.                                                  |



### Input & Error Management

* **Validation & Clamping** — drag distance converted to `power_ratio ∈ [0,1]`; projectile speed is capped.
* **Collision Detection** — mask‑based (`pygame.sprite.collide_mask`) with graceful fallback to rect overlap.
* **Known Bugs**

  * The “Restart” option after victory screen is pending implementation.





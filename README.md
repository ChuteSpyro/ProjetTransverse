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
8. [Testing & Validation](#testing--validation)
9. [Screenshots](#screenshots)

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
3. **Install Pygame (seule dépendance externe)**

   ```bash
   pip install pygame  # ou 'pip install pygame==2.1.3' pour une version spécifique
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

| Module                  | Prototype                                                       |
| ----------------------- | --------------------------------------------------------------- |
| accueil.py              | `afficher_accueil(screen)`                                      |
| camera.py               | `__init__(self, width, height)`                                 |
| camera.py               | `smooth_update(self, target: pygame.sprite.Sprite, dt: float)`  |
| camera.py               | `update(self, target: pygame.sprite.Sprite)`                    |
| character\_selection.py | `character_and_weapon_select(screen)`                           |
| character\_selection.py | `map_selection(screen)`                                         |
| game.py                 | `__init__(self, choix_joueurs)`                                 |
| game.py                 | `check_collision(self, sprite, group)`                          |
| game.py                 | `update(self, screen, camera)`                                  |
| main.py                 | `get_ground_y(sprite)`                                          |
| map.py                  | `generate_map(width, height, tile_size, map_name)`              |
| master.py               | `__init__(self, game, selection)`                               |
| master.py               | `damage(self, damage)`                                          |
| master.py               | `launch_master_projectile(self, angle, selection, velocity=50)` |
| master.py               | `update_health_bar(self, surface, camera)`                      |
| player.py               | `__init__(self, game, selection)`                               |
| player.py               | `damage(self, damage)`                                          |
| player.py               | `launch_player_projectile(self, angle, selection, velocity=50)` |
| player.py               | `update_health_bar(self, surface, camera)`                      |
| projectile.py           | `__init__(self, user, angle, selection, velocity)`              |
| projectile.py           | `move(self, dt)`                                                |
| projectile.py           | `remove(self)`                                                  |
| projectile.py           | `rotate(self)`                                                  |

### Input & Error Management

* **Validation & Clamping** — drag distance converted to `power_ratio ∈ [0,1]`; projectile speed is capped.
* **Collision Detection** — mask‑based (`pygame.sprite.collide_mask`) with graceful fallback to rect overlap.
* **Known Bugs**

  * The “Restart” option after victory screen is pending implementation.
